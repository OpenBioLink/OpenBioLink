from enum import Enum

class MappingType(Enum):
    UMLS_DO = 0
    OMIM_DO = 1
    UMLS_HPO = 2
    STRING_NCBI = 3
    ENSEMBL_NCBI = 4
    UNIPRO_NCBI = 5
    DRUGCENTRAL_PUBCHEM = 6

    ALT_DO_DO =10
    ALT_GO_GO =11
    ALT_HPO_HPO =12
    ALT_UBERON_UBERON = 13
