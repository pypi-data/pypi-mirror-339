import os
import time
import logging
import datetime
from functools import partial
from jsrl_library_common.utils.aws import athena_database as athena
from jsrl_library_common.exceptions.database import athena_exceptions
from jsrl_library_common.models.database.athena_conn_model import AthenaConnection
from jsrl_library_common.constants.database.athena_constants import RETRY_DELTA_TIME
from jsrl_library_common.constants.database.athena_constants import AthenaQueryStatus

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s -%(levelname)s - %(name)s - %(message)s',
                    force=True)
logger = logging.getLogger(__name__)

_CONF = {}

def get_connection(database='', params_connection={}):
    """Get database conection
    
    Args:
        - database(string): get connection params by specific database which are 
                            related the enviroment variables
        - params_connection (dict): the params connection defined by code 
        
    Returns:
        - connection: database connection
    """
    dbconfig = get_db_params(database, params_connection)
    conn = AthenaConnection(**dbconfig)
    return conn


def get_retry_connection(database='',
                         params_connection={},
                         retries_limit=-1):
    """Get database connection throught retry method

    Args:
        - database (string): get connection params by specific database which are 
                            related the enviroment variables
        - params_connection (dict): the params connection defined by code
        - retries_limit (int): the limit of retries to generate the connection. Defaults to -1.
        
    Returns:
        - connection: database connection
    """
    retry = True
    retries = 1
    while retry:
        conn = _get_retry_connection(database,
                                      params_connection)
        retry = (conn == None) if (retries_limit == -1) \
                               else (conn == None) and (retries <= retries_limit)
        if (retry):
            logger.info("[MESSAGE] Get connection is taking a break...")
            time.sleep(RETRY_DELTA_TIME)
            logger.info("[MESSAGE] Get connection retry #" + str(retries))
            retries += 1
    return conn


def get_db_params(database='', params_connection: dict = {}):
    """Get database connection parameters.

    Args:
        - database (string): get the connection params where 
                             its enviroment has exactly the database string
        - params_connection (dict): the params connection defined by code. Defaults to {}.

    Returns:
        - dict: database connection parameters.
                - catalog: athena catalog.
                - database: athena database name.
                - output_location: athena database output path.
                - workgroup: athena workgroup.
                - is_async: is the request asynchronous?.
                - options: the athena database connection options
    """
    async_func = lambda value: True if value == "True" else False
    if (params_connection):
        if type(params_connection["is_async"]) is str:
            params_connection["is_async"] = async_func(params_connection["is_async"])
        
        if type(params_connection["options"]) is str:
            options = params_connection["options"]
            params_connection["options"] = dict(attr.strip().split("=") for attr in options.split("-c"))
        return params_connection
    
    if not database:
        database = ''
        
    database = database.upper()
    options = params_connection.get("options", os.environ.get(f'MERIT_MEDICINE_{database}DB_OPTIONS'))
    if type(options) is str:
        options = dict(attr.strip().split("=") for attr in options.split("-c"))
    elif options is None:
        options = {}
    return {
        "catalog": os.environ.get(f'MERIT_MEDICINE_{database}DB_CATALOG', "AwsDataCatalog"),
        "database": os.environ.get(f'MERIT_MEDICINE_{database}DB_SCHEMA'),
        "output_location": os.environ.get(f'MERIT_MEDICINE_{database}DB_OUTPUT_LOCATION'),
        "workgroup": os.environ.get(f'MERIT_MEDICINE_{database}DB_WORKGROUP'),
        "is_async": async_func(os.environ.get(f'MERIT_MEDICINE_{database}DB_ASYNC_PROCESS', "True")),
        "options": options
    }
        
        
def close_connection(connection, database):
    """Close the athena client connection

    Args:
        - connection (AthenaConnection): the athena connection object
        - database (str): the database
    """
    connection.close()
    
    
