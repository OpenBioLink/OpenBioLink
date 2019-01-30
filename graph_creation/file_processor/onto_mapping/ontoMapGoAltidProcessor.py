from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.Types.readerType import ReaderType
from graph_creation.Types.infileType import InfileType
from graph_creation.metadata_infile.mapping.inMetaMapOntoGoAltid import InMetaMapOntoGoAltid



class OntoMapGoAltidProcessor(FileProcessor):

    def __init__(self):
        self.use_cols =       InMetaMapOntoGoAltid.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_ONTO_GO,
                         infileType=InfileType.IN_MAP_ONTO_GO_ALT_ID, mapping_sep=InMetaMapOntoGoAltid.MAPPING_SEP)