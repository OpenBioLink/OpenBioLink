import os

import graph_creation.graphCreationConfig as g
from graph_creation.types.dbType import DbType
from graph_creation.types.readerType import ReaderType
from graph_creation.file_reader.postgresDumpReader import PostgresDumpReader


class MapDrugCentralPubchemReader(PostgresDumpReader):
    """ to create a new csv file reader:
              *) declare the corresponding DB_META_CLASS, DB_META_CLASS.table_name, DB_META_CLASS.cols, readerType, as well as dbType
              *) for clearer structure, move class to corresponding module (and import in corresponding init)
              prior steps necessary:
              *) create DB_META_CLASS
              *) add readerType
              *) add dbType
        """

    DB_META_CLASS = None            # database meta class here

    def __init__(self):
        super().__init__(
            in_path = os.path.join(g.O_FILE_PATH, self.DB_META_CLASS.OFILE_NAME),
            table_name= None,       # table defined in DB_META_CLASS here
            cols=None,              # cols defined in DB_META_CLASS here
            readerType= None,       # reader type here
            dbType = None           # database type here
        )

