from graph_creation.Types.infileType import InfileType
from graph_creation.Types.readerType import ReaderType
from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.metadata_infile import InMetaOntoUberonIsA, InMetaOntoUberonPartOf


class OntoUberonPartOfProcessor(FileProcessor):

    def __init__(self):
        self.MetaInfileClass = InMetaOntoUberonPartOf
        self.use_cols = self.MetaInfileClass.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_ONTO_UBERON,
                         infileType=InfileType.IN_ONTO_UBERON_PART_OF, mapping_sep=self.MetaInfileClass.MAPPING_SEP)


    def individual_postprocessing(self, data):
        # bgee is only mapping on CL and UBERON terms
        data = data[data['ID'].str.startswith('UBERON:') | data['ID'].str.startswith('CL:') ]
        data = data[data['PART_OF'].str.startswith('UBERON:') | data['PART_OF'].str.startswith('CL:') ]
        return data