from enum import Enum


class NodeType(Enum):
    GENE = 0
    GO = 1
    DIS = 2
    DRUG = 3
    PHENOTYPE = 4
    PATHWAY = 5
    ANATOMY = 6

    def __str__(self):
        return (self.name)
