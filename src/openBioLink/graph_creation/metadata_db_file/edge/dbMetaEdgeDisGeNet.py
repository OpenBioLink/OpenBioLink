from openbiolink.graph_creation.metadata_db_file.edge.dbMetadataEdge import DbMetadataEdge
from openbiolink.graph_creation.types.dbType import DbType


class DbMetaEdgeDisGeNet(DbMetadataEdge):
    NAME = 'Edge - DisGeNet - Gene Disease'
    # URL = "http://www.disgenet.org/ds/DisGeNET/results/curated_gene_disease_associations.tsv.gz"
    URL = "http://www.disgenet.org/static/disgenet_ap1/files/downloads/curated_gene_disease_associations.tsv.gz"
    OFILE_NAME = "DisGeNet_gene_disease.tsv.gz"
    COLS = ['geneID', 'geneSym', 'DSI', 'DPI', 'umlsID', 'disName', 'diseaseType', 'diseaseClass',
            'diseaseSemanticType', 'score', 'EI', 'YearInitial', 'YearFinal', 'NofPmids', 'NofSnps', 'source']

    FILTER_COLS = ['geneID', 'umlsID', 'score']
    HEADER = 1
    DB_TYPE = DbType.DB_EDGE_DISGENET

    def __init__(self):
        super().__init__(url=DbMetaEdgeDisGeNet.URL,
                         ofile_name=DbMetaEdgeDisGeNet.OFILE_NAME,
                         dbType=DbMetaEdgeDisGeNet.DB_TYPE)
