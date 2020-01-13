from openbiolink.graph_creation.file_processor.fileProcessor import FileProcessor
from openbiolink.graph_creation.metadata_infile.edge.inMetaEdgeCdtPath import InMetaEdgeCdtPath
from openbiolink.graph_creation.types.infileType import InfileType
from openbiolink.graph_creation.types.readerType import ReaderType


class EdgeCdtPathProcessor(FileProcessor):
    IN_META_CLASS = InMetaEdgeCdtPath

    def __init__(self):
        self.use_cols = self.IN_META_CLASS.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_EDGE_CDT_PATH,
                         infileType=InfileType.IN_EDGE_CDT_PATH, mapping_sep=self.IN_META_CLASS.MAPPING_SEP)
