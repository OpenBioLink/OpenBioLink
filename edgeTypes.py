from enum import Enum


class EdgeType (Enum):
    IS_A = 0
    HAS_A = 1

    GENE_GENE = 10
    GENE_GO = 11
    GENE_DIS = 12
    GENE_DRUG = 13
    GENE_PHENOTYPE = 14
    GENE_PATHWAY = 15
    GENE_ANATOMY = 16
    DIS_DRUG = 17
    DIS_PHENOTYPE = 18
    DRUG_PHENOTYPE = 19