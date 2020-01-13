from enum import Enum


class EdgeType(Enum):
    IS_A = 0
    PART_OF = 1

    GENE_GENE = 10
    GENE_GO = 11
    GENE_DIS = 12
    GENE_DRUG = 13
    GENE_PHENOTYPE = 14
    GENE_PATHWAY = 15
    GENE_EXPRESSED_ANATOMY = 16
    DIS_DRUG = 17
    DIS_PHENOTYPE = 18
    DRUG_PHENOTYPE = 19
    GENE_OVEREXPRESSED_ANATOMY = 20
    GENE_UNDEREXPRESSED_ANATOMY = 201

    DRUG_ACTIVATION_GENE = 21
    DRUG_BINDING_GENE = 22
    DRUG_CATALYSIS_GENE = 23
    DRUG_EXPRESSION_GENE = 24
    DRUG_INHIBITION_GENE = 25
    DRUG_PREDBIND_GENE = 26
    DRUG_REACTION_GENE = 27
    DRUG_BINDACT_GENE = 28
    DRUG_BINDINH_GENE = 29

    GENE_ACTIVATION_GENE = 31
    GENE_BINDING_GENE = 32
    GENE_CATALYSIS_GENE = 33
    GENE_EXPRESSION_GENE = 34
    GENE_INHIBITION_GENE = 35
    GENE_PTMOD_GENE = 36
    GENE_REACTION_GENE = 37
    GENE_BINDACT_GENE = 38
    GENE_BINDINH_GENE = 39

    def __str__(self):
        return (self.name)

    def get_parent(self):
        if self in [EdgeType.DRUG_ACTIVATION_GENE,
                    EdgeType.DRUG_BINDING_GENE,
                    EdgeType.DRUG_CATALYSIS_GENE,
                    EdgeType.DRUG_EXPRESSION_GENE,
                    EdgeType.DRUG_INHIBITION_GENE,
                    EdgeType.DRUG_PREDBIND_GENE,
                    EdgeType.DRUG_REACTION_GENE,
                    EdgeType.DRUG_BINDACT_GENE,
                    EdgeType.DRUG_BINDINH_GENE]:
            return EdgeType.GENE_DRUG
        elif self in [EdgeType.GENE_ACTIVATION_GENE,
                      EdgeType.GENE_BINDING_GENE,
                      EdgeType.GENE_CATALYSIS_GENE,
                      EdgeType.GENE_EXPRESSION_GENE,
                      EdgeType.GENE_INHIBITION_GENE,
                      EdgeType.GENE_PTMOD_GENE,
                      EdgeType.GENE_REACTION_GENE,
                      EdgeType.GENE_BINDACT_GENE,
                      EdgeType.GENE_BINDINH_GENE]:
            return EdgeType.GENE_GENE
        elif self in [EdgeType.GENE_OVEREXPRESSED_ANATOMY,
                      EdgeType.GENE_UNDEREXPRESSED_ANATOMY]:
            return EdgeType.GENE_EXPRESSED_ANATOMY
        else:
            return self
