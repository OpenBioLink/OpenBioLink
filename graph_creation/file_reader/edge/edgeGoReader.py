from graph_creation.file_reader.csvReader import CsvReader
from graph_creation.dbType import DbType
from graph_creation.metadata_db_file.edge.dbMetaEdgeGo import DbMetaEdgeGo
import graph_creation.globalConstant as g
import os


class EdgeGoReader(CsvReader):

    def __init__(self):
        super().__init__(
        in_path = os.path.join(g.O_FILE_PATH, DbMetaEdgeGo.OFILE_NAME),
        sep = None,
            cols=DbMetaEdgeGo.COLS,
            use_cols=DbMetaEdgeGo.FILTER_COLS,
            nr_lines_header=DbMetaEdgeGo.HEADER,
        dtypes = None,
            dbType= DbType.DB_EDGE_GO
        )

