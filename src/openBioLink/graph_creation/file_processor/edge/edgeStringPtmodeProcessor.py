import utils
from ...types.infileType import InfileType
from ...types.readerType import ReaderType
from ..fileProcessor import FileProcessor
from ...metadata_infile import InMetaEdgeStringPtmod


class EdgeStringPtmodeProcessor(FileProcessor):

    IN_META_CLASS = InMetaEdgeStringPtmod

    def __init__(self):
        self.use_cols = self.IN_META_CLASS.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_EDGE_STRING_ACTION,
                         infileType=InfileType.IN_EDGE_STRING_PTMOD, mapping_sep=self.IN_META_CLASS.MAPPING_SEP)


    def individual_preprocessing(self, data):
        #ptmod is an undirectional link --> take only the undirectional cases and only in one direction
        data = data[data['mode'] == 'ptmod']
        data = data[data['is_directional']=='f']
        return data

    def individual_postprocessing(self, data):
        return utils.make_undir(data)

