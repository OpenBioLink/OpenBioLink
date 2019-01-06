from graph_creation.file_reader.csvReader import CsvReader
from graph_creation.dbType import DbType
from graph_creation.metadata_db_file.edge.dbMetaEdgeHpa import DbMetaEdgeHpa
import graph_creation.globalConstant as g
import os


class EdgeHpaReader(CsvReader):

    def __init__(self):
        super().__init__(
        in_path = os.path.join(g.O_FILE_PATH, DbMetaEdgeHpa.OFILE_NAME),
        sep = None,
            cols=DbMetaEdgeHpa.COLS,
            use_cols=DbMetaEdgeHpa.FILTER_COLS,
            nr_lines_header=DbMetaEdgeHpa.HEADER,
        dtypes = None,
            dbType= DbType.DB_EDGE_HPA
        )

