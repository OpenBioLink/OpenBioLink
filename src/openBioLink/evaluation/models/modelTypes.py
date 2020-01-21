from enum import Enum
import evaluation.models.pykeen_models as pykeen_models
class ModelTypes(Enum):

    #Model_Name = ModelClass
    TransE_Pykeen = pykeen_models.TransE_PyKeen
    TransR_Pykeen = pykeen_models.TransR_PyKeen
    TransD_Pykeen = pykeen_models.TransD_PyKeen
    TransH_Pykeen = pykeen_models.TransH_PyKeen
    UM_Pykeen = pykeen_models.Unstructured_PyKeen
    DistMult_Pykeen = pykeen_models.DistMult_PyKeen
    SE_Pykeen = pykeen_models.SE_PyKeen
    Rescal_Pykeen = pykeen_models.Rescal_PyKeen



