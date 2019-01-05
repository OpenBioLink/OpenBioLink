from graph_creation.file_reader.csvReader import CsvReader
from graph_creation.dbType import DbType
import graph_creation.constants.db_file.edge.dbEdgeStitchConstant as constant
import graph_creation.constants.globalConstant as g
import os


class EdgeStitchReader(CsvReader):

    def __init__(self):
        super().__init__(
        in_path = os.path.join(g.O_FILE_PATH, constant.OFILE_NAME),
        sep = None,
            cols=constant.COLS,
            use_cols=constant.FILTER_COLS,
            nr_lines_header=constant.HEADER,
        dtypes = None,
            dbType= DbType.DB_EDGE_STITCH
        )

