from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.Types.readerType import ReaderType
from graph_creation.Types.infileType import InfileType
from graph_creation.metadata_infile.mapping.inMetaMapUniEnsNcbi import InMetaMapUniEnsNcbi



class MapUniEnsNcbiProcessor(FileProcessor):

    def __init__(self):
        super().__init__(InMetaMapUniEnsNcbi.USE_COLS, readerType=ReaderType.READER_MAP_UNIPROT,
                         infileType=InfileType.IN_MAP_UNI_ENS_NCBI, mapping_sep=InMetaMapUniEnsNcbi.MAPPING_SEP)
