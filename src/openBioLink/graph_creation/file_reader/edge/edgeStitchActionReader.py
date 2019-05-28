import os

from ... import graphCreationConfig as g
from ...types.dbType import DbType
from ...types.readerType import ReaderType
from ...file_reader.csvReader import CsvReader
from ...metadata_db_file import DbMetaEdgeStitchAction


class EdgeStitchActionReader(CsvReader):

    DB_META_CLASS = DbMetaEdgeStitchAction

    def __init__(self):
        super().__init__(
        in_path = os.path.join(g.O_FILE_PATH, self.DB_META_CLASS.OFILE_NAME),
        sep = None,
            cols=self.DB_META_CLASS.COLS,
            use_cols=self.DB_META_CLASS.FILTER_COLS,
            nr_lines_header=self.DB_META_CLASS.HEADER,
        dtypes = None,
            readerType= ReaderType.READER_EDGE_STITCH_ACTION,
        dbType = DbType.DB_EDGE_STITCH_ACTION
        )

