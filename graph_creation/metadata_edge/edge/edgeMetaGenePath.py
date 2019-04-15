import os

import graph_creation.graphCreationConfig as glob
from graph_creation.types.qualityType import QualityType
from graph_creation.metadata_edge.edgeRegularMetadata import EdgeRegularMetadata
from graph_creation.metadata_infile.edge.inMetaEdgeCdtPath import InMetaEdgeCdtPath


class EdgeMetaGenePath(EdgeRegularMetadata):

    EDGE_INMETA_CLASS = InMetaEdgeCdtPath

    def __init__(self, quality : QualityType):

        edges_file_path = os.path.join(glob.IN_FILE_PATH, self.EDGE_INMETA_CLASS.CSV_NAME)
        super().__init__(is_directional=True,
                         edges_file_path=edges_file_path,
                         colindex1=self.EDGE_INMETA_CLASS.NODE1_COL, colindex2=self.EDGE_INMETA_CLASS.NODE2_COL,
                         edgeType=self.EDGE_INMETA_CLASS.EDGE_TYPE,
                         node1_type=self.EDGE_INMETA_CLASS.NODE1_TYPE, node2_type=self.EDGE_INMETA_CLASS.NODE2_TYPE,
                         colindex_qscore=self.EDGE_INMETA_CLASS.QSCORE_COL)
