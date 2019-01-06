from graph_creation.file_reader.csvReader import CsvReader
from graph_creation.dbType import DbType
from graph_creation.metadata_db_file.mapping.dbMetaMapDisGeNet import DbMetaMapDisGeNet
import graph_creation.globalConstant as g
import os

class MapDisGeNetReader(CsvReader):

    def __init__(self):
        super().__init__(
        in_path = os.path.join(g.O_FILE_PATH, DbMetaMapDisGeNet.OFILE_NAME),
        sep = None,
            cols=DbMetaMapDisGeNet.COLS,
            use_cols=DbMetaMapDisGeNet.FILTER_COLS,
            nr_lines_header=DbMetaMapDisGeNet.HEADER,
        dtypes = None,
            dbType= DbType.DB_MAP_DISGENET
        )

