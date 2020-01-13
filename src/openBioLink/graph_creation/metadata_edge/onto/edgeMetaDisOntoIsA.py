import os

from openbiolink.graph_creation import graphCreationConfig as glob
from openbiolink.graph_creation.metadata_edge.edgeOntoMetadata import EdgeOntoMetadata
from openbiolink.graph_creation.metadata_infile.onto.inMetaOntoDoIsA import InMetaOntoDoIsA


class EdgeMetaDisOntoIsA(EdgeOntoMetadata):
    NAME = 'Onto - Disease_isA_Disease'

    EDGE_INMETA_CLASS = InMetaOntoDoIsA

    def __init__(self, quality=None):
        super().__init__(is_directional=True,
                         edges_file_path=os.path.join(glob.IN_FILE_PATH, self.EDGE_INMETA_CLASS.CSV_NAME),
                         colindex1=self.EDGE_INMETA_CLASS.NODE1_COL, colindex2=self.EDGE_INMETA_CLASS.NODE2_COL,
                         edgeType=self.EDGE_INMETA_CLASS.EDGE_TYPE,
                         node1_type=self.EDGE_INMETA_CLASS.NODE1_TYPE, node2_type=self.EDGE_INMETA_CLASS.NODE2_TYPE)
