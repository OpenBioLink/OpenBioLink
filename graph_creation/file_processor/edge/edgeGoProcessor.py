from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.Types.readerType import ReaderType
from graph_creation.Types.infileType import InfileType
from graph_creation.metadata_infile.edge.inMetaEdgeGo import InMetaEdgeGo


class EdgeGoProcessor(FileProcessor):
    IN_META_CLASS = InMetaEdgeGo

    def __init__(self):
        self.use_cols = self.IN_META_CLASS.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_EDGE_GO,
                         infileType=InfileType.IN_EDGE_GO, mapping_sep=self.IN_META_CLASS.MAPPING_SEP)