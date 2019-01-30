from graph_creation.Types.infileType import InfileType
from graph_creation.Types.readerType import ReaderType
from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.metadata_infile import InMetaEdgeStringCatalysis


class EdgeStringCatalysisProcessor(FileProcessor):

    META_EDGE_CLASS = InMetaEdgeStringCatalysis

    def __init__(self):
        self.use_cols = self.META_EDGE_CLASS.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_EDGE_STRING_ACTION,
                         infileType=InfileType.IN_EDGE_STRING_CATALYSIS, mapping_sep=self.META_EDGE_CLASS.MAPPING_SEP)


    def individual_preprocessing(self, data):
        #catalysis is a directional link --> take only the directional cases where a is acting
        data = data[data['mode'] == 'catalysis']
        data = data[data['is_directional']=='t']
        data = data[data['a_is_acting'] =='t']
        return data