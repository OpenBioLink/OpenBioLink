from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.dbType import DbType
from graph_creation.infileType import InfileType
from graph_creation.metadata_infile.edge.inMetaEdgeCdtPath import InMetaEdgeCdtPath


class EdgeCdtPathProcessor(FileProcessor):

    def __init__(self):
        self.use_cols =  InMetaEdgeCdtPath.USE_COLS
        super().__init__(self.use_cols, dbType=DbType.DB_EDGE_CDT_PATH,
                         infileType=InfileType.IN_EDGE_CDT_PATH, mapping_sep=InMetaEdgeCdtPath.MAPPING_SEP)