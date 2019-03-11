from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.Types.readerType import ReaderType
from graph_creation.Types.infileType import InfileType
from graph_creation.metadata_infile.edge.inMetaEdgeCdtPath import InMetaEdgeCdtPath


class EdgeCdtPathProcessor(FileProcessor):
    IN_META_CLASS = InMetaEdgeCdtPath

    def __init__(self):
        self.use_cols =  self.IN_META_CLASS.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_EDGE_CDT_PATH,
                         infileType=InfileType.IN_EDGE_CDT_PATH, mapping_sep=self.IN_META_CLASS.MAPPING_SEP)