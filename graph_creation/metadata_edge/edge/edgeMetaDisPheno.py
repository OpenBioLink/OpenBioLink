import os
import graph_creation.globalConstant as glob

from graph_creation.metadata_infile.edge.inMetaEdgeHpoDis import InMetaEdgeHpoDis
from graph_creation.metadata_infile.mapping.inMetaMapOntoDoOmim import InMetaMapOntoDoOmim
from graph_creation.metadata_infile import InMetaMapOntoDoAltid, InMetaMapOntoHpoAltid

from graph_creation.Types.qualityType import QualityType

from graph_creation.metadata_edge.edgeMetadata import EdgeMetadata


class EdgeMetaDisPheno(EdgeMetadata):
    LQ_CUTOFF = None
    MQ_CUTOFF = None
    HQ_CUTOFF = None
    LQ_CUTOFF_TEXT = None
    MQ_CUTOFF_TEXT = None
    HQ_CUTOFF_TEXT = None
    def __init__(self, quality : QualityType = None):
        if quality is QualityType.HQ:
            cutoff_txt = EdgeMetaDisPheno.HQ_CUTOFF_TEXT
            cutoff_num = EdgeMetaDisPheno.HQ_CUTOFF
        elif quality is QualityType.MQ:
            cutoff_txt = EdgeMetaDisPheno.MQ_CUTOFF_TEXT
            cutoff_num = EdgeMetaDisPheno.MQ_CUTOFF
        elif quality is QualityType.LQ:
            cutoff_txt = EdgeMetaDisPheno.LQ_CUTOFF_TEXT
            cutoff_num = EdgeMetaDisPheno.LQ_CUTOFF
        else:
            cutoff_txt = None
            cutoff_num = None

        self.EdgesMetaClass = InMetaEdgeHpoDis
        self.Map1MetaClass = InMetaMapOntoDoOmim
        self.Map2MetaClass = None
        self.MapAltId1MetaClass = InMetaMapOntoDoAltid
        self.MapAltId2MetaClass = InMetaMapOntoHpoAltid


        edges_file_path = os.path.join(glob.IN_FILE_PATH, self.EdgesMetaClass.CSV_NAME)
        mapping_file1 = os.path.join(glob.IN_FILE_PATH, self.Map1MetaClass.CSV_NAME)
        altid_mapping_file1 = os.path.join(glob.IN_FILE_PATH, self.MapAltId1MetaClass.CSV_NAME)
        altid_mapping_file2 = os.path.join(glob.IN_FILE_PATH, self.MapAltId2MetaClass.CSV_NAME)

        super().__init__(is_directional=True,
                         edges_file_path=edges_file_path,
                         colindex1=self.EdgesMetaClass.NODE1_COL, colindex2=self.EdgesMetaClass.NODE2_COL,
                         edgeType=self.EdgesMetaClass.EDGE_TYPE,
                         node1_type=self.EdgesMetaClass.NODE1_TYPE, node2_type=self.EdgesMetaClass.NODE2_TYPE,
                         colindex_qscore=self.EdgesMetaClass.QSCORE_COL,  # todo check licenses / if IEA ok
                         mapping1_file=mapping_file1,
                         map1_sourceindex=self.Map1MetaClass.SOURCE_COL, map1_targetindex=self.Map1MetaClass.TARGET_COL,
                         altid_mapping1_file=altid_mapping_file1,
                         altid_map1_sourceindex=self.MapAltId1MetaClass.SOURCE_COL, altid_map1_targetindex=self.MapAltId1MetaClass.TARGET_COL,
                         altid_mapping2_file=altid_mapping_file2,
                         altid_map2_sourceindex=self.MapAltId2MetaClass.SOURCE_COL, altid_map2_targetindex=self.MapAltId2MetaClass.TARGET_COL
                         )
