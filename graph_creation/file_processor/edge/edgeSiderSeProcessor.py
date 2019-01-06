from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.dbType import DbType
from graph_creation.infileType import InfileType
from graph_creation.metadata_infile.edge.inMetaEdgeSiderSe import InMetaEdgeSiderSe


class EdgeSiderSeProcessor(FileProcessor):

    def __init__(self):
        self.use_cols = InMetaEdgeSiderSe.USE_COLS
        super().__init__(self.use_cols, dbType=DbType.DB_EDGE_SIDER_SE,
                         infileType=InfileType.IN_EDGE_SIDER_SE, mapping_sep=InMetaEdgeSiderSe.MAPPING_SEP)


    def individual_preprocessing(self, data):
        self.stitch_to_pubchem_id(data, 0)
        return data