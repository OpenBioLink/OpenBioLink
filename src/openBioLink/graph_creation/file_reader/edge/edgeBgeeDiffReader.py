import os

from openbiolink.graph_creation import graphCreationConfig as g
from openbiolink.graph_creation.file_reader.csvReader import CsvReader
from openbiolink.graph_creation.metadata_db_file.edge.dbMetaEdgeBgeeDiffExpr import DbMetaEdgeBgeeDiffExpr
from openbiolink.graph_creation.types.dbType import DbType
from openbiolink.graph_creation.types.readerType import ReaderType


class EdgeBgeeDiffReader(CsvReader):
    DB_META_CLASS = DbMetaEdgeBgeeDiffExpr

    def __init__(self):
        super().__init__(
            in_path=os.path.join(g.O_FILE_PATH, self.DB_META_CLASS.OFILE_NAME),
            sep=None,
            cols=self.DB_META_CLASS.COLS,
            use_cols=self.DB_META_CLASS.FILTER_COLS,
            nr_lines_header=self.DB_META_CLASS.HEADER,
            readerType=ReaderType.READER_EDGE_BGEE_DIFF,
            dbType=DbType.DB_EDGE_BGEE_DIFF
        )
