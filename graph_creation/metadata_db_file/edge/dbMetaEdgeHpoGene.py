from graph_creation.metadata_db_file.edge.dbMetadataEdge import DbMetadataEdge
from graph_creation.dbType import DbType


class DbMetaEdgeHpoGene(DbMetadataEdge):
    URL = "http://compbio.charite.de/jenkins/job/hpo.annotations.monthly/lastSuccessfulBuild/artifact/annotation/ALL_SOURCES_ALL_FREQUENCIES_genes_to_phenotype.txt"
    OFILE_NAME = "HPO_gene_phenotype.tsv"
    COLS = ['geneID', 'geneSymb', 'hpoName', 'hpoID']
    FILTER_COLS = ['geneID', 'hpoID']
    HEADER = 1
    DB_TYPE = DbType.DB_EDGE_HPO_GENE

    def __init__(self):
        super().__init__(url= DbMetaEdgeHpoGene.URL,
                         ofile_name=DbMetaEdgeHpoGene.OFILE_NAME,
                         dbType=DbMetaEdgeHpoGene.DB_TYPE)