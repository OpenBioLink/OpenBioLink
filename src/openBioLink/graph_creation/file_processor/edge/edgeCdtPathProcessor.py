from ..fileProcessor import FileProcessor
from ...types.readerType import ReaderType
from ...types.infileType import InfileType
from ...metadata_infile.edge.inMetaEdgeCdtPath import InMetaEdgeCdtPath


class EdgeCdtPathProcessor(FileProcessor):
    IN_META_CLASS = InMetaEdgeCdtPath

    def __init__(self):
        self.use_cols =  self.IN_META_CLASS.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_EDGE_CDT_PATH,
                         infileType=InfileType.IN_EDGE_CDT_PATH, mapping_sep=self.IN_META_CLASS.MAPPING_SEP)