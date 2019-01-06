from graph_creation.metadata_edge.edgeMetadata import EdgeMetadata
import os
import graph_creation.globalConstant as glob
from graph_creation.metadata_infile.onto.inMetaOntoDo import InMetaOntoDo

class EdgeMetaDisOnto(EdgeMetadata):
    def __init__(self, quality = None):
        super().__init__(edges_file_path=os.path.join(glob.IN_FILE_PATH, InMetaOntoDo.CSV_NAME), #fixme csvname / path
                         colindex1=InMetaOntoDo.NODE1_COL, colindex2=InMetaOntoDo.NODE2_COL,
                         edgeType=InMetaOntoDo.EDGE_TYPE,
                         node1_type=InMetaOntoDo.NODE1_TYPE, node2_type=InMetaOntoDo.NODE2_TYPE)