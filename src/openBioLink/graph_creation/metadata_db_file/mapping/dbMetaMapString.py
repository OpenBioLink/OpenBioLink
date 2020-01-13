from openbiolink.graph_creation.metadata_db_file.mapping.dbMetadataMapping import DbMetadataMapping
from openbiolink.graph_creation.types.dbType import DbType


class DbMetaMapString(DbMetadataMapping):
    NAME = 'Mapping - DisGeNet - Gene (string -> ncbi entrez)'
    # URL = "http://string-db.org/mapping_files/entrez_mappings//entrez_gene_id.vs.string.v10.28042015.tsv"
    URL = "http://string-db.org/mapping_files/entrez/human.entrez_2_string.2018.tsv.gz"
    OFILE_NAME = "String_mapping_gene_ncbi_string.tsv.gz"
    COLS = ['tax_id', 'ncbiID', 'stringID']
    FILTER_COLS = ['ncbiID', 'stringID']
    HEADER = 1
    DB_TYPE = DbType.DB_MAP_STRING

    def __init__(self):
        super().__init__(url=DbMetaMapString.URL,
                         ofile_name=DbMetaMapString.OFILE_NAME,
                         dbType=DbMetaMapString.DB_TYPE)
