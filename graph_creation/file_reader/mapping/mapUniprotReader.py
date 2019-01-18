from graph_creation.Types.dbType import DbType
from graph_creation.file_reader.csvReader import CsvReader
from graph_creation.Types.readerType import ReaderType
from graph_creation.metadata_db_file.mapping.dbMetaMapUniprot import DbMetaMapUniprot
import graph_creation.globalConstant as g
import os


class MapUniprotReader(CsvReader):

    DB_META_CLASS = DbMetaMapUniprot

    def __init__(self):
        super().__init__(
        in_path = os.path.join(g.O_FILE_PATH, self.DB_META_CLASS.OFILE_NAME),
        sep = None,
            cols=self.DB_META_CLASS.COLS,
            use_cols=self.DB_META_CLASS.FILTER_COLS,
            nr_lines_header=self.DB_META_CLASS.HEADER,
            dtypes=self.DB_META_CLASS.DTYPES,
            readerType= ReaderType.READER_MAP_UNIPROT,
        dbType = DbType.DB_MAP_UNIPROT
        )

