from openbiolink.graph_creation.metadata_edge.edgeMetadata import EdgeMetadata
from openbiolink.graph_creation.types.qualityType import QualityType


class EdgeRegularMetadata(EdgeMetadata):
    LQ_CUTOFF = None
    MQ_CUTOFF = None
    HQ_CUTOFF = None
    LQ_CUTOFF_TEXT = None
    MQ_CUTOFF_TEXT = None
    HQ_CUTOFF_TEXT = None

    def __init__(self, is_directional, edges_file_path, colindex1, colindex2, edgeType, node1_type, node2_type,
                 colindex_qscore=None,
                 mapping1_file=None, map1_sourceindex=None, map1_targetindex=None,
                 altid_mapping1_file=None, altid_map1_sourceindex=None, altid_map1_targetindex=None,
                 mapping2_file=None, map2_sourceindex=None, map2_targetindex=None,
                 altid_mapping2_file=None, altid_map2_sourceindex=None, altid_map2_targetindex=None,
                 quality: QualityType = None):
        if quality is QualityType.HQ:
            cutoff_txt = self.HQ_CUTOFF_TEXT
            cutoff_num = self.HQ_CUTOFF
        elif quality is QualityType.MQ:
            cutoff_txt = self.MQ_CUTOFF_TEXT
            cutoff_num = self.MQ_CUTOFF
        elif quality is QualityType.LQ:
            cutoff_txt = self.LQ_CUTOFF_TEXT
            cutoff_num = self.LQ_CUTOFF
        else:
            cutoff_txt = None
            cutoff_num = None
        super().__init__(is_directional=is_directional,
                         edges_file_path=edges_file_path,
                         colindex1=colindex1, colindex2=colindex2,
                         edgeType=edgeType,
                         node1_type=node1_type, node2_type=node2_type,
                         colindex_qscore=colindex_qscore, cutoff_num=cutoff_num, cutoff_txt=cutoff_txt,
                         mapping1_file=mapping1_file,
                         map1_sourceindex=map1_sourceindex, map1_targetindex=map1_targetindex,
                         altid_mapping1_file=altid_mapping1_file,
                         altid_map1_sourceindex=altid_map1_sourceindex, altid_map1_targetindex=altid_map1_targetindex,
                         mapping2_file=mapping2_file,
                         map2_sourceindex=map2_sourceindex, map2_targetindex=map2_targetindex,
                         altid_mapping2_file=altid_mapping2_file,
                         altid_map2_sourceindex=altid_map2_sourceindex, altid_map2_targetindex=altid_map2_targetindex
                         )
