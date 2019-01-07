from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.Types.readerType import ReaderType
from graph_creation.Types.infileType import InfileType
from graph_creation.metadata_infile.edge.inMetaEdgeString import InMetaEdgeString



class EdgeStringProcessor(FileProcessor):

    def __init__(self):
        self.use_cols = InMetaEdgeString.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_EDGE_STRING,
                         infileType=InfileType.IN_EDGE_STRING, mapping_sep=InMetaEdgeString.MAPPING_SEP)