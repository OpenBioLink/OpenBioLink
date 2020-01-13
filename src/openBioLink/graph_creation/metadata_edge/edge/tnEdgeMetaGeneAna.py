import os

from openbiolink.graph_creation import graphCreationConfig as glob
from openbiolink.graph_creation.metadata_edge.edge.edgeMetaGeneAna import EdgeMetaGeneAna
from openbiolink.graph_creation.metadata_edge.tnEdgeRegularMetadata import TnEdgeRegularMetadata
from openbiolink.graph_creation.metadata_infile import InMetaMapOntoUberonAltid
from openbiolink.graph_creation.metadata_infile.edge.inMetaEdgeBgeeNoExpr import InMetaEdgeBgeeNoExpr
from openbiolink.graph_creation.metadata_infile.mapping.inMetaMapUniEnsNcbi import InMetaMapUniEnsNcbi
from openbiolink.graph_creation.types.qualityType import QualityType


class TnEdgeMetaGeneAna(TnEdgeRegularMetadata):
    NAME = 'Negative Edge - Gene_expression_Anatomy'

    LQ_CUTOFF_TEXT = None
    MQ_CUTOFF_TEXT = None
    HQ_CUTOFF_TEXT = ['silver quality']

    EDGE_INMETA_CLASS = InMetaEdgeBgeeNoExpr
    TP_EDGE_CLASS = EdgeMetaGeneAna
    MAP1_META_CLASS = InMetaMapUniEnsNcbi
    MAP2_ALT_ID_META_CLASS = InMetaMapOntoUberonAltid

    def __init__(self, quality: QualityType = None):
        edges_file_path = os.path.join(glob.IN_FILE_PATH, self.EDGE_INMETA_CLASS.CSV_NAME)
        mapping_file1 = os.path.join(glob.IN_FILE_PATH, self.MAP1_META_CLASS.CSV_NAME)
        altid_mapping2_file = os.path.join(glob.IN_FILE_PATH, self.MAP2_ALT_ID_META_CLASS.CSV_NAME)
        super().__init__(is_directional=True,
                         edges_file_path=edges_file_path,
                         colindex1=self.EDGE_INMETA_CLASS.NODE1_COL,
                         colindex2=self.EDGE_INMETA_CLASS.NODE2_COL,
                         edgeType=self.TP_EDGE_CLASS.EDGE_INMETA_CLASS.EDGE_TYPE,
                         node1_type=self.EDGE_INMETA_CLASS.NODE1_TYPE,
                         node2_type=self.EDGE_INMETA_CLASS.NODE2_TYPE,
                         colindex_qscore=self.EDGE_INMETA_CLASS.QSCORE_COL,
                         quality=quality,
                         mapping1_file=mapping_file1,
                         map1_sourceindex=self.MAP1_META_CLASS.SOURCE_COL,
                         map1_targetindex=self.MAP1_META_CLASS.TARGET_COL,
                         altid_mapping2_file=altid_mapping2_file,
                         altid_map2_sourceindex=self.MAP2_ALT_ID_META_CLASS.SOURCE_COL,
                         altid_map2_targetindex=self.MAP2_ALT_ID_META_CLASS.TARGET_COL
                         )
