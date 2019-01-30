import os
import graph_creation.globalConstant as glob
from graph_creation.metadata_infile import InMetaMapOntoHpoAltid

from graph_creation.metadata_infile.edge.inMetaEdgeSiderSe import InMetaEdgeSiderSe
from graph_creation.metadata_infile.mapping.inMetaMapOntoHpoUmls import InMetaMapOntoHpoUmls


from graph_creation.Types.qualityType import QualityType

from graph_creation.metadata_edge.edgeMetadata import EdgeMetadata


class EdgeMetaDrugPheno(EdgeMetadata):
    LQ_CUTOFF = None
    MQ_CUTOFF = None
    HQ_CUTOFF = None
    LQ_CUTOFF_TEXT = None
    MQ_CUTOFF_TEXT = None
    HQ_CUTOFF_TEXT = None
    def __init__(self, quality : QualityType = None):
        if quality is QualityType.HQ:
            cutoff_txt = EdgeMetaDrugPheno.HQ_CUTOFF_TEXT
            cutoff_num = EdgeMetaDrugPheno.HQ_CUTOFF
        elif quality is QualityType.MQ:
            cutoff_txt = EdgeMetaDrugPheno.MQ_CUTOFF_TEXT
            cutoff_num = EdgeMetaDrugPheno.MQ_CUTOFF
        elif quality is QualityType.LQ:
            cutoff_txt = EdgeMetaDrugPheno.LQ_CUTOFF_TEXT
            cutoff_num = EdgeMetaDrugPheno.LQ_CUTOFF
        else:
            cutoff_txt = None
            cutoff_num = None

        self.EdgesMetaClass = InMetaEdgeSiderSe
        self.Map1MetaClass = None
        self.Map2MetaClass = InMetaMapOntoHpoUmls
        self.MapAltId2MetaClass = InMetaMapOntoHpoAltid

        edges_file_path = os.path.join(glob.IN_FILE_PATH, self.EdgesMetaClass.CSV_NAME)
        mapping_file2 = os.path.join(glob.IN_FILE_PATH, self.Map2MetaClass.CSV_NAME)
        altid_mapping_file2 = os.path.join(glob.IN_FILE_PATH, self.MapAltId2MetaClass.CSV_NAME)

        super().__init__(is_directional=True,
                         edges_file_path=edges_file_path,
                         colindex1=self.EdgesMetaClass.NODE1_COL, colindex2=self.EdgesMetaClass.NODE2_COL,
                         edgeType=self.EdgesMetaClass.EDGE_TYPE,
                         node1_type=self.EdgesMetaClass.NODE1_TYPE, node2_type=self.EdgesMetaClass.NODE2_TYPE,
                         colindex_qscore=self.EdgesMetaClass.QSCORE_COL,
                         mapping2_file=mapping_file2, map2_sourceindex=self.Map2MetaClass.SOURCE_COL, map2_targetindex=self.Map2MetaClass.TARGET_COL,
                         altid_mapping2_file=altid_mapping_file2,
                         altid_map2_sourceindex=self.MapAltId2MetaClass.SOURCE_COL,
                         altid_map2_targetindex=self.MapAltId2MetaClass.TARGET_COL
                         )
