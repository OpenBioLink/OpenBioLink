from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.Types.readerType import ReaderType
from graph_creation.Types.infileType import InfileType
from graph_creation.metadata_infile.mapping.inMetaMapString import InMetaMapString



class MapStringProcessor(FileProcessor):

    def __init__(self):
        self.use_cols = InMetaMapString.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_MAP_STRING,
                         infileType=InfileType.IN_MAP_STRING, mapping_sep=InMetaMapString.MAPPING_SEP)