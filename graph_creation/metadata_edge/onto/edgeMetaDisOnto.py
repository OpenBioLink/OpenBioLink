from graph_creation.metadata_edge.edgeMetadata import EdgeMetadata
import os
import graph_creation.globalConstant as glob
from graph_creation.metadata_infile.onto.inMetaOntoDo import InMetaOntoDo

class EdgeMetaDisOnto(EdgeMetadata):
    def __init__(self, quality = None):
        self.ontoMetaClass = InMetaOntoDo
        super().__init__(edges_file_path=os.path.join(glob.IN_FILE_PATH, self.ontoMetaClass.CSV_NAME), #fixme csvname / path
                         colindex1=self.ontoMetaClass.NODE1_COL, colindex2=self.ontoMetaClass.NODE2_COL,
                         edgeType=self.ontoMetaClass.EDGE_TYPE,
                         node1_type=self.ontoMetaClass.NODE1_TYPE, node2_type=self.ontoMetaClass.NODE2_TYPE)