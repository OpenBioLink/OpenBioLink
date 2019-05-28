from ...types.dbType import DbType
from ...file_reader.csvReader import CsvReader
from ...types.readerType import ReaderType
from ...metadata_db_file.mapping.dbMetaMapUniprot import DbMetaMapUniprot
from ... import graphCreationConfig as g
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

