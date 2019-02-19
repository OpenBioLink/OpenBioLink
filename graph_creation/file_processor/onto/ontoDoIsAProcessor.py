from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.Types.readerType import ReaderType
from graph_creation.Types.infileType import InfileType
from graph_creation.metadata_infile.onto.inMetaOntoDoIsA import InMetaOntoDoIsA



class OntoDoIsAProcessor(FileProcessor):

    def __init__(self):
        self.use_cols =   InMetaOntoDoIsA.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_ONTO_DO,
                         infileType=InfileType.IN_ONTO_DO_IS_A, mapping_sep=InMetaOntoDoIsA.MAPPING_SEP)