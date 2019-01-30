import os

import graph_creation.globalConstant as glob
from graph_creation.Types.qualityType import QualityType
from graph_creation.metadata_edge.edgeMetadata import EdgeMetadata
from graph_creation.metadata_infile import InMetaEdgeBgeeOverExpr
from graph_creation.metadata_infile.edge.inMetaEdgeBgeeExpr import InMetaEdgeBgeeExpr
from graph_creation.metadata_infile.mapping.inMetaMapUniEnsNcbi import InMetaMapUniEnsNcbi


class EdgeMetaGeneOverAna(EdgeMetadata):
    LQ_CUTOFF = None
    MQ_CUTOFF = None
    HQ_CUTOFF = None
    LQ_CUTOFF_TEXT = 'low quality'
    MQ_CUTOFF_TEXT = 'low quality'
    HQ_CUTOFF_TEXT = 'high quality'
    def __init__(self, quality : QualityType= None):
        if quality is QualityType.HQ:
            cutoff_txt = EdgeMetaGeneOverAna.HQ_CUTOFF_TEXT
            cutoff_num = EdgeMetaGeneOverAna.HQ_CUTOFF
        elif quality is QualityType.MQ:
            cutoff_txt = EdgeMetaGeneOverAna.MQ_CUTOFF_TEXT
            cutoff_num = EdgeMetaGeneOverAna.MQ_CUTOFF
        elif quality is QualityType.LQ:
            cutoff_txt = EdgeMetaGeneOverAna.LQ_CUTOFF_TEXT
            cutoff_num = EdgeMetaGeneOverAna.LQ_CUTOFF
        else:
            cutoff_txt = None
            cutoff_num = None

        self.EdgesMetaClass = InMetaEdgeBgeeOverExpr
        self.Map1MetaClass = InMetaMapUniEnsNcbi
        self.Map2MetaClass = None

        edges_file_path = os.path.join(glob.IN_FILE_PATH, self.EdgesMetaClass.CSV_NAME)
        mapping_file1 = os.path.join(glob.IN_FILE_PATH, self.Map1MetaClass.CSV_NAME)
        super().__init__(is_directional=True,
                         edges_file_path=edges_file_path,
                         colindex1=self.EdgesMetaClass.NODE1_COL, colindex2=self.EdgesMetaClass.NODE2_COL,
                         edgeType=self.EdgesMetaClass.EDGE_TYPE,
                         node1_type=self.EdgesMetaClass.NODE1_TYPE, node2_type=self.EdgesMetaClass.NODE2_TYPE,
                         colindex_qscore=self.EdgesMetaClass.QSCORE_COL,
                         mapping1_file=mapping_file1, map1_sourceindex=self.Map1MetaClass.SOURCE_COL, map1_targetindex=self.Map1MetaClass.TARGET_COL)