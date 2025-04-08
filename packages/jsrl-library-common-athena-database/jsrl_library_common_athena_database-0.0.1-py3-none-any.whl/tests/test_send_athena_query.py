from jsrl_library_common.constants.database.engines import DatabaseEngine
from jsrl_library_common.utils.decorators.query_connection import query_connection_decorator

client_id = "merit-med-source-test"

params_connection = {
    "catalog": "AwsDataCatalog",
    "database": "monarch_db",
    "output_location": f"s3://mm-predict-prod-{client_id}/result/",
    "workgroup": "monarchWorkgroupDev",
    "is_async": False,
    "options": "get_status_retries=10 -c retry_delta_time=0.235"
}


@query_connection_decorator(database_engine=DatabaseEngine.ATHENA.value)
def simple_select(conn,
                  portfolio_id,
                  engine_methods):
    """Get portfolio groups information
    """
    client_table = portfolio_id.replace("-", "_")
    query = f"""
        SELECT
            *
        FROM
            {client_table}_groups
    """
    
    values = []
    
    result, response = engine_methods.execute_query(query,
                                            values,
                                            conn)
    result = list(result)
    return result, response


simple_select(client_id,
              params_connection=params_connection)
    