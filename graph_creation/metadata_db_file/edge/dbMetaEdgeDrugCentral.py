from graph_creation.metadata_db_file.edge.dbMetadataEdge import DbMetadataEdge
from graph_creation.Types.dbType import DbType


class DbMetaEdgeDrugCentral(DbMetadataEdge):
    URL = "http://unmtid-shinyapps.net/download/drugcentral.dump.08262018.sql.gz"
    OFILE_NAME = "sql_dump.sql.gz"

    TABLE_NAME_IND = "omop_relationship"
    COLS_IND = [
        "id",
        "struct_id",
        "concept_id",
        "relationship_name",
        "concept_name",
        "umls_cui",
        "snomed_full_name",
        "cui_semantic_type",
        "snomed_conceptid"
    ]
    DB_TYPE_IND = DbType.DB_EDGE_DRUGCENTRAL

    TABLE_NAME_MAP_PUBCHEM = "identifier"
    COLS_MAP_PUBCHEM = [
        "id",
        "identifier",
        "id_type",
        "struct_id",
        "parent_match"
    ]
    DB_TYPE_MAP_PUBCHEM = DbType.DB_EDGE_DRUGCENTRAL

    def __init__(self):
        super().__init__(url=DbMetaEdgeDrugCentral.URL,
                         ofile_name=DbMetaEdgeDrugCentral.OFILE_NAME,
                         dbType=DbMetaEdgeDrugCentral.DB_TYPE_IND)