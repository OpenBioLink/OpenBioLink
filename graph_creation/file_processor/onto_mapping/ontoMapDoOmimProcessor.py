from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.Types.readerType import ReaderType
from graph_creation.Types.infileType import InfileType
from graph_creation.metadata_infile.mapping.inMetaMapOntoDoOmim import InMetaMapOntoDoOmim



class OntoMapDoUmlsProcessor(FileProcessor):

    def __init__(self):
        self.use_cols =       InMetaMapOntoDoOmim.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_ONTO_DO,
                         infileType=InfileType.IN_MAP_ONTO_DO_OMIM, mapping_sep=InMetaMapOntoDoOmim.MAPPING_SEP)