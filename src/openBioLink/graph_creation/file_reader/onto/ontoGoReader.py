import os

from openbiolink.graph_creation import graphCreationConfig as g
from openbiolink.graph_creation.file_reader.oboReader import OboReader
from openbiolink.graph_creation.metadata_db_file.onto.dbMetaOntoGo import DbMetaOntoGo
from openbiolink.graph_creation.types.dbType import DbType
from openbiolink.graph_creation.types.readerType import ReaderType


class OntoGoReader(OboReader):
    DB_META_CLASS = DbMetaOntoGo

    def __init__(self):
        super().__init__(
            in_path=os.path.join(g.O_FILE_PATH, self.DB_META_CLASS.OFILE_NAME),
            quadruple_list=self.DB_META_CLASS.QUADRUPLES,
            readerType=ReaderType.READER_ONTO_GO,
            dbType=DbType.DB_ONTO_GO
        )
