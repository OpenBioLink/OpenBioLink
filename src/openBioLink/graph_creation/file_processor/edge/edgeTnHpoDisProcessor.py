from ..fileProcessor import FileProcessor
from ...types.readerType import ReaderType
from ...types.infileType import InfileType
from ...metadata_infile import InMetaEdgeTnHpoDis


class EdgeTnHpoDisProcessor(FileProcessor):
    IN_META_CLASS = InMetaEdgeTnHpoDis

    def __init__(self):
        self.use_cols = self.IN_META_CLASS.USE_COLS
        super().__init__( self.use_cols, readerType=ReaderType.READER_EDGE_TN_HPO_DIS,
                          infileType=InfileType.IN_EDGE_TN_HPO_DIS, mapping_sep=self.IN_META_CLASS.MAPPING_SEP)