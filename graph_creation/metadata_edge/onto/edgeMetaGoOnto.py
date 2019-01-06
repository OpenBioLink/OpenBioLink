from graph_creation.metadata_edge.edgeMetadata import EdgeMetadata
import os
import graph_creation.globalConstant as glob
from graph_creation.metadata_infile.onto.inMetaOntoGo import InMetaOntoGo

class EdgeMetaGoOnto(EdgeMetadata, ):
    def __init__(self, quality = None):
        super().__init__(edges_file_path=os.path.join (glob.IN_FILE_PATH, InMetaOntoGo.CSV_NAME),
                         colindex1=InMetaOntoGo.NODE1_COL, colindex2=InMetaOntoGo.NODE2_COL,
                         edgeType=InMetaOntoGo.EDGE_TYPE,
                         node1_type=InMetaOntoGo.NODE1_TYPE, node2_type=InMetaOntoGo.NODE2_TYPE)