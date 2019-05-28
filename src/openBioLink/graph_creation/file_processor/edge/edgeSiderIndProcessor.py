from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.types.readerType import ReaderType
from graph_creation.types.infileType import InfileType
from graph_creation.metadata_infile.edge.inMetaEdgeSiderInd import InMetaEdgeSiderInd


class EdgeSiderIndProcessor(FileProcessor):
    IN_META_CLASS = InMetaEdgeSiderInd

    def __init__(self):
        self.use_cols = self.IN_META_CLASS.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_EDGE_SIDER_IND,
                         infileType=InfileType.IN_EDGE_SIDER_IND, mapping_sep=self.IN_META_CLASS.MAPPING_SEP)

    def individual_postprocessing(self, data):
        self.stitch_to_pubchem_id(data, 1)
        return data