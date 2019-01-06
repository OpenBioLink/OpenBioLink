import os

import graph_creation.globalConstant as glob
from graph_creation.metadata_edge.edgeMetadata import EdgeMetadata
from graph_creation.metadata_infile.edge.inMetaEdgeHpoGene import InMetaEdgeHpoGene
from graph_creation.qualityType import QualityType


class EdgeMetaGenePheno(EdgeMetadata):
    LQ_CUTOFF = None
    MQ_CUTOFF = None
    HQ_CUTOFF = None
    LQ_CUTOFF_TEXT = None
    MQ_CUTOFF_TEXT = None
    HQ_CUTOFF_TEXT = None

    def __init__(self, quality : QualityType= None):
        if quality is QualityType.HQ:
            cutoff_txt = EdgeMetaGenePheno.HQ_CUTOFF_TEXT
            cutoff_num = EdgeMetaGenePheno.HQ_CUTOFF
        elif quality is QualityType.MQ:
            cutoff_txt = EdgeMetaGenePheno.MQ_CUTOFF_TEXT
            cutoff_num = EdgeMetaGenePheno.MQ_CUTOFF
        elif quality is QualityType.LQ:
            cutoff_txt = EdgeMetaGenePheno.LQ_CUTOFF_TEXT
            cutoff_num = EdgeMetaGenePheno.LQ_CUTOFF
        else:
            cutoff_txt = None
            cutoff_num = None

        self.EdgesMetaClass = InMetaEdgeHpoGene
        self.Map1MetaClass = None
        self.Map2MetaClass = None

        edges_file_path = os.path.join(glob.IN_FILE_PATH, self.EdgesMetaClass.CSV_NAME)
        super().__init__(edges_file_path=edges_file_path,
                         colindex1=self.EdgesMetaClass.NODE1_COL, colindex2=self.EdgesMetaClass.NODE2_COL,
                         edgeType=self.EdgesMetaClass.EDGE_TYPE,
                         node1_type=self.EdgesMetaClass.NODE1_TYPE, node2_type=self.EdgesMetaClass.NODE2_TYPE,
                         colindex_qscore=self.EdgesMetaClass.QSCORE_COL)
