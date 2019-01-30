import os

import graph_creation.globalConstant as g
from graph_creation.Types.dbType import DbType
from graph_creation.Types.readerType import ReaderType
from graph_creation.file_reader.oboReader import OboReader
from graph_creation.metadata_db_file import DbMetaOntoUberon


class OntoUberonReader(OboReader):
    DB_META_CLASS = DbMetaOntoUberon

    def __init__(self):
        super().__init__(
        in_path = os.path.join(g.O_FILE_PATH, self.DB_META_CLASS.OFILE_NAME),
            quadruple_list= self.DB_META_CLASS.QUADRUPLES,
            readerType= ReaderType.READER_ONTO_UBERON,
        dbType = DbType.DB_ONTO_UBERON
        )

