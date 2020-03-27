from openbiolink.graph_creation.metadata_db_file.edge.dbMetadataEdge import DbMetadataEdge
from openbiolink.graph_creation.types.dbType import DbType


class DbMetaEdgeHpoGene(DbMetadataEdge):
    NAME = "Edge - HPO - Gene Phenotype"
    URL = "http://compbio.charite.de/jenkins/job/hpo.annotations/1270/artifact/util/annotation/genes_to_phenotype.txt"
    OFILE_NAME = "HPO_gene_phenotype.tsv"
    COLS = ["geneID", "geneSymb", "hpoID", "hpoName", "frequencyRaw", "frequencyHPO", "addInfo", "source", "disId"]
    FILTER_COLS = ["geneID", "hpoID"]
    HEADER = 1
    DB_TYPE = DbType.DB_EDGE_HPO_GENE

    def __init__(self):
        super().__init__(
            url=DbMetaEdgeHpoGene.URL, ofile_name=DbMetaEdgeHpoGene.OFILE_NAME, dbType=DbMetaEdgeHpoGene.DB_TYPE
        )
