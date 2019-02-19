from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.Types.readerType import ReaderType
from graph_creation.Types.infileType import InfileType
from graph_creation.metadata_infile import InMetaOntoGoPartOf
from graph_creation.metadata_infile.onto.inMetaOntoGoIsA import InMetaOntoGoIsA



class OntoGoPartOfProcessor(FileProcessor):

    def __init__(self):
        self.inMetaClass = InMetaOntoGoPartOf

        self.use_cols = self.inMetaClass.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_ONTO_GO,
                         infileType=InfileType.IN_ONTO_GO_PART_OF, mapping_sep=InMetaOntoGoIsA.MAPPING_SEP)