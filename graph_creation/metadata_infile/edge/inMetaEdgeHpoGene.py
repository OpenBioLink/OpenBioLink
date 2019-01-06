from edgeType import EdgeType
from graph_creation.infileType import InfileType
from graph_creation.metadata_infile.infileMetadata import InfileMetadata
from nodeType import NodeType


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

    def __init__(self, folder_path):
        super().__init__(csv_name=InMetaEdgeHpoGene.CSV_NAME,
                         folder_path=folder_path,
                         infileType=InMetaEdgeHpoGene.INFILE_TYPE)
