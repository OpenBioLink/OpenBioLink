import os

from openbiolink.graph_creation import graphCreationConfig as g
from openbiolink.graph_creation.file_reader.postgresDumpReader import PostgresDumpReader
from openbiolink.graph_creation.metadata_db_file.edge.dbMetaEdgeDrugCentral import DbMetaEdgeDrugCentral
from openbiolink.graph_creation.types.dbType import DbType
from openbiolink.graph_creation.types.readerType import ReaderType


class EdgeDrugCentralReader(PostgresDumpReader):
    DB_META_CLASS = DbMetaEdgeDrugCentral

    def __init__(self):
        super().__init__(
            in_path=os.path.join(g.O_FILE_PATH, self.DB_META_CLASS.OFILE_NAME),
            table_name=self.DB_META_CLASS.TABLE_NAME_IND,
            cols=self.DB_META_CLASS.COLS_IND,
            readerType=ReaderType.READER_EDGE_DRUGCENTRAL_IND,
            dbType=DbType.DB_EDGE_DRUGCENTRAL
        )
