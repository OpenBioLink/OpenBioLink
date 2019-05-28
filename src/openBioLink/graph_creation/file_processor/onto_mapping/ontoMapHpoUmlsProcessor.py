from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.types.readerType import ReaderType
from graph_creation.types.infileType import InfileType
from graph_creation.metadata_infile.mapping.inMetaMapOntoHpoUmls import InMetaMapOntoHpoUmls


class OntoMapHpoUmlsProcessor(FileProcessor):
    IN_META_CLASS = InMetaMapOntoHpoUmls

    def __init__(self):
        self.use_cols =   self.IN_META_CLASS.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_ONTO_HPO,
                         infileType=InfileType.IN_MAP_ONTO_HPO_UMLS, mapping_sep= self.IN_META_CLASS.MAPPING_SEP)