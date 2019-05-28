from ...file_processor.fileProcessor import FileProcessor
from ...types.readerType import ReaderType
from ...types.infileType import InfileType
from ...metadata_infile.mapping.inMetaMapUniEnsNcbi import InMetaMapUniEnsNcbi



class MapUniEnsNcbiProcessor(FileProcessor):
    IN_META_CLASS = InMetaMapUniEnsNcbi

    def __init__(self):
        super().__init__(self.IN_META_CLASS.USE_COLS, readerType=ReaderType.READER_MAP_UNIPROT,
                         infileType=InfileType.IN_MAP_UNI_ENS_NCBI, mapping_sep=self.IN_META_CLASS.MAPPING_SEP)
