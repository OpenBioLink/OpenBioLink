from openbiolink.graph_creation.metadata_db_file.edge.dbMetadataEdge import DbMetadataEdge
from openbiolink.graph_creation.types.dbType import DbType


class DbMetaEdgeSiderInd(DbMetadataEdge):
    NAME = 'Edge - Sider - Indications'
    URL = "http://sideeffects.embl.de/media/download/meddra_all_indications.tsv.gz"
    OFILE_NAME = "SIDER_dis_drug.tsv.gz"
    COLS = ['stichID', 'umlsID', 'method', 'umlsName', 'medDRAumlsType',
            'medDRAumlsID', 'medDRAumlsName']
    FILTER_COLS = ['umlsID', 'stichID', 'method']
    HEADER = 0
    DB_TYPE = DbType.DB_EDGE_SIDER_IND

    def __init__(self):
        super().__init__(url=DbMetaEdgeSiderInd.URL,
                         ofile_name=DbMetaEdgeSiderInd.OFILE_NAME,
                         dbType=DbMetaEdgeSiderInd.DB_TYPE)
