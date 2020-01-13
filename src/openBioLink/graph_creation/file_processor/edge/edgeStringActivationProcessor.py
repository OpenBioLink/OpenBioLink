from openbiolink.graph_creation.file_processor.fileProcessor import FileProcessor
from openbiolink.graph_creation.metadata_infile import InMetaEdgeStringActivation
from openbiolink.graph_creation.types.infileType import InfileType
from openbiolink.graph_creation.types.readerType import ReaderType


class EdgeStringActivationProcessor(FileProcessor):
    IN_META_CLASS = InMetaEdgeStringActivation

    def __init__(self):
        self.use_cols = self.IN_META_CLASS.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_EDGE_STRING_ACTION,
                         infileType=InfileType.IN_EDGE_STRING_ACTIVATION, mapping_sep=self.IN_META_CLASS.MAPPING_SEP)

    def individual_preprocessing(self, data):
        # activation is a directional link --> take only the directional cases where a is acting
        data = data[data['mode'] == 'activation']
        data = data[data['is_directional'] == 't']
        data = data[data['a_is_acting'] == 't']
        return data
