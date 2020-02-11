from enum import Enum


class Namespaces(Enum):
    CL = "CL"
    DIS = "DOID"
    ENSEMBL = "ENSEMBL"
    GO = "GO"
    HPO = "HP"
    KEGG = "KEGG"
    NCBI = "NCBIGENE"
    PUBCHEM = "PUBCHEM.COMPOUND"
    REACTOME = "REACTOME"
    UBERON = "UBERON"
    UMLS = "UMLS"
    UNIPROT = "UNIPROT"

    MULTI = "MULTI"
    NONE = "NONE"

    def __str__(self):
        return self.name


class Namespace:
    def __init__(self, namespace, isNamespaceInId=True, mapping=None):
        if namespace.value == Namespaces.MULTI:
            assert isNamespaceInId, "Namespace of type MULTI must have the Namespace in the ID"
        self.namespace = namespace
        self.isNamespaceInID = isNamespaceInId
        self.mapping = mapping

    def resolve(self, id):
        if self.mapping is not None:
            for key, value in self.mapping.items():
                id = id.replace(key, value)
        if self.namespace == Namespaces.NONE:
            return id
        if not self.isNamespaceInID:
            id = self.namespace.value + ":" + id
        return id

    def __str__(self):
        return self.namespace.value
