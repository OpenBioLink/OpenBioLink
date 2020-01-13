import os

from openbiolink.graph_creation import graphCreationConfig as g
from openbiolink.graph_creation.file_reader.oboReader import OboReader
from openbiolink.graph_creation.metadata_db_file import DbMetaOntoUberon
from openbiolink.graph_creation.types.dbType import DbType
from openbiolink.graph_creation.types.readerType import ReaderType


class OntoUberonReader(OboReader):
    DB_META_CLASS = DbMetaOntoUberon

    def __init__(self):
        super().__init__(
            in_path=os.path.join(g.O_FILE_PATH, self.DB_META_CLASS.OFILE_NAME),
            quadruple_list=self.DB_META_CLASS.QUADRUPLES,
            readerType=ReaderType.READER_ONTO_UBERON,
            dbType=DbType.DB_ONTO_UBERON
        )
