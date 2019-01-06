from graph_creation.file_reader.csvReader import CsvReader
from graph_creation.dbType import DbType
from graph_creation.metadata_db_file.edge.dbMetaEdgeStitch import DbMetaEdgeStitch
import graph_creation.globalConstant as g
import os


class EdgeStitchReader(CsvReader):

    def __init__(self):
        super().__init__(
        in_path = os.path.join(g.O_FILE_PATH, DbMetaEdgeStitch.OFILE_NAME),
        sep = None,
            cols=DbMetaEdgeStitch.COLS,
            use_cols=DbMetaEdgeStitch.FILTER_COLS,
            nr_lines_header=DbMetaEdgeStitch.HEADER,
        dtypes = None,
            dbType= DbType.DB_EDGE_STITCH
        )

