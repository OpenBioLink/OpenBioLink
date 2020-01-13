from openbiolink.graph_creation.file_processor.fileProcessor import FileProcessor
from openbiolink.graph_creation.metadata_infile.mapping.inMetaMapOntoDoUmls import InMetaMapOntoDoUmls
from openbiolink.graph_creation.types.infileType import InfileType
from openbiolink.graph_creation.types.readerType import ReaderType


class OntoMapDoUmlsProcessor(FileProcessor):
    IN_META_CLASS = InMetaMapOntoDoUmls

    def __init__(self):
        self.use_cols = self.IN_META_CLASS.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_ONTO_DO,
                         infileType=InfileType.IN_MAP_ONTO_DO_UMLS, mapping_sep=self.IN_META_CLASS.MAPPING_SEP)
