from ...types.dbType import DbType
from ...file_reader.csvReader import CsvReader
from ...types.readerType import ReaderType
from ...metadata_db_file.edge.dbMetaEdgeHpoDis import DbMetaEdgeHpoDis
from ... import graphCreationConfig as g
import os


class EdgeHpoDisReader(CsvReader):

    DB_META_CLASS = DbMetaEdgeHpoDis

    def __init__(self):
        super().__init__(
        in_path = os.path.join(g.O_FILE_PATH, self.DB_META_CLASS.OFILE_NAME),
        sep = None,
            cols=self.DB_META_CLASS.COLS,
            use_cols=self.DB_META_CLASS.FILTER_COLS,
            nr_lines_header=self.DB_META_CLASS.HEADER,
        dtypes = None,
            readerType= ReaderType.READER_EDGE_HPO_DIS,
        dbType = DbType.DB_EDGE_HPO_DIS
        )

