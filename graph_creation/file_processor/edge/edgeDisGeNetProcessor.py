from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.Types.readerType import ReaderType
from graph_creation.Types.infileType import InfileType
from graph_creation.metadata_infile.edge.inMetaEdgeDisGeNet import InMetaEdgeDisGeNet


class EdgeDisGeNetProcessor(FileProcessor):

    def __init__(self):
        self.use_cols = InMetaEdgeDisGeNet.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_EDGE_DISGENET, infileType=InfileType.IN_EDGE_DISGENET,
                         mapping_sep=InMetaEdgeDisGeNet.MAPPING_SEP)