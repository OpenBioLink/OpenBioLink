from openbiolink.graph_creation.metadata_db_file.edge.dbMetadataEdge import DbMetadataEdge
from openbiolink.graph_creation.types.dbType import DbType


class DbMetaEdgeCtdPath(DbMetadataEdge):
    NAME = 'Edge - CTD - Gene Pathway'

    URL = "http://ctdbase.org/reports/CTD_genes_pathways.tsv.gz"
    OFILE_NAME = "CDT_gene_pathway.tsv.gz"
    COLS = ['geneSymb', 'geneID', 'pathName', 'pathID']
    FILTER_COLS = ['geneID', 'pathID']
    HEADER = 29
    DB_TYPE = DbType.DB_EDGE_CDT_PATH

    def __init__(self):
        super().__init__(url=DbMetaEdgeCtdPath.URL,
                         ofile_name=DbMetaEdgeCtdPath.OFILE_NAME,
                         dbType=DbMetaEdgeCtdPath.DB_TYPE)
