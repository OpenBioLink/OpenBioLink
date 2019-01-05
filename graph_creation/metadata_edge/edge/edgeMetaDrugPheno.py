import os
import graph_creation.constants.globalConstant as glob

import graph_creation.constants.in_file.edge.inEdgeSiderSeConstant as edgeConst
import graph_creation.constants.in_file.mapping.inMapOntoHpoUmlsConstant as map2Const

import graph_creation.constants.edge_file.edge.edgeEdgeDrugPhenoConstant as const

from graph_creation.qualityType import QualityType

from graph_creation.metadata_edge.edgeMetadata import EdgeMetadata
from edgeType import EdgeType
from nodeType import NodeType

class EdgeMetaDrugPheno(EdgeMetadata):
    def __init__(self, quality : QualityType = None):
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
        mapping_file2 = os.path.join(glob.IN_FILE_PATH, map2Const.CSV_NAME)
        super().__init__(edges_file_path=edges_file_path,
                         colindex1=0, colindex2=1, edgeType=EdgeType.DRUG_PHENOTYPE,
                         node1_type=NodeType.DRUG, node2_type=NodeType.PHENOTYPE,
                         mapping2_file=mapping_file2, map2_sourceindex=1, map2_targetindex=0)
