from ...types.dbType import DbType
from ...file_reader.oboReader import OboReader
from ...types.readerType import ReaderType
from ...metadata_db_file.onto.dbMetaOntoDo import DbMetaOntoDo
from ... import graphCreationConfig as g
import os

class OntoDoReader(OboReader):
    DB_META_CLASS = DbMetaOntoDo

    def __init__(self):
        super().__init__(
        in_path = os.path.join(g.O_FILE_PATH, self.DB_META_CLASS.OFILE_NAME),
            quadruple_list= self.DB_META_CLASS.QUADRUPLES,
            readerType= ReaderType.READER_ONTO_DO,
        dbType = DbType.DB_ONTO_DO
        )

