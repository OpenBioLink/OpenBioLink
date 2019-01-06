from graph_creation.file_reader.csvReader import CsvReader
from graph_creation.dbType import DbType
from graph_creation.metadata_db_file.mapping.dbMetaMapString import DbMetaMapString
import graph_creation.globalConstant as g
import os


class MapStringReader(CsvReader):
    def __init__(self):
        super().__init__(
        in_path = os.path.join(g.O_FILE_PATH, DbMetaMapString.OFILE_NAME),
        sep = None,
            cols=DbMetaMapString.COLS,
            use_cols=DbMetaMapString.FILTER_COLS,
            nr_lines_header=DbMetaMapString.HEADER,
        dtypes = None,
            dbType= DbType.DB_MAP_STRING
        )

