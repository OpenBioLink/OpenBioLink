from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.dbType import DbType
from graph_creation.infileType import InfileType
from graph_creation.metadata_infile.edge.inMetaEdgeStitch import InMetaEdgeStitch


class EdgeStitchProcessor(FileProcessor):

    def __init__(self):
        self.use_cols = InMetaEdgeStitch.USE_COLS
        super().__init__(self.use_cols, dbType=DbType.DB_EDGE_STITCH,
                         infileType=InfileType.IN_EDGE_STITCH, mapping_sep=InMetaEdgeStitch.MAPPING_SEP)


    def individual_preprocessing(self, data):
        self.stitch_to_pubchem_id(data,0)
        return data