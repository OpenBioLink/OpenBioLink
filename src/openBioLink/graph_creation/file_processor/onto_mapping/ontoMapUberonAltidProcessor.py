from openbiolink.graph_creation.file_processor.fileProcessor import FileProcessor
from openbiolink.graph_creation.metadata_infile.mapping.inMetaMapOntoUberonAltid import InMetaMapOntoUberonAltid
from openbiolink.graph_creation.types.infileType import InfileType
from openbiolink.graph_creation.types.readerType import ReaderType


class OntoMapUberonAltidProcessor(FileProcessor):
    IN_META_CLASS = InMetaMapOntoUberonAltid

    def __init__(self):
        self.use_cols = self.IN_META_CLASS.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_ONTO_UBERON,
                         infileType=InfileType.IN_MAP_ONTO_UBERON_ALT_ID, mapping_sep=self.IN_META_CLASS.MAPPING_SEP)
