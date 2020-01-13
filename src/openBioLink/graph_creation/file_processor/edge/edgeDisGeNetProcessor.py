from openbiolink.graph_creation.file_processor.fileProcessor import FileProcessor
from openbiolink.graph_creation.metadata_infile.edge.inMetaEdgeDisGeNet import InMetaEdgeDisGeNet
from openbiolink.graph_creation.types.infileType import InfileType
from openbiolink.graph_creation.types.readerType import ReaderType


class EdgeDisGeNetProcessor(FileProcessor):
    IN_META_CLASS = InMetaEdgeDisGeNet

    def __init__(self):
        self.use_cols = self.IN_META_CLASS.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_EDGE_DISGENET,
                         infileType=InfileType.IN_EDGE_DISGENET,
                         mapping_sep=self.IN_META_CLASS.MAPPING_SEP)
