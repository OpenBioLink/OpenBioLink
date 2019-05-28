from ...types.infileType import InfileType
from ...types.readerType import ReaderType
from ..fileProcessor import FileProcessor
from ...metadata_infile import InMetaEdgeStringBindInh


class EdgeStringBindInhProcessor(FileProcessor):

    IN_META_CLASS = InMetaEdgeStringBindInh

    def __init__(self):
        self.use_cols = self.IN_META_CLASS.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_EDGE_STRING_ACTION,
                         infileType=InfileType.IN_EDGE_STRING_BINDINH, mapping_sep=self.IN_META_CLASS.MAPPING_SEP)


    def individual_preprocessing(self, data):
        #bindinh is a directional link --> take only the directional cases where a is acting
        data = data[data['action'] == 'inhibition']
        data = data[data['mode'] == 'binding']
        data = data[data['is_directional']=='t']
        data = data[data['a_is_acting'] =='t']
        return data