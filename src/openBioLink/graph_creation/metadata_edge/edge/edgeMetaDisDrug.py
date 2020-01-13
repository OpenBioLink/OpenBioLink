import os

from openbiolink.graph_creation import graphCreationConfig as glob
from openbiolink.graph_creation.metadata_edge.edgeRegularMetadata import EdgeRegularMetadata
from openbiolink.graph_creation.metadata_infile import InMetaMapOntoDoAltid
from openbiolink.graph_creation.metadata_infile.edge.inMetaEdgeDrugCentral import InMetaEdgeDrugCentral
from openbiolink.graph_creation.metadata_infile.mapping.inMetaMapDisGeNet import InMetaMapDisGeNet
from openbiolink.graph_creation.metadata_infile.mapping.inMetaMapDrugCentralPubchem import InMetaMapDrugCentralPubchem
from openbiolink.graph_creation.types.qualityType import QualityType


class EdgeMetaDisDrug(EdgeRegularMetadata):
    NAME = 'Edge - Disease_treatedWith_Drug (Indication)'
    EDGE_INMETA_CLASS = InMetaEdgeDrugCentral
    MAP1_META_CLASS = InMetaMapDisGeNet
    MAP2_META_CLASS = InMetaMapDrugCentralPubchem
    MAP1_ALT_ID_META_CLASS = InMetaMapOntoDoAltid

    def __init__(self, quality: QualityType = None):
        edges_file_path = os.path.join(glob.IN_FILE_PATH, self.EDGE_INMETA_CLASS.CSV_NAME)
        mapping_file1 = os.path.join(glob.IN_FILE_PATH, self.MAP1_META_CLASS.CSV_NAME)
        altid_mapping_file1 = os.path.join(glob.IN_FILE_PATH, self.MAP1_ALT_ID_META_CLASS.CSV_NAME)
        mapping_file2 = os.path.join(glob.IN_FILE_PATH, self.MAP2_META_CLASS.CSV_NAME)

        super().__init__(is_directional=True,
                         edges_file_path=edges_file_path,
                         colindex1=self.EDGE_INMETA_CLASS.NODE1_COL, colindex2=self.EDGE_INMETA_CLASS.NODE2_COL,
                         edgeType=self.EDGE_INMETA_CLASS.EDGE_TYPE,
                         node1_type=self.EDGE_INMETA_CLASS.NODE1_TYPE, node2_type=self.EDGE_INMETA_CLASS.NODE2_TYPE,
                         colindex_qscore=self.EDGE_INMETA_CLASS.QSCORE_COL,
                         mapping1_file=mapping_file1,
                         map1_sourceindex=self.MAP1_META_CLASS.SOURCE_COL,
                         map1_targetindex=self.MAP1_META_CLASS.TARGET_COL,
                         altid_mapping1_file=altid_mapping_file1,
                         altid_map1_sourceindex=self.MAP1_ALT_ID_META_CLASS.SOURCE_COL,
                         altid_map1_targetindex=self.MAP1_ALT_ID_META_CLASS.TARGET_COL,
                         mapping2_file=mapping_file2,
                         map2_sourceindex=self.MAP2_META_CLASS.SOURCE_COL,
                         map2_targetindex=self.MAP2_META_CLASS.TARGET_COL
                         )
