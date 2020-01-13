from openbiolink.graph_creation.file_processor.fileProcessor import FileProcessor
from openbiolink.graph_creation.metadata_infile.mapping.inMetaMapUniEnsNcbi import InMetaMapUniEnsNcbi
from openbiolink.graph_creation.types.infileType import InfileType
from openbiolink.graph_creation.types.readerType import ReaderType


class MapUniEnsNcbiProcessor(FileProcessor):
    IN_META_CLASS = InMetaMapUniEnsNcbi

    def __init__(self):
        super().__init__(self.IN_META_CLASS.USE_COLS, readerType=ReaderType.READER_MAP_UNIPROT,
                         infileType=InfileType.IN_MAP_UNI_ENS_NCBI, mapping_sep=self.IN_META_CLASS.MAPPING_SEP)
