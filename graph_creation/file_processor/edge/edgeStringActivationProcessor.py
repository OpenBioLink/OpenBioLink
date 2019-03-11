from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.Types.readerType import ReaderType
from graph_creation.Types.infileType import InfileType
from graph_creation.metadata_infile import InMetaEdgeStringActivation
from graph_creation.metadata_infile.edge.inMetaEdgeStitchActivation import InMetaEdgeStitchActivation


class EdgeStringActivationProcessor(FileProcessor):

    IN_META_CLASS = InMetaEdgeStringActivation

    def __init__(self):
        self.use_cols = self.IN_META_CLASS.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_EDGE_STRING_ACTION,
                         infileType=InfileType.IN_EDGE_STRING_ACTIVATION, mapping_sep=self.IN_META_CLASS.MAPPING_SEP)


    def individual_preprocessing(self, data):
        #activation is a directional link --> take only the directional cases where a is acting
        data = data[data['mode'] == 'activation']
        data = data[data['is_directional']=='t']
        data = data[data['a_is_acting'] =='t']
        return data