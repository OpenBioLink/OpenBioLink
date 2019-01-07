from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.Types.readerType import ReaderType
from graph_creation.Types.infileType import InfileType
from graph_creation.metadata_infile.onto.inMetaOntoHpo import InMetaOntoHpo



class OntoHpoProcessor(FileProcessor):

    def __init__(self):
        self.use_cols = InMetaOntoHpo.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_ONTO_HPO,
                         infileType=InfileType.IN_ONTO_HPO, mapping_sep=InMetaOntoHpo.MAPPING_SEP)