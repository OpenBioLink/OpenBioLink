from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.dbType import DbType
from graph_creation.infileType import InfileType
import graph_creation.constants.in_file.edge.inEdgeStitchConstant as constant


class EdgeStitchProcessor(FileProcessor):

    def __init__(self):
        self.use_cols = constant.USE_COLS
        super().__init__(self.use_cols, dbType=DbType.DB_EDGE_STITCH, infileType=InfileType.IN_EDGE_STITCH, mapping_sep=constant.MAPPING_SEP)


    def individual_preprocessing(self, data):
        self.stitch_to_pubchem_id(data,0)
        return data