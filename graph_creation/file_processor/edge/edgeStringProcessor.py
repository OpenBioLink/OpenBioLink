from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.dbType import DbType
from graph_creation.infileType import InfileType
from graph_creation.metadata_infile.edge.inMetaEdgeString import InMetaEdgeString



class EdgeStringProcessor(FileProcessor):

    def __init__(self):
        self.use_cols = InMetaEdgeString.USE_COLS
        super().__init__(self.use_cols, dbType=DbType.DB_EDGE_STRING,
                         infileType=InfileType.IN_EDGE_STRING, mapping_sep=InMetaEdgeString.MAPPING_SEP)