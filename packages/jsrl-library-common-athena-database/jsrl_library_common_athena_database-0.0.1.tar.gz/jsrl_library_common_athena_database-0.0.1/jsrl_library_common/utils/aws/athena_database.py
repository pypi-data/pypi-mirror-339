import boto3
from botocore import exceptions

def execute_async_query(query,
                        database,
                        values=[],
                        catalog=None,
                        workgroup=None,
                        output_location=None,
                        athena_client=None):
    """Execute athena query

    Args:
        - query (str): the query to execute
        - database (str): the athena database
        - catalog (str, optional): the athena catalog. Defaults to None.
        - workgroup (str, optional): the athena workgroup. Defaults to None.
        - output_location (str, optional): the query output location. Defaults to None.
        - athena_client (boto3.client, optional): the athena client. Defaults to None.

    Returns:
        - str: the athene execution query id
        - boto3.client: the athena client
    """
    response = None
    try:
        catalog = catalog if catalog else "AwsDataCatalog"
        workgroup = workgroup if workgroup else "primary"
        client = _get_athena_connection(athena_client)
        execution_params = {
            "QueryString": query,
            "QueryExecutionContext": {
                "Database": database,
                "Catalog": catalog
            },
            "ResultConfiguration": {
                "OutputLocation": output_location
            },
            "WorkGroup": workgroup
        }
        if values:
            execution_params["ExecutionParameters"] = values
        result = client.start_query_execution(**execution_params)
        response = result["QueryExecutionId"]
        return response, client
    except exceptions.ClientError as ex:
        raise ex
        

def get_query_information_status(query_id, athena_client=None):
    """Get the query information

    Args:
        - query_id (str): the query execution id
        - athena_client (boto3.client, optional): the athena client. Defaults to None.
        
    Returns:
        - dict: the query execution information
        - boto3.client: the athena client
    """
    client = _get_athena_connection(athena_client)
    result = client.get_query_execution(QueryExecutionId=query_id)
    return result, client


def get_query_results(query_id, athena_client=None):
    """Get the execution query results

    Args:
        - query_id (str): the execution query id
        - athena_client (boto3.client, optional): the athena client. Defaults to None.
        
    Returns:
        - dict: the query execution information
        - boto3.client: the athena client
    """
    client = _get_athena_connection(athena_client)
    flag = True
    response = {"values": [], "cols": {}}
    func_params = {
        "QueryExecutionId": query_id,
        "MaxResults": 100
    }
    while flag:
        result = client.get_query_results(**func_params)
        if not result.get("NextToken"):
            flag = False
            response["cols"] = {col.pop("Name"):col for col in result["ResultSet"]["ResultSetMetadata"]["ColumnInfo"]}
        response["values"] += [[col["VarCharValue"] if col else None for col in row["Data"]] for row in result["ResultSet"]["Rows"]]
    
    return response, client


def _get_athena_connection(athena_client=None):
    """Get the athena connection

    Args:
        - athena_client (boto3.client, optional): the athena client if exists

    Returns:
        - boto3.client: the athena client
    """
    client = None
    client = athena_client if athena_client else boto3.client("athena")
    return client