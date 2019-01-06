from graph_creation.file_reader.csvReader import CsvReader
from graph_creation.dbType import DbType
from graph_creation.metadata_db_file.edge.dbMetaEdgeDisGeNet import DbMetaEdgeDisGeNet
import graph_creation.globalConstant as g
import os

class EdgeDisGeNetReader(CsvReader):

    def __init__(self):
        super().__init__(
        in_path = os.path.join(g.O_FILE_PATH, DbMetaEdgeDisGeNet.OFILE_NAME),
        sep = None,
            cols=DbMetaEdgeDisGeNet.COLS,
            use_cols=DbMetaEdgeDisGeNet.FILTER_COLS,
            nr_lines_header=DbMetaEdgeDisGeNet.HEADER,
        dtypes = None,
            dbType= DbType.DB_EDGE_DISGENET
        )

