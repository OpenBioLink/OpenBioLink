import os

import graph_creation.globalConstant as glob
from graph_creation.Types.qualityType import QualityType
from graph_creation.metadata_edge.edge.edgeMetaGeneOverAna import EdgeMetaGeneOverAna
from graph_creation.metadata_edge.tnEdgeRegularMetadata import TnEdgeRegularMetadata
from graph_creation.metadata_infile import InMetaEdgeBgeeUnderExpr
from graph_creation.metadata_infile.mapping.inMetaMapUniEnsNcbi import InMetaMapUniEnsNcbi


class TnEdgeMetaGeneOverAna(TnEdgeRegularMetadata):

    LQ_CUTOFF_TEXT = 'low quality'
    MQ_CUTOFF_TEXT = 'low quality'
    HQ_CUTOFF_TEXT = 'high quality'

    EDGE_INMETA_CLASS = InMetaEdgeBgeeUnderExpr
    TP_EDGE_CLASS = EdgeMetaGeneOverAna
    MAP1_META_CLASS = InMetaMapUniEnsNcbi

    def __init__(self, quality : QualityType= None):

        edges_file_path = os.path.join(glob.IN_FILE_PATH, self.EDGE_INMETA_CLASS.CSV_NAME)
        mapping_file1 = os.path.join(glob.IN_FILE_PATH, self.MAP1_META_CLASS.CSV_NAME)
        super().__init__(is_directional=True,
                         edges_file_path=edges_file_path,
                         colindex1=self.EDGE_INMETA_CLASS.NODE1_COL, colindex2=self.EDGE_INMETA_CLASS.NODE2_COL,
                         edgeType=self.TP_EDGE_CLASS.EDGE_INMETA_CLASS.EDGE_TYPE,
                         node1_type=self.EDGE_INMETA_CLASS.NODE1_TYPE, node2_type=self.EDGE_INMETA_CLASS.NODE2_TYPE,
                         colindex_qscore=self.EDGE_INMETA_CLASS.QSCORE_COL, quality=quality,
                         mapping1_file=mapping_file1, map1_sourceindex=self.MAP1_META_CLASS.SOURCE_COL, map1_targetindex=self.MAP1_META_CLASS.TARGET_COL)