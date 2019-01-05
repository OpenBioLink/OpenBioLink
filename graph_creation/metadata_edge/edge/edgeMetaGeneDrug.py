import os
import graph_creation.constants.globalConstant as glob

import graph_creation.constants.in_file.edge.inEdgeStitchConstant as edgeConst
import graph_creation.constants.in_file.mapping.inMapStringConstant as map1Const
import graph_creation.constants.edge_file.edge.edgeEdgeGeneDrugConstant as const

from graph_creation.qualityType import QualityType

from graph_creation.metadata_edge.edgeMetadata import EdgeMetadata
from edgeType import EdgeType
from nodeType import NodeType

class EdgeMetaGeneDrug(EdgeMetadata):
    def __init__(self, quality : QualityType= None):
        if quality is QualityType.HQ:
            cutoff_txt = const.HQ_CUTOFF_TEXT
            cutoff_num = const.HQ_CUTOFF
        elif quality is QualityType.MQ:
            cutoff_txt = const.MQ_CUTOFF_TEXT
            cutoff_num = const.MQ_CUTOFF
        elif quality is QualityType.LQ:
            cutoff_txt = const.LQ_CUTOFF_TEXT
            cutoff_num = const.LQ_CUTOFF
        else:
            cutoff_txt = None
            cutoff_num = None

        edges_file_path = os.path.join(glob.IN_FILE_PATH, edgeConst.CSV_NAME)
        mapping_file1 = os.path.join(glob.IN_FILE_PATH, map1Const.CSV_NAME)
        super().__init__(edges_file_path=edges_file_path,
                         colindex1=0, colindex2=1, edgeType=EdgeType.GENE_DRUG,
                         node1_type=NodeType.GENE, node2_type=NodeType.DRUG,
                         colindex_qscore=2, cutoff_num=cutoff_num, cutoff_txt=cutoff_txt,
                         mapping1_file=mapping_file1, map1_sourceindex=1, map1_targetindex=0)
