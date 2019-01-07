from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.Types.readerType import ReaderType
from graph_creation.Types.infileType import InfileType
from graph_creation.metadata_infile.edge.inMetaEdgeHpoGene import InMetaEdgeHpoGene


class EdgeHpoGeneProcessor(FileProcessor):

    def __init__(self):
        self.use_cols = InMetaEdgeHpoGene.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_EDGE_HPO_GENE,
                         infileType=InfileType.IN_EDGE_HPO_GENE, mapping_sep=InMetaEdgeHpoGene.MAPPING_SEP)