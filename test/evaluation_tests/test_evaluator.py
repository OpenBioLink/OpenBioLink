from openbiolink.evaluation.evaluation import Evaluator
import numpy as np

evaluator = Evaluator()
print(evaluator.expected_input_format)
print(evaluator.expected_output_format)

y_pred_pos = np.random.randn(1000,)
y_pred_neg = np.random.randn(1000,100)

input_dict = {'y_pred_pos': y_pred_pos, 'y_pred_neg': y_pred_neg}
result = evaluator.eval(input_dict)

print(f"Hits@1 {result['hits@1_list'].mean()}")
print(f"Hits@3 {result['hits@3_list'].mean()}")
print(f"Hits@10 {result['hits@10_list'].mean()}")
print(f"MRR {result['mrr_list'].mean()}")