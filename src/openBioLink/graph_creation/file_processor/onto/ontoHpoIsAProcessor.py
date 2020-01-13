from openbiolink.graph_creation.file_processor.fileProcessor import FileProcessor
from openbiolink.graph_creation.metadata_infile.onto.inMetaOntoHpoIsA import InMetaOntoHpoIsA
from openbiolink.graph_creation.types.infileType import InfileType
from openbiolink.graph_creation.types.readerType import ReaderType


class OntoHpoIsAProcessor(FileProcessor):
    IN_META_CLASS = InMetaOntoHpoIsA

    def __init__(self):
        self.use_cols = self.IN_META_CLASS.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_ONTO_HPO,
                         infileType=InfileType.IN_ONTO_HPO_IS_A, mapping_sep=self.IN_META_CLASS.MAPPING_SEP)
