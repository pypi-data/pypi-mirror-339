from jsrl_library_common.models.database.database_engine_conf_model import DatabaseEngineConf

__conf = DatabaseEngineConf()
DatabaseEngine = __conf.create_engine()

ENGINE_METHODS = {database:getattr(__import__(f'{__conf.HEALTHNEXUS_DATABASE_PACKAGES}',
                                               fromlist=[database]),
                                   database)
                  for database in __conf.get_engine_list()}
