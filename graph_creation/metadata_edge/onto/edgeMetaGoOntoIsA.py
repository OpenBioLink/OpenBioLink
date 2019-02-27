import os

import graph_creation.graphCreationConfig as glob
from graph_creation.metadata_edge.edgeOntoMetadata import EdgeOntoMetadata
from graph_creation.metadata_infile.onto.inMetaOntoGoIsA import InMetaOntoGoIsA


class EdgeMetaGoOntoIsA(EdgeOntoMetadata):
    EDGE_INMETA_CLASS = InMetaOntoGoIsA
    def __init__(self, quality = None):

        super().__init__(is_directional=True, edges_file_path=os.path.join (glob.IN_FILE_PATH, self.EDGE_INMETA_CLASS.CSV_NAME),
                         colindex1=self.EDGE_INMETA_CLASS.NODE1_COL, colindex2=self.EDGE_INMETA_CLASS.NODE2_COL,
                         edgeType=self.EDGE_INMETA_CLASS.EDGE_TYPE,
                         node1_type=self.EDGE_INMETA_CLASS.NODE1_TYPE, node2_type=self.EDGE_INMETA_CLASS.NODE2_TYPE)