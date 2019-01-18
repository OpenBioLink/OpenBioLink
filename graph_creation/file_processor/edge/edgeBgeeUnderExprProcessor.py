from graph_creation.Types.infileType import InfileType
from graph_creation.Types.readerType import ReaderType
from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.metadata_infile.edge.inMetaEdgeBgeeUnderExpr import InMetaEdgeBgeeUnderExpr


class EdgeBgeeUnderExprProcessor(FileProcessor):

    def __init__(self):
        self.MetaInfileClass = InMetaEdgeBgeeUnderExpr
        self.use_cols =   self.MetaInfileClass.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_EDGE_BGEE_DIFF,
                         infileType=InfileType.IN_EDGE_BGEE_UNDEREXPR, mapping_sep= self.MetaInfileClass.MAPPING_SEP)

    def individual_preprocessing(self, data):
        data = data[data.differential_expr == 'under-expression']
        return data