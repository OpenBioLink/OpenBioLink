from openbiolink.graph_creation.file_processor.fileProcessor import FileProcessor
from openbiolink.graph_creation.metadata_infile.edge.inMetaEdgeGo import InMetaEdgeGo
from openbiolink.graph_creation.types.infileType import InfileType
from openbiolink.graph_creation.types.readerType import ReaderType


class EdgeGoProcessor(FileProcessor):
    IN_META_CLASS = InMetaEdgeGo

    def __init__(self):
        self.use_cols = self.IN_META_CLASS.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_EDGE_GO,
                         infileType=InfileType.IN_EDGE_GO, mapping_sep=self.IN_META_CLASS.MAPPING_SEP)
