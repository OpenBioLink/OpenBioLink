from enum import Enum
import evaluation.models.pykeen_models as pykeen_models
class ModelTypes(Enum):

    #PYKEEN_TRANS_E = 'TransE_PyKeen'
    #PYKEEN_TRANS_R = 'TransR_PyKeen'
    TransE_PyKeen = pykeen_models.TransE_PyKeen
    TransR_Pykeen = pykeen_models.TransR_PyKeen


