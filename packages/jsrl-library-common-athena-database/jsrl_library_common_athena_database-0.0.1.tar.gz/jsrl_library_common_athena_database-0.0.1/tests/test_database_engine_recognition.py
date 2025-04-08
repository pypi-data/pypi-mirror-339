from jsrl_library_common.models.database.database_engine_conf_model import DatabaseEngineConf

test = DatabaseEngineConf()
enum = test.create_engine()
assert enum.ATHENA.value == "athena"