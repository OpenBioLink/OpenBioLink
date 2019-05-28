import os

from ... import graphCreationConfig as g
from ...types.dbType import DbType
from ...types.readerType import ReaderType
from ...file_reader.postgresDumpReader import PostgresDumpReader
from ...metadata_db_file.edge.dbMetaEdgeDrugCentral import DbMetaEdgeDrugCentral


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

