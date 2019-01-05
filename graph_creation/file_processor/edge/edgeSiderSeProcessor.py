from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.dbType import DbType
from graph_creation.infileType import InfileType
import graph_creation.constants.in_file.edge.inEdgeSiderSeConstant as constant


class EdgeSiderSeProcessor(FileProcessor):

    def __init__(self):
        self.use_cols = constant.USE_COLS
        super().__init__(self.use_cols, dbType=DbType.DB_EDGE_SIDER_SE, infileType=InfileType.IN_EDGE_SIDER_SE, mapping_sep=constant.MAPPING_SEP)


    def individual_preprocessing(self, data):
        self.stitch_to_pubchem_id(data, 0)
        return data