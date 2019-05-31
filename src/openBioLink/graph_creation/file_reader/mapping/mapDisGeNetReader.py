from ...types.dbType import DbType
from ...file_reader.csvReader import CsvReader
from ...types.readerType import ReaderType
from ...metadata_db_file.mapping.dbMetaMapDisGeNet import DbMetaMapDisGeNet
from ... import graphCreationConfig as gcConst
import os

class MapDisGeNetReader(CsvReader):

    DB_META_CLASS = DbMetaMapDisGeNet

    def __init__(self):
        super().__init__(
        in_path = os.path.join(gcConst.O_FILE_PATH, self.DB_META_CLASS.OFILE_NAME),
        sep = '|',
            cols=self.DB_META_CLASS.COLS,
            use_cols=self.DB_META_CLASS.FILTER_COLS,
            nr_lines_header=self.DB_META_CLASS.HEADER,
        dtypes = None,
            readerType= ReaderType.READER_MAP_DISGENET,
        dbType = DbType.DB_MAP_DISGENET
        )

