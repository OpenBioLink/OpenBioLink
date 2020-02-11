from openbiolink.edgeType import EdgeType
from openbiolink.graph_creation.metadata_infile.infileMetadata import InfileMetadata
from openbiolink.graph_creation.types.infileType import InfileType
from openbiolink.namespace import *
from openbiolink.nodeType import NodeType


class InMetaEdgeStitchPredBind(InfileMetadata):
    CSV_NAME = "DB_STITCH_drug_PredBind_gene.csv"
    USE_COLS = ["item_id_a", "item_id_b", "score"]
    NODE1_COL = 0
    NODE2_COL = 1
    QSCORE_COL = 2
    SOURCE = "STITCH"
    NODE1_TYPE = NodeType.DRUG
    NODE1_NAMESPACE = Namespace(Namespaces.PUBCHEM, False)
    NODE2_TYPE = NodeType.GENE
    NODE2_NAMESPACE = Namespace(Namespaces.ENSEMBL, False, mapping={"9606.": ""})
    EDGE_TYPE = EdgeType.DRUG_PREDBIND_GENE
    INFILE_TYPE = InfileType.IN_EDGE_STITCH_PREDBIND

    MAPPING_SEP = None

    def __init__(self):
        super().__init__(
            csv_name=InMetaEdgeStitchPredBind.CSV_NAME,
            cols=self.USE_COLS,
            infileType=InMetaEdgeStitchPredBind.INFILE_TYPE,
        )
