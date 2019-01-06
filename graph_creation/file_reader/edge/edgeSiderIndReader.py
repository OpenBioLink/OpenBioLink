from graph_creation.file_reader.csvReader import CsvReader
from graph_creation.dbType import DbType
from graph_creation.metadata_db_file.edge.dbMetaEdgeSiderInd import DbMetaEdgeSiderInd
import graph_creation.globalConstant as g
import os


class EdgeSiderIndReader(CsvReader):

    def __init__(self):
        super().__init__(
        in_path = os.path.join(g.O_FILE_PATH, DbMetaEdgeSiderInd.OFILE_NAME),
        sep = None,
        cols=DbMetaEdgeSiderInd.COLS,
        use_cols=DbMetaEdgeSiderInd.FILTER_COLS,
        nr_lines_header=DbMetaEdgeSiderInd.HEADER,
        dtypes = None,
            dbType= DbType.DB_EDGE_SIDER_IND
        )

