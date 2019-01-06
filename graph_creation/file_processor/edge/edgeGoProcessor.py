from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.dbType import DbType
from graph_creation.infileType import InfileType
from graph_creation.metadata_infile.edge.inMetaEdgeGo import InMetaEdgeGo


class EdgeGoProcessor(FileProcessor):

    def __init__(self):
        self.use_cols = InMetaEdgeGo.USE_COLS
        super().__init__(self.use_cols, dbType=DbType.DB_EDGE_GO,
                         infileType=InfileType.IN_EDGE_GO, mapping_sep=InMetaEdgeGo.MAPPING_SEP)