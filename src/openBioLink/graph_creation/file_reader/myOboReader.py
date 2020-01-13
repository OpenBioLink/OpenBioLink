import os

from openbiolink.graph_creation import graphCreationConfig as g
# from openbiolink.graph_creationtypes.dbType import DbType
# from openbiolink.graph_creationtypes.readerType import ReaderType
from openbiolink.graph_creation.file_reader.oboReader import OboReader


class MyOntoReader(OboReader):
    """ to create a new obo file reader:
       *) declare the corresponding DB_META_CLASS, readerType, as well as dbType
       *) for clearer structure, move class to corresponding module (and import in corresponding init)
       prior steps necessary:
       *) create DB_META_CLASS
       *) add readerType
       *) add dbType
        """

    DB_META_CLASS = None  # database metaclass here

    def __init__(self):
        super().__init__(
            in_path=os.path.join(g.O_FILE_PATH, self.DB_META_CLASS.OFILE_NAME),
            quadruple_list=self.DB_META_CLASS.QUADRUPLES,
            readerType=None,  # reader type here
            dbType=None  # database type here
        )
