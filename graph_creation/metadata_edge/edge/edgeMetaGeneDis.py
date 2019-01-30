import os
import graph_creation.globalConstant as glob
from graph_creation.metadata_infile import InMetaMapOntoDoAltid

from graph_creation.metadata_infile.edge.inMetaEdgeDisGeNet import InMetaEdgeDisGeNet
from graph_creation.metadata_infile.mapping.inMetaMapDisGeNet import InMetaMapDisGeNet

from graph_creation.Types.qualityType import QualityType

from graph_creation.metadata_edge.edgeMetadata import EdgeMetadata
from edgeType import EdgeType


class EdgeMetaGeneDis(EdgeMetadata):
    LQ_CUTOFF = 0
    MQ_CUTOFF = 0
    HQ_CUTOFF = 0.7
    LQ_CUTOFF_TEXT = None
    MQ_CUTOFF_TEXT = None
    HQ_CUTOFF_TEXT = None

    def __init__(self, quality : QualityType= None):
        if quality is QualityType.HQ:
            cutoff_txt = EdgeMetaGeneDis.HQ_CUTOFF_TEXT
            cutoff_num = EdgeMetaGeneDis.HQ_CUTOFF
        elif quality is QualityType.MQ:
            cutoff_txt = EdgeMetaGeneDis.MQ_CUTOFF_TEXT
            cutoff_num = EdgeMetaGeneDis.MQ_CUTOFF
        elif quality is QualityType.LQ:
            cutoff_txt = EdgeMetaGeneDis.LQ_CUTOFF_TEXT
            cutoff_num = EdgeMetaGeneDis.LQ_CUTOFF
        else:
            cutoff_txt = None
            cutoff_num = None

        self.edgeType = EdgeType.GENE_DIS

        self.EdgesMetaClass = InMetaEdgeDisGeNet
        self.Map1MetaClass = None
        self.Map2MetaClass = InMetaMapDisGeNet
        self.MapAltId2MetaClass = InMetaMapOntoDoAltid


        edges_file_path = os.path.join(glob.IN_FILE_PATH, self.EdgesMetaClass.CSV_NAME)
        mapping_file2 = os.path.join(glob.IN_FILE_PATH, self.Map2MetaClass.CSV_NAME)
        altid_mapping_file2 = os.path.join(glob.IN_FILE_PATH, self.MapAltId2MetaClass.CSV_NAME)

        super().__init__(is_directional=True,
                         edges_file_path=edges_file_path,
                         colindex1=self.EdgesMetaClass.NODE1_COL, colindex2=self.EdgesMetaClass.NODE2_COL,
                         edgeType=self.EdgesMetaClass.EDGE_TYPE,
                         node1_type=self.EdgesMetaClass.NODE1_TYPE, node2_type=self.EdgesMetaClass.NODE2_TYPE,
                         colindex_qscore=self.EdgesMetaClass.QSCORE_COL, cutoff_num=cutoff_num, cutoff_txt=cutoff_txt,
                         mapping2_file=mapping_file2, map2_sourceindex=self.Map2MetaClass.SOURCE_COL, map2_targetindex=self.Map2MetaClass.TARGET_COL,
                         altid_mapping2_file=altid_mapping_file2,
                         altid_map2_sourceindex=self.MapAltId2MetaClass.SOURCE_COL,
                         altid_map2_targetindex=self.MapAltId2MetaClass.TARGET_COL
                         )