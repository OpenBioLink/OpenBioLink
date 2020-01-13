import os

from openbiolink.graph_creation import graphCreationConfig as glob
from openbiolink.graph_creation.metadata_edge.edgeRegularMetadata import EdgeRegularMetadata
from openbiolink.graph_creation.metadata_infile import InMetaEdgeStitchExpression
from openbiolink.graph_creation.metadata_infile.mapping.inMetaMapString import InMetaMapString
from openbiolink.graph_creation.types.qualityType import QualityType


class EdgeMetaDrugExpressionGene(EdgeRegularMetadata):
    NAME = 'Edge - Drug_expression_Gene'

    LQ_CUTOFF = 0
    MQ_CUTOFF = 400
    HQ_CUTOFF = 700

    EDGE_INMETA_CLASS = InMetaEdgeStitchExpression
    MAP2_META_CLASS = InMetaMapString

    def __init__(self, quality: QualityType = None):
        edges_file_path = os.path.join(glob.IN_FILE_PATH, self.EDGE_INMETA_CLASS.CSV_NAME)
        mapping_file2 = os.path.join(glob.IN_FILE_PATH, self.MAP2_META_CLASS.CSV_NAME)
        super().__init__(is_directional=True,
                         edges_file_path=edges_file_path,
                         colindex1=self.EDGE_INMETA_CLASS.NODE1_COL, colindex2=self.EDGE_INMETA_CLASS.NODE2_COL,
                         edgeType=self.EDGE_INMETA_CLASS.EDGE_TYPE,
                         node1_type=self.EDGE_INMETA_CLASS.NODE1_TYPE, node2_type=self.EDGE_INMETA_CLASS.NODE2_TYPE,
                         colindex_qscore=self.EDGE_INMETA_CLASS.QSCORE_COL, quality=quality,
                         mapping2_file=mapping_file2, map2_sourceindex=self.MAP2_META_CLASS.SOURCE_COL,
                         map2_targetindex=self.MAP2_META_CLASS.TARGET_COL)
