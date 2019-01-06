from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.dbType import DbType
from graph_creation.infileType import InfileType
from graph_creation.metadata_infile.edge.inMetaEdgeDisGeNet import InMetaEdgeDisGeNet


class EdgeDisGeNetProcessor(FileProcessor):

    def __init__(self):
        self.use_cols = InMetaEdgeDisGeNet.USE_COLS
        super().__init__(self.use_cols, dbType=DbType.DB_EDGE_DISGENET, infileType=InfileType.IN_EDGE_DISGENET,
                         mapping_sep=InMetaEdgeDisGeNet.MAPPING_SEP)