import utils
from ..fileProcessor import FileProcessor
from ...metadata_infile.edge.inMetaEdgeString import InMetaEdgeString
from ...types.infileType import InfileType
from ...types.readerType import ReaderType


class EdgeStringProcessor(FileProcessor):
    IN_META_CLASS = InMetaEdgeString

    def __init__(self):
        self.use_cols = self.IN_META_CLASS.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_EDGE_STRING,
                         infileType=InfileType.IN_EDGE_STRING, mapping_sep=self.IN_META_CLASS.MAPPING_SEP)


    def individual_postprocessing(self, data):
        return utils.remove_bidir_edges_from_df(data)


