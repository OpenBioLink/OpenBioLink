from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.dbType import DbType
from graph_creation.infileType import InfileType
from graph_creation.metadata_infile.edge.inMetaEdgeHpoDis import InMetaEdgeHpoDis


class EdgeHpoDisProcessor(FileProcessor):

    def __init__(self):
        self.use_cols = InMetaEdgeHpoDis.USE_COLS
        super().__init__( self.use_cols, dbType=DbType.DB_EDGE_HPO_DIS,
                          infileType=InfileType.IN_EDGE_HPO_DIS, mapping_sep=InMetaEdgeHpoDis.MAPPING_SEP)