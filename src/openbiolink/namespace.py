from enum import Enum

class Namespaces(Enum):
    NCBI = "NCBIGENE"
    GO = "GO"
    DIS = "DOID"
    PUBCHEM = "PUBCHEM.COMPOUND"
    UBERON = "UBERON"
    CL = "CL"
    HPO = "HP"
    REACTOME = "REACTOME"
    KEGG = "KEGG"
    BGEEGENE = "BEGEE.GENE"
    UMLS = "UMLS"
    UNIPROT = "UNIPROT"
    ENSEMBL = "ENSEMBL"
    MULTI = "MULTI"
    NONE = "NONE"

    def __str__(self):
        return (self.name)

class Namespace():
    def __init__(self,namespace,isNamespaceInId=True,mapping=None):
        if namespace.value == Namespaces.MULTI:
            assert isNamespaceInId == True, "Namespace of type MULTI must have the Namespace in the ID"
        self.namespace = namespace
        self.isNamespaceInID = isNamespaceInId
        self.mapping = mapping

    def resolve(self,id):
        if self.mapping != None:
            for key, value in self.mapping.items():
                id = id.replace(key,value)
        if self.isNamespaceInID == False:
            id = self.namespace.value + ":" + id
        return id





