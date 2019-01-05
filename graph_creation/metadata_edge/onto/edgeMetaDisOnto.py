from graph_creation.metadata_edge.edgeMetadata import EdgeMetadata
from edgeType import EdgeType
from nodeType import NodeType
import os
import graph_creation.constants.globalConstant as glob
import graph_creation.constants.in_file.onto.inOntoDoConstant as edgeConst

class EdgeMetaDisOnto(EdgeMetadata):
    def __init__(self, quality = None):
        super().__init__(edges_file_path=os.path.join(glob.IN_FILE_PATH, edgeConst.CSV_NAME), #fixme csvname / path
                                      colindex1=0, colindex2=1, edgeType=EdgeType.IS_A,
                                      node1_type=NodeType.DIS, node2_type=NodeType.DIS)