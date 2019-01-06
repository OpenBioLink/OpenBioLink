from enum import Enum

class MappingType(Enum):
    UMLS_DO = 0
    OMIM_DO = 1
    UMLS_HPO = 2
    STRING_NCBI = 3
    ENSEMBL_NCBI = 4
    UNIPRO_NCBI = 5