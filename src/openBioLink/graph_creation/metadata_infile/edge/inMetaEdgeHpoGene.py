from openbiolink.edgeType import EdgeType
from openbiolink.graph_creation.metadata_infile.infileMetadata import InfileMetadata
from openbiolink.graph_creation.types.infileType import InfileType
from openbiolink.nodeType import NodeType


class InMetaEdgeHpoGene(InfileMetadata):
    CSV_NAME = "DB_HPO_gene_phenotype.csv"
    USE_COLS = ['geneID', 'hpoID']
    NODE1_COL = 0
    NODE2_COL = 1
    QSCORE_COL = None
    NODE1_TYPE = NodeType.GENE
    NODE2_TYPE = NodeType.PHENOTYPE
    EDGE_TYPE = EdgeType.GENE_PHENOTYPE
    INFILE_TYPE = InfileType.IN_EDGE_HPO_GENE

    MAPPING_SEP = None

    def __init__(self):
        super().__init__(csv_name=InMetaEdgeHpoGene.CSV_NAME,
                         cols=self.USE_COLS,
                         infileType=InMetaEdgeHpoGene.INFILE_TYPE)
