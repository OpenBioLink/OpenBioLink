import torch

from openbiolink.evaluation.evaluation import Evaluator
import numpy as np
import time

evaluator = Evaluator()
print(evaluator.expected_input_format)
print(evaluator.expected_output_format)

np.random.seed(0)

y_pred_pos = torch.randn(180, )
y_pred_neg = torch.randn(180, 5000)

start = time.time()

for i in range(1000):
    evaluator.update(y_pred_pos, y_pred_neg)


result = evaluator.result()

print(time.time() - start)

print(f"Hits@1 {result['hits@1']}")
print(f"Hits@3 {result['hits@3']}")
print(f"Hits@10 {result['hits@10']}")
print(f"MRR {result['mrr']}")