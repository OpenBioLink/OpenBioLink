from graph_creation.file_reader.csvReader import CsvReader
from graph_creation.dbType import DbType
from graph_creation.metadata_db_file.edge.dbMetaEdgeString import DbMetaEdgeString
import graph_creation.globalConstant as g
import os


class EdgeStringReader(CsvReader):

    def __init__(self):
        super().__init__(
        in_path = os.path.join(g.O_FILE_PATH, DbMetaEdgeString.OFILE_NAME),
        sep = None,
            cols=DbMetaEdgeString.COLS,
            use_cols=DbMetaEdgeString.FILTER_COLS,
            nr_lines_header=DbMetaEdgeString.HEADER,
        dtypes = None,
            dbType= DbType.DB_EDGE_STRING
        )

