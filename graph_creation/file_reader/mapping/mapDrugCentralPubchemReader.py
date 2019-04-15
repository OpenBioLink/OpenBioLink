import os

import graph_creation.graphCreationConfig as g
from graph_creation.types.dbType import DbType
from graph_creation.types.readerType import ReaderType
from graph_creation.file_reader.postgresDumpReader import PostgresDumpReader
from graph_creation.metadata_db_file.edge.dbMetaEdgeDrugCentral import DbMetaEdgeDrugCentral


class MapDrugCentralPubchemReader(PostgresDumpReader):

    DB_META_CLASS = DbMetaEdgeDrugCentral

    def __init__(self):
        super().__init__(
        in_path = os.path.join(g.O_FILE_PATH, self.DB_META_CLASS.OFILE_NAME),
            table_name= self.DB_META_CLASS.TABLE_NAME_MAP_PUBCHEM,
            cols=self.DB_META_CLASS.COLS_MAP_PUBCHEM,
            readerType= ReaderType.READER_MAP_DRUGCENTRAL_PUBCHEM,
        dbType = DbType.DB_EDGE_DRUGCENTRAL
        )

