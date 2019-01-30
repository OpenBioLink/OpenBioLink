from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.Types.readerType import ReaderType
from graph_creation.Types.infileType import InfileType
from graph_creation.metadata_infile.mapping.inMetaMapOntoHpoAltid import InMetaMapOntoHpoAltid



class OntoMapHpoAltidProcessor(FileProcessor):

    def __init__(self):
        self.use_cols =       InMetaMapOntoHpoAltid.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_ONTO_HPO,
                         infileType=InfileType.IN_MAP_ONTO_HPO_ALT_ID, mapping_sep=InMetaMapOntoHpoAltid.MAPPING_SEP)