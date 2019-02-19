from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.Types.readerType import ReaderType
from graph_creation.Types.infileType import InfileType
from graph_creation.metadata_infile.onto.inMetaOntoHpoIsA import InMetaOntoHpoIsA



class OntoHpoIsAProcessor(FileProcessor):

    def __init__(self):
        self.use_cols = InMetaOntoHpoIsA.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_ONTO_HPO,
                         infileType=InfileType.IN_ONTO_HPO_IS_A, mapping_sep=InMetaOntoHpoIsA.MAPPING_SEP)