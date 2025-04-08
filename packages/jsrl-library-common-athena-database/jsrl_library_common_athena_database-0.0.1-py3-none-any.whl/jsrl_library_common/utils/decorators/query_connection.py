import os
import sys
# sys.path.append(os.path.join(sys.path[0], '..', '..', '..'))
from jsrl_library_common.constants.database.engines import DatabaseEngine, ENGINE_METHODS
from jsrl_library_common.utils.decorators.inject_parameters import parameters_injection_decorator

def query_connection_decorator(database_name='',
                               database_engine=DatabaseEngine._member_map_[DatabaseEngine._member_names_[0]].value,
                               retry_connection=False,
                               retries_limit=-1,
                               encode_connection_client=False,
                               encode_func=None):
    """Create database connection and pass additional parameters to use engine methods

    Args:
        - database_name (string): the environment database name
        - database_engine (enum): the databas engine
        - retry_connection (bool): activate the retry connection mode
        - retries_limit (int): the limit of retries (-1 is infinit)
        - encode_connection_client (bool): activate utf8 client encode
        - encode_func (None|function): the custom encode

    Note:
        In invoke mode, you can pass the next kwargs parameters:
            - params_connection (dict): the database connection params object
            - engine (enum string): the database engine
            - database (string): the environment database name
            - retry (bool): active the retry connection mode
            - retry_limit (int): the limit of retries. -1 no limit
            - encode (bool): activate the enconde adjust
            - encode_func (None|function): the encode function to apply. 
                    NOTE: If `encode_connection_client` is True, the encode function parameter
                          must be a function with only one parameter (receive the database connection)
                          and that function have to return the connection updated

    Returns:
        - func: the wrapper
    """

    def decorator(func):

        def __build_connection(database,
                               params_connection,
                               engine_methods,
                               retry_conn,
                               retry_limit):
            """Build connection if need retry database connection
            mode or not

            Args:
                - database (string): the environment database name
                - params_connection (dict): the database params connection (if connection is dinamic)
                - engine_methods (module): the database engine methods
                - retry_conn (bool): if connection fail, does the process retry?

            Returns:
                - connection: the database connection
            """
            
            if (retry_conn):
                conn = engine_methods.get_retry_connection(database,
                                                           params_connection,
                                                           retry_limit)
            else:
                conn = engine_methods.get_connection(database, params_connection)
                
            return conn
        

        def __encode_connection_client(conn,
                                       encode_func,
                                       engine_methods):
            """Apply encode function to connection

            Args:
                - conn (connection): the database connection
                - encode_func (None|function): the encode apply function
                - engine_methods (module): the databas engine methods

            Returns:
                - connection: the set connection
            """    
            if (encode_func == None):
                conn = engine_methods.set_utf8_unicode_conn(conn)
            else:
                conn = encode_func(conn)
            return conn
        
        
        def wrapper(*args, **kwargs):
            """Create connection and pass to parameter function to realice query call,
            this connection could be filter by specific database.
            
            Note:
                If you want pass the params_connection by code, use the param "params_connection"
                as key word argument, as following:
                
                POSTGRESQL:
                    func(..., params_connection={
                        "host": ...,
                        "dbname": ...
                    })
                    
                Also you can define the "engine" and "database" by function invoke parameters

            Args:
                - args: Tuple arguments from func
                - kwargs: Dict arguments from func
                    - decorator parameters:
                        - params_connection (dict): the database connection params object
                        - engine (enum string): the database engine
                        - database (string): the environment database name
                        - retry (bool): active the retry connection mode
                        - retry_limit (int): the limit of retries (-1 is infinite)
                        - encode (bool): activate the enconde adjust
                        - encode_func (None|function): the encode function to apply
                                NOTE: If `encode_connection_client` is True, the encode function parameter
                                      must be a function with only one parameter (receive the database connection)
                                      and that function have to return the connection updated

            
            Returns:
                - any: function data return
            """
            try:
                params_connection = kwargs.pop('params_connection', {})
                engine = kwargs.pop("engine", database_engine)
                database = kwargs.pop('database',database_name)
                retry_conn = kwargs.pop('retry', retry_connection)
                retry_limit = kwargs.pop('retry_limit', retries_limit)
                encode = kwargs.pop('encode', encode_connection_client)
                encode_apply_func = kwargs.pop('encode_func', encode_func)

                engine_methods = ENGINE_METHODS[engine]

                conn = __build_connection(database,
                                          params_connection,
                                          engine_methods,
                                          retry_conn,
                                          retry_limit)
                
                if (encode):
                    conn = __encode_connection_client(conn,
                                                      encode_apply_func,
                                                      engine_methods)

                additional_resources = {
                    "engine_methods": engine_methods,
                    "engine": engine,
                    "_database": database 
                }

                exec_func = parameters_injection_decorator(conn, **additional_resources)(func)
                data = exec_func(*args, **kwargs)
                return data
            finally:
                if 'conn' in locals():
                    engine_methods.close_connection(conn, database)
                
        return wrapper

    return decorator
