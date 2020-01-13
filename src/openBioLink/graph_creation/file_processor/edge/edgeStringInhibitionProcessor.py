from openbiolink.graph_creation.file_processor.fileProcessor import FileProcessor
from openbiolink.graph_creation.metadata_infile import InMetaEdgeStringInhibition
from openbiolink.graph_creation.types.infileType import InfileType
from openbiolink.graph_creation.types.readerType import ReaderType


class EdgeStringInhibitionProcessor(FileProcessor):
    IN_META_CLASS = InMetaEdgeStringInhibition

    def __init__(self):
        self.use_cols = self.IN_META_CLASS.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_EDGE_STRING_ACTION,
                         infileType=InfileType.IN_EDGE_STRING_INHIBITION, mapping_sep=self.IN_META_CLASS.MAPPING_SEP)

    def individual_preprocessing(self, data):
        # inhibition is a directional link --> take only the directional cases where a is acting
        data = data[data['mode'] == 'inhibition']
        data = data[data['is_directional'] == 't']
        data = data[data['a_is_acting'] == 't']
        return data
