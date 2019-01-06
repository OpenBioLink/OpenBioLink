from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.dbType import DbType
from graph_creation.infileType import InfileType
from graph_creation.metadata_infile.edge.inMetaEdgeHpoGene import InMetaEdgeHpoGene


class EdgeHpoGeneProcessor(FileProcessor):

    def __init__(self):
        self.use_cols = InMetaEdgeHpoGene.USE_COLS
        super().__init__(self.use_cols, dbType=DbType.DB_EDGE_HPO_GENE,
                         infileType=InfileType.IN_EDGE_HPO_GENE, mapping_sep=InMetaEdgeHpoGene.MAPPING_SEP)