import os

import graph_creation.globalConstant as glob
from graph_creation.metadata_edge.edgeMetadata import EdgeMetadata
from graph_creation.metadata_infile import InMetaOntoUberon


class EdgeMetaAnatomyOnto(EdgeMetadata):
    def __init__(self, quality = None):
        self.EdgesMetaClass = InMetaOntoUberon

        super().__init__(is_directional=True, edges_file_path= os.path.join(glob.IN_FILE_PATH, self.EdgesMetaClass.CSV_NAME),
                         colindex1=self.EdgesMetaClass.NODE1_COL, colindex2=self.EdgesMetaClass.NODE2_COL,
                         edgeType=self.EdgesMetaClass.EDGE_TYPE,
                         node1_type=self.EdgesMetaClass.NODE1_TYPE, node2_type=self.EdgesMetaClass.NODE2_TYPE)