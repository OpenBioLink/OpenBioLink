from ...types.dbType import DbType
from ...file_reader.oboReader import OboReader
from ...types.readerType import ReaderType
from ...metadata_db_file.onto.dbMetaOntoGo import DbMetaOntoGo
from ... import graphCreationConfig as g
import os

class OntoGoReader(OboReader):
    DB_META_CLASS = DbMetaOntoGo

    def __init__(self):
        super().__init__(
        in_path = os.path.join(g.O_FILE_PATH, self.DB_META_CLASS.OFILE_NAME),
            quadruple_list= self.DB_META_CLASS.QUADRUPLES,
            readerType= ReaderType.READER_ONTO_GO,
        dbType = DbType.DB_ONTO_GO
        )

