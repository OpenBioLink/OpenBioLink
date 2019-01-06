from graph_creation.metadata_db_file.edge.dbMetadataEdge import DbMetadataEdge
from graph_creation.dbType import DbType


class DbMetaEdgeSiderSe(DbMetadataEdge):
    URL = "http://sideeffects.embl.de/media/download/meddra_all_se.tsv.gz"
    OFILE_NAME = "SIDER_se.tsv.gz"
    COLS = ['stitchID_flat', 'stitchID_stereo', 'umlsID', 'medDRAumlsType', 'medDRAumlsID', 'SEname']
    FILTER_COLS = ['stitchID_flat', 'umlsID']
    HEADER = 0
    DB_TYPE = DbType.DB_EDGE_SIDER_SE

    def __init__(self):

        super().__init__(url= DbMetaEdgeSiderSe.URL,
                         ofile_name=DbMetaEdgeSiderSe.OFILE_NAME,
                         dbType=DbMetaEdgeSiderSe.DB_TYPE)