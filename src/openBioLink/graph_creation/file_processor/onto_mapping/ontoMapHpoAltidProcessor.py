from openbiolink.graph_creation.file_processor.fileProcessor import FileProcessor
from openbiolink.graph_creation.metadata_infile.mapping.inMetaMapOntoHpoAltid import InMetaMapOntoHpoAltid
from openbiolink.graph_creation.types.infileType import InfileType
from openbiolink.graph_creation.types.readerType import ReaderType


class OntoMapHpoAltidProcessor(FileProcessor):
    IN_META_CLASS = InMetaMapOntoHpoAltid

    def __init__(self):
        self.use_cols = self.IN_META_CLASS.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_ONTO_HPO,
                         infileType=InfileType.IN_MAP_ONTO_HPO_ALT_ID, mapping_sep=self.IN_META_CLASS.MAPPING_SEP)
