from openbiolink.graph_creation.metadata_db_file.mapping.dbMetadataMapping import DbMetadataMapping
from openbiolink.graph_creation.types.dbType import DbType


class DbMetaMapDisGeNet(DbMetadataMapping):
    NAME = 'Mapping - DisGeNet - Disease (umls -> do)'
    # URL = "http://www.disgenet.org/ds/DisGeNET/results/disease_mappings.tsv.gz"
    URL = "http://www.disgenet.org/static/disgenet_ap1/files/downloads/disease_mappings.tsv.gz"
    OFILE_NAME = "DisGeNet_mapping_disease_umls_do.tab.gz"
    COLS = ['umlsID', 'name', 'voc', 'code', 'vocName']
    FILTER_COLS = ['umlsID', 'voc', 'code']
    HEADER = 1
    DB_TYPE = DbType.DB_MAP_DISGENET

    def __init__(self):
        super().__init__(url=DbMetaMapDisGeNet.URL,
                         ofile_name=DbMetaMapDisGeNet.OFILE_NAME,
                         dbType=DbMetaMapDisGeNet.DB_TYPE)
