import os
import logging
from enum import Enum
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                    force=True)
logger = logging.getLogger(__name__)

class DatabaseEngineConf():

    HEALTHNEXUS_DATABASE_PACKAGES = 'jsrl_library_common.utils.database'

    def create_engine(self) -> Enum:
        """Create the supported engines based on the download packages

        Returns:
            Enum: the available database engines installed
        """
        return Enum('DatabaseEngine', { name.upper():name for name in self.get_engine_list() })


    def get_engine_list(self):
        """Extract the installed database engines

        Returns:
            list: the engines that have been installed
        """
        base_path = f'{os.path.sep}'.join(__file__.split(os.path.sep)[:-4])
        database_packages_path = os.path.join(base_path, *(self.HEALTHNEXUS_DATABASE_PACKAGES).split('.'))
        return [ self.__transform_file_to_package(database) for database in os.listdir(database_packages_path) \
                                                            if database != '__init__.py' ]
    

    def __transform_file_to_package(self, package):
        """Remove the python extension of package file name

        Args:
            - package (str): the package file name

        Returns:
            - str: the python package related to file
        """
        return package[:-3] if package.endswith('.py') \
                            else package
