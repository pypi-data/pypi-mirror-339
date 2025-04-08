from jsrl_library_common.utils.aws import athena_database

class AthenaConnection:
    
    def __init__(self,
                 database,
                 catalog="AwsDataCatalog",
                 output_location=None,
                 workgroup=None,
                 is_async=True,
                 options={}):
        self.connection_params = {
            "database": database,
            "catalog": catalog,
            "output_location": output_location,
            "workgroup": workgroup,
            "is_async": is_async,
            "options": options
        }
        self.conn = athena_database._get_athena_connection()

    
    def close(self):
        self.conn.close()