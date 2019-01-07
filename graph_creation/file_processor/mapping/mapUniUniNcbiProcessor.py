from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.Types.readerType import ReaderType
from graph_creation.Types.infileType import InfileType
from graph_creation.metadata_infile.mapping.inMetaMapUniUniNcbi import InMetaMapUniUniNcbi



class MapUniUniNcbiProcessor(FileProcessor):

    def __init__(self):
        super().__init__(InMetaMapUniUniNcbi.USE_COLS, readerType=ReaderType.READER_MAP_UNIPROT,
                         infileType=InfileType.IN_MAP_UNI_UNI_NCBI, mapping_sep=InMetaMapUniUniNcbi.MAPPING_SEP)