def execute_query(query,
                  params,
                  connection):
    """Execute database query.
    
    Args:
        - query (string): query to execute.
        - params (tuple): query parameters.
        - connection (psycopg2.extensions.connection): database connection.
        
    Returns:
        - generator: the query response objects
        - str: the query id
    """
    query_id, _ = athena.execute_async_query(query,
                                             connection.connection_params["database"],
                                             params,
                                             catalog=connection.connection_params["catalog"],
                                             workgroup=connection.connection_params["workgroup"],
                                             output_location=connection.connection_params["output_location"],
                                             athena_client=connection.conn)
    
    if connection.connection_params["is_async"]:
        return query_id
    
    results = _get_query_results(query_id, connection)
    
    return results, query_id

    
def _get_query_results(query_id, connection):
    """Get the query results

    Args:
        - query_id (str): the athena query execution id
        - connection (AthenaConnection): the athena connection object

    Raises:
        - Exception: the query failed
        - QueryNotReady: the query have not finished yet.

    Returns:
        - generator: the query response objects
    """
    response = None
    retries = None if int(connection.connection_params["options"].get("get_status_retries", -1)) == -1 \
                   else int(connection.connection_params["options"].get("get_status_retries", -1))
    retry = 0
    logger.info(f"Number of retries: {retries}")
    flag = True
    result = None
    while flag:
        result, _ = athena.get_query_information_status(query_id, connection.conn)
        if result["QueryExecution"]["Status"]["State"] == AthenaQueryStatus.SUCCEEDED.value:
            result, _ = athena.get_query_results(query_id, connection.conn)
            response = _generate_response_obj(result["values"], result["cols"])
            flag = False
        elif result["QueryExecution"]["Status"]["State"] in (AthenaQueryStatus.FAILED.value, AthenaQueryStatus.CANCELLED.value):
            raise Exception(result["QueryExecution"]["Status"]["AthenaError"]["ErrorMessage"])
        
        if flag and retries is not None:
            retry += 1
            flag = retry < retries
            if flag:
                logger.info(f"Get query result is taking a break..")
                time.sleep(float(connection.connection_params["options"].get("retry_delta_time", RETRY_DELTA_TIME)))
                logger.info(f"Start retry #{retry}..")
            
    if response is None:
        raise athena_exceptions.QueryNotReady(query_id, result["QueryExecution"]["Status"]["State"])
    
    return response
    
    
def _generate_response_obj(data, data_type):
    """Generate the response object

    Args:
        - data (list): the athena query data response
        
    Returns:
        - generator: the response objects
    """
    headers = data[0]
    for row in data[1:]:
        yield dict((col, _map_column_type(value, data_type[col]))
                   for (col, value) in zip(headers, row))
    
    
def _map_column_type(value, athena_col_type):
    """Map the athena response column with the python type
    based on the column table setup

    Args:
        - value (str): the value to map
        - athena_col_type (dict): the athena column type definition
        
    Returns:
        - any: the value mapped to the expected type
    """
    response = value
    python_type = {
        "int": int,
        "tinyint": int,
        "float": float,
        "bigint": int,
        "string": str,
        "varchar": str,
        "double": float,
        "boolean": _bool_athena_col_type,
        "date": partial(datetime.datetime.strptime, format="%Y-%m-%d %H:%M:%S.%f %Z")
    }
    apply_func = python_type.get(athena_col_type["Type"], str)
    if value is not None:
        response = apply_func(value)
    return response
    

def _bool_athena_col_type(value):
    """Map the bool type to python type

    Args:
        - value (str): the athena response value

    Returns:
        - bool: the mapped value
    """
    response = True
    if value == "false":
        response = False
    return response
    
    
def _get_retry_connection(database='',
                          params_connection={}):
    """Get database connection and handler if the connection
    was created or not

    Args:
        - database(string): get connection params by specific database which are 
                            related the enviroment variables
        - params_connection (dict): the params connection defined by code 
        
    Returns:
        - connection | None: database connection
    """
    conn = None
    try:
        conn = get_connection(database,
                              params_connection)
    finally:
        return conn
        