import os
import graph_creation.globalConstant as glob

from graph_creation.metadata_infile.edge.inMetaEdgeCdtPath import InMetaEdgeCdtPath

from graph_creation.Types.qualityType import QualityType

from graph_creation.metadata_edge.edgeMetadata import EdgeMetadata


class EdgeMetaGenePath(EdgeMetadata):
    LQ_CUTOFF = None
    MQ_CUTOFF = None
    HQ_CUTOFF = None
    LQ_CUTOFF_TEXT = None
    MQ_CUTOFF_TEXT = None
    HQ_CUTOFF_TEXT = None

    def __init__(self, quality : QualityType):
        if quality is QualityType.HQ:
            cutoff_txt = EdgeMetaGenePath.HQ_CUTOFF_TEXT
            cutoff_num = EdgeMetaGenePath.HQ_CUTOFF
        elif quality is QualityType.MQ:
            cutoff_txt = EdgeMetaGenePath.MQ_CUTOFF_TEXT
            cutoff_num = EdgeMetaGenePath.MQ_CUTOFF
        elif quality is QualityType.LQ:
            cutoff_txt = EdgeMetaGenePath.LQ_CUTOFF_TEXT
            cutoff_num = EdgeMetaGenePath.LQ_CUTOFF
        else:
            cutoff_txt = None
            cutoff_num = None

        self.EdgesMetaClass =  InMetaEdgeCdtPath
        self.Map1MetaClass = None
        self.Map2MetaClass = None

        edges_file_path = os.path.join(glob.IN_FILE_PATH, self.EdgesMetaClass.CSV_NAME)
        super().__init__(edges_file_path=edges_file_path,
                         colindex1=self.EdgesMetaClass.NODE1_COL, colindex2=self.EdgesMetaClass.NODE2_COL,
                         edgeType=self.EdgesMetaClass.EDGE_TYPE,
                         node1_type=self.EdgesMetaClass.NODE1_TYPE, node2_type=self.EdgesMetaClass.NODE2_TYPE,
                         colindex_qscore=self.EdgesMetaClass.QSCORE_COL)
