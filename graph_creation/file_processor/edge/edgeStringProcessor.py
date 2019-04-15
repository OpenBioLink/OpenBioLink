from profilehooks import profile

from graph_creation import utils
from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.types.readerType import ReaderType
from graph_creation.types.infileType import InfileType
from graph_creation.metadata_infile.edge.inMetaEdgeString import InMetaEdgeString



class EdgeStringProcessor(FileProcessor):
    IN_META_CLASS = InMetaEdgeString

    def __init__(self):
        self.use_cols = self.IN_META_CLASS.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_EDGE_STRING,
                         infileType=InfileType.IN_EDGE_STRING, mapping_sep=self.IN_META_CLASS.MAPPING_SEP)


    def individual_postprocessing(self, data):
        return utils.remove_bidir_edges_from_df(data)


