from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.dbType import DbType
from graph_creation.infileType import InfileType
from graph_creation.metadata_infile.edge.inMetaEdgeSiderInd import InMetaEdgeSiderInd


class EdgeSiderIndProcessor(FileProcessor):

    def __init__(self):
        self.use_cols = InMetaEdgeSiderInd.USE_COLS
        super().__init__(self.use_cols, dbType=DbType.DB_EDGE_SIDER_IND,
                         infileType=InfileType.IN_EDGE_SIDER_IND, mapping_sep=InMetaEdgeSiderInd.MAPPING_SEP)