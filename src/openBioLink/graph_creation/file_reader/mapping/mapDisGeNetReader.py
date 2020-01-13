import os

from openbiolink.graph_creation import graphCreationConfig as gcConst
from openbiolink.graph_creation.file_reader.csvReader import CsvReader
from openbiolink.graph_creation.metadata_db_file.mapping.dbMetaMapDisGeNet import DbMetaMapDisGeNet
from openbiolink.graph_creation.types.dbType import DbType
from openbiolink.graph_creation.types.readerType import ReaderType


class MapDisGeNetReader(CsvReader):
    DB_META_CLASS = DbMetaMapDisGeNet

    def __init__(self):
        super().__init__(
            in_path=os.path.join(gcConst.O_FILE_PATH, self.DB_META_CLASS.OFILE_NAME),
            sep='|',
            cols=self.DB_META_CLASS.COLS,
            use_cols=self.DB_META_CLASS.FILTER_COLS,
            nr_lines_header=self.DB_META_CLASS.HEADER,
            dtypes=None,
            readerType=ReaderType.READER_MAP_DISGENET,
            dbType=DbType.DB_MAP_DISGENET
        )
