from graph_creation.metadata_db_file.edge.dbMetadataEdge import DbMetadataEdge
from graph_creation.Types.dbType import DbType


class DbMetaEdgeDisGeNet(DbMetadataEdge):
    URL = "http://www.disgenet.org/ds/DisGeNET/results/curated_gene_disease_associations.tsv.gz"
    OFILE_NAME = "DisGeNet_gene_disease.tsv.gz"
    COLS = ['geneID', 'geneSym', 'umlsID', 'disName', 'score', 'NofPmids', 'NofSnps', 'source']
    FILTER_COLS = ['geneID', 'umlsID', 'score']
    HEADER = 1
    DB_TYPE = DbType.DB_EDGE_DISGENET

    def __init__(self):
        super().__init__(url=DbMetaEdgeDisGeNet.URL,
                         ofile_name=DbMetaEdgeDisGeNet.OFILE_NAME,
                         dbType=DbMetaEdgeDisGeNet.DB_TYPE)