from graph_creation.types.dbType import DbType
from graph_creation.file_reader.csvReader import CsvReader
from graph_creation.types.readerType import ReaderType
from graph_creation.metadata_db_file.edge.dbMetaEdgeDisGeNet import DbMetaEdgeDisGeNet
import graph_creation.graphCreationConfig as g
import os

class EdgeDisGeNetReader(CsvReader):
    DB_META_CLASS = DbMetaEdgeDisGeNet


    def __init__(self):
        super().__init__(
        in_path = os.path.join(g.O_FILE_PATH, self.DB_META_CLASS.OFILE_NAME),
        sep = None,
            cols=self.DB_META_CLASS.COLS,
            use_cols=self.DB_META_CLASS.FILTER_COLS,
            nr_lines_header=self.DB_META_CLASS.HEADER,
        dtypes = None,
            readerType= ReaderType.READER_EDGE_DISGENET,
        dbType = DbType.DB_EDGE_DISGENET
        )

