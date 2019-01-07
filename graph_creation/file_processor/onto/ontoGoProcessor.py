from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.Types.readerType import ReaderType
from graph_creation.Types.infileType import InfileType
from graph_creation.metadata_infile.onto.inMetaOntoGo import InMetaOntoGo



class OntoGoProcessor(FileProcessor):

    def __init__(self):
        self.use_cols = InMetaOntoGo.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_ONTO_GO,
                         infileType=InfileType.IN_ONTO_GO, mapping_sep=InMetaOntoGo.MAPPING_SEP)