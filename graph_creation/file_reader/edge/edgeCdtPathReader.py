from graph_creation.file_reader.csvReader import CsvReader
from graph_creation.dbType import DbType
from graph_creation.metadata_db_file.edge.dbMetaEdgeCtdPath import DbMetaEdgeCtdPath
import graph_creation.globalConstant as g
import os


class EdgeCdtPathReader(CsvReader):

    def __init__(self):
        super().__init__(
        in_path = os.path.join(g.O_FILE_PATH, DbMetaEdgeCtdPath.OFILE_NAME),
        sep = None,
        cols = DbMetaEdgeCtdPath.COLS,
        use_cols = DbMetaEdgeCtdPath.FILTER_COLS,
        nr_lines_header = DbMetaEdgeCtdPath.HEADER,
            dbType= DbType.DB_EDGE_CDT_PATH
        )

