import os

import graph_creation.globalConstant as g
from graph_creation.Types.readerType import ReaderType
from graph_creation.file_reader.sqlReader import SqlReader
from graph_creation.metadata_db_file.edge.dbMetaEdgeDrugCentral import DbMetaEdgeDrugCentral


class MapDrugCentralPubchemReader(SqlReader):

    def __init__(self):
        self.dbMetaClass = DbMetaEdgeDrugCentral
        super().__init__(
        in_path = os.path.join(g.O_FILE_PATH, self.dbMetaClass.OFILE_NAME),
            table_name= self.dbMetaClass.TABLE_NAME_MAP_PUBCHEM,
            cols=self.dbMetaClass.COLS_MAP_PUBCHEM,
            readerType= ReaderType.READER_MAP_DRUGCENTRAL_PUBCHEM
        )

