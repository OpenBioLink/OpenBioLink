from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.Types.readerType import ReaderType
from graph_creation.Types.infileType import InfileType
from graph_creation.metadata_infile.mapping.inMetaMapOntoDoUmls import InMetaMapOntoDoUmls



class OntoMapDoUmlsProcessor(FileProcessor):

    def __init__(self):
        self.use_cols =  InMetaMapOntoDoUmls.USE_COLS
        super().__init__(self.use_cols, dbType=DbType.DB_ONTO_DO,
                         infileType=InfileType.IN_MAP_ONTO_DO_UMLS, mapping_sep=InMetaMapOntoDoUmls.MAPPING_SEP)