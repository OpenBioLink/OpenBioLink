from openbiolink.graph_creation.metadata_db_file.edge.dbMetadataEdge import DbMetadataEdge
from openbiolink.graph_creation.types.dbType import DbType


class DbMetaEdgeDrugCentral(DbMetadataEdge):
    NAME = 'Edge/Mapping - DrugCentral - (Contra)Indications, Mapping:(dc --> pubchem)'
    URL = "http://unmtid-shinyapps.net/download/drugcentral.dump.08262018.sql.gz"
    OFILE_NAME = "sql_dump.sql.gz"

    TABLE_NAME_IND = "public.omop_relationship"
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

    TABLE_NAME_MAP_PUBCHEM = "public.identifier"
    COLS_MAP_PUBCHEM = [
        "id",
        "identifier",
        "id_type",
        "struct_id",
        "parent_match"
    ]

    DB_TYPE = DbType.DB_EDGE_DRUGCENTRAL

    def __init__(self):
        super().__init__(url=DbMetaEdgeDrugCentral.URL,
                         ofile_name=DbMetaEdgeDrugCentral.OFILE_NAME,
                         dbType=DbMetaEdgeDrugCentral.DB_TYPE)
