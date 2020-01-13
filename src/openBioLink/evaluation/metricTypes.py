from enum import Enum


class RankMetricType(Enum):
    HITS_AT_K = 'hits@K'
    HITS_AT_K_UNFILTERED = 'unfiltered hits@k'
    MRR = 'MRR'
    MRR_UNFILTERED = 'unfiltered MRR'


class ThresholdMetricType(Enum):
    ROC = 'ROC'
    ROC_AUC = 'ROC AUC'
    PR_REC_CURVE = 'precision-recall curve (PRC)'
    PR_AUC = 'PRC AUC'
