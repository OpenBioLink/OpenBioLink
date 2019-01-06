from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.dbType import DbType
from graph_creation.infileType import InfileType
from graph_creation.metadata_infile.edge.inMetaEdgeHpa import InMetaEdgeHpa


class EdgeHpaProcessor(FileProcessor):

    def __init__(self):
        self.use_cols = InMetaEdgeHpa.USE_COLS
        super().__init__( self.use_cols, dbType=DbType.DB_EDGE_HPA, infileType=InfileType.IN_EDGE_HPA,
                          mapping_sep=InMetaEdgeHpa.MAPPING_SEP)