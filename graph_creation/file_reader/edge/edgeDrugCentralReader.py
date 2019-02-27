import os

import graph_creation.graphCreationConfig as g
from graph_creation.Types.dbType import DbType
from graph_creation.Types.readerType import ReaderType
from graph_creation.file_reader.sqlReader import SqlReader
from graph_creation.metadata_db_file.edge.dbMetaEdgeDrugCentral import DbMetaEdgeDrugCentral


class EdgeDrugCentralReader(SqlReader):

    DB_META_CLASS = DbMetaEdgeDrugCentral

    def __init__(self):
        super().__init__(
        in_path = os.path.join(g.O_FILE_PATH, self.DB_META_CLASS.OFILE_NAME),
            table_name= self.DB_META_CLASS.TABLE_NAME_IND,
            cols=self.DB_META_CLASS.COLS_IND,
            readerType= ReaderType.READER_EDGE_DRUGCENTRAL_IND,
        dbType = DbType.DB_EDGE_DRUGCENTRAL
        )

