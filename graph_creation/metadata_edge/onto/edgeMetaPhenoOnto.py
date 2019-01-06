from graph_creation.metadata_edge.edgeMetadata import EdgeMetadata
import os
import graph_creation.globalConstant as glob
from graph_creation.metadata_infile.onto.inMetaOntoHpo import InMetaOntoHpo

class EdgeMetaPhenoOnto(EdgeMetadata):
    def __init__(self, quality = None):
        super().__init__(edges_file_path= os.path.join(glob.IN_FILE_PATH, InMetaOntoHpo.CSV_NAME),
                         colindex1=InMetaOntoHpo.NODE1_COL, colindex2=InMetaOntoHpo.NODE2_COL,
                         edgeType=InMetaOntoHpo.EDGE_TYPE,
                         node1_type=InMetaOntoHpo.NODE1_TYPE, node2_type=InMetaOntoHpo.NODE2_TYPE)