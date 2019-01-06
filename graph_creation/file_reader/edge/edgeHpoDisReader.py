from graph_creation.file_reader.csvReader import CsvReader
from graph_creation.dbType import DbType
from graph_creation.metadata_db_file.edge.dbMetaEdgeHpoDis import DbMetaEdgeHpoDis
import graph_creation.globalConstant as g
import os


class EdgeHpoDisReader(CsvReader):

    def __init__(self):
        super().__init__(
        in_path = os.path.join(g.O_FILE_PATH, DbMetaEdgeHpoDis.OFILE_NAME),
        sep = None,
            cols=DbMetaEdgeHpoDis.COLS,
            use_cols=DbMetaEdgeHpoDis.FILTER_COLS,
            nr_lines_header=DbMetaEdgeHpoDis.HEADER,
        dtypes = None,
            dbType= DbType.DB_EDGE_HPO_DIS
        )

