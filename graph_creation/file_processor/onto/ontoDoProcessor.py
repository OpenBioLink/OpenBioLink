from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.Types.readerType import ReaderType
from graph_creation.Types.infileType import InfileType
from graph_creation.metadata_infile.onto.inMetaOntoDo import InMetaOntoDo



class OntoDoProcessor(FileProcessor):

    def __init__(self):
        self.use_cols =   InMetaOntoDo.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_ONTO_DO,
                         infileType=InfileType.IN_ONTO_DO, mapping_sep=InMetaOntoDo.MAPPING_SEP)