from ...types.infileType import InfileType
from ...types.readerType import ReaderType
from ...file_processor.fileProcessor import FileProcessor
from ...metadata_infile import InMetaOntoUberonIsA


class OntoUberonIsAProcessor(FileProcessor):
    IN_META_CLASS = InMetaOntoUberonIsA

    def __init__(self):
        self.use_cols = self.IN_META_CLASS.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_ONTO_UBERON,
                         infileType=InfileType.IN_ONTO_UBERON_IS_A, mapping_sep=self.IN_META_CLASS.MAPPING_SEP)


    def individual_postprocessing(self, data):
        # bgee is only mapping on CL and UBERON terms
        data = data[data['ID'].str.startswith('UBERON:') | data['ID'].str.startswith('CL:') ]
        data = data[data['IS_A'].str.startswith('UBERON:') | data['IS_A'].str.startswith('CL:') ]
        return data