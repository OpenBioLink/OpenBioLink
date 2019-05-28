from ...file_processor.fileProcessor import FileProcessor
from ...types.readerType import ReaderType
from ...types.infileType import InfileType
from ...metadata_infile.onto.inMetaOntoHpoIsA import InMetaOntoHpoIsA



class OntoHpoIsAProcessor(FileProcessor):
    IN_META_CLASS = InMetaOntoHpoIsA

    def __init__(self):
        self.use_cols = self.IN_META_CLASS.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_ONTO_HPO,
                         infileType=InfileType.IN_ONTO_HPO_IS_A, mapping_sep=self.IN_META_CLASS.MAPPING_SEP)