from graph_creation.file_reader.csvReader import CsvReader
from graph_creation.dbType import DbType
from graph_creation.metadata_db_file.mapping.dbMetaMapUniprot import DbMetaMapUniprot
import graph_creation.globalConstant as g
import os


class MapUniprotReader(CsvReader):

    def __init__(self):
        super().__init__(
        in_path = os.path.join(g.O_FILE_PATH, DbMetaMapUniprot.OFILE_NAME),
        sep = None,
            cols=DbMetaMapUniprot.COLS,
            use_cols=DbMetaMapUniprot.FILTER_COLS,
            nr_lines_header=DbMetaMapUniprot.HEADER,
            dtypes=DbMetaMapUniprot.DTYPES,
            dbType= DbType.DB_MAP_UNIPROT
        )

