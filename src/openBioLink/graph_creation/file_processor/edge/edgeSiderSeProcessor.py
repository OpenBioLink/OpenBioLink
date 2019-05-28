from ..fileProcessor import FileProcessor
from ...types.readerType import ReaderType
from ...types.infileType import InfileType
from ...metadata_infile.edge.inMetaEdgeSiderSe import InMetaEdgeSiderSe


class EdgeSiderSeProcessor(FileProcessor):
    IN_META_CLASS = InMetaEdgeSiderSe

    def __init__(self):
        self.use_cols = self.IN_META_CLASS.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_EDGE_SIDER_SE,
                         infileType=InfileType.IN_EDGE_SIDER_SE, mapping_sep=self.IN_META_CLASS.MAPPING_SEP)


    def individual_postprocessing(self, data):
        self.stitch_to_pubchem_id(data, self.use_cols.index('stitchID_stereo'))
        return data