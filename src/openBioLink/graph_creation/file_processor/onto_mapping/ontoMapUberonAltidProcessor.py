from ...file_processor.fileProcessor import FileProcessor
from ...metadata_infile.mapping.inMetaMapOntoUberonAltid import InMetaMapOntoUberonAltid
from ...types.infileType import InfileType
from ...types.readerType import ReaderType


class OntoMapUberonAltidProcessor(FileProcessor):
    IN_META_CLASS = InMetaMapOntoUberonAltid

    def __init__(self):
        self.use_cols =  self.IN_META_CLASS.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_ONTO_UBERON,
                         infileType=InfileType.IN_MAP_ONTO_UBERON_ALT_ID, mapping_sep=self.IN_META_CLASS.MAPPING_SEP)