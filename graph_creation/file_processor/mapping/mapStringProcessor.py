from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.types.readerType import ReaderType
from graph_creation.types.infileType import InfileType
from graph_creation.metadata_infile.mapping.inMetaMapString import InMetaMapString



class MapStringProcessor(FileProcessor):
    IN_META_CLASS = InMetaMapString

    def __init__(self):
        self.use_cols = self.IN_META_CLASS.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_MAP_STRING,
                         infileType=InfileType.IN_MAP_STRING, mapping_sep=self.IN_META_CLASS.MAPPING_SEP)