from ..fileProcessor import FileProcessor
from ...types.readerType import ReaderType
from ...types.infileType import InfileType
from ...metadata_infile.edge.inMetaEdgeGo import InMetaEdgeGo


class EdgeGoProcessor(FileProcessor):
    IN_META_CLASS = InMetaEdgeGo

    def __init__(self):
        self.use_cols = self.IN_META_CLASS.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_EDGE_GO,
                         infileType=InfileType.IN_EDGE_GO, mapping_sep=self.IN_META_CLASS.MAPPING_SEP)