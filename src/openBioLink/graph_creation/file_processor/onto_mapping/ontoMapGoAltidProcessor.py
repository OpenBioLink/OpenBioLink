from openbiolink.graph_creation.file_processor.fileProcessor import FileProcessor
from openbiolink.graph_creation.metadata_infile.mapping.inMetaMapOntoGoAltid import InMetaMapOntoGoAltid
from openbiolink.graph_creation.types.infileType import InfileType
from openbiolink.graph_creation.types.readerType import ReaderType


class OntoMapGoAltidProcessor(FileProcessor):
    IN_META_CLASS = InMetaMapOntoGoAltid

    def __init__(self):
        self.use_cols = self.IN_META_CLASS.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_ONTO_GO,
                         infileType=InfileType.IN_MAP_ONTO_GO_ALT_ID, mapping_sep=self.IN_META_CLASS.MAPPING_SEP)
