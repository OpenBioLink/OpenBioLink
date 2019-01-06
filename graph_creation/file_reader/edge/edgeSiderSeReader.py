from graph_creation.file_reader.csvReader import CsvReader
from graph_creation.dbType import DbType
from graph_creation.metadata_db_file.edge.dbMetaEdgeSiderSe import DbMetaEdgeSiderSe
import graph_creation.globalConstant as g
import os


class EdgeSiderSeReader(CsvReader):

    def __init__(self):
        super().__init__(
        in_path = os.path.join(g.O_FILE_PATH, DbMetaEdgeSiderSe.OFILE_NAME),
        sep = None,
            cols=DbMetaEdgeSiderSe.COLS,
            use_cols=DbMetaEdgeSiderSe.FILTER_COLS,
            nr_lines_header=DbMetaEdgeSiderSe.HEADER,
        dtypes = None,
            dbType= DbType.DB_EDGE_SIDER_SE
        )

