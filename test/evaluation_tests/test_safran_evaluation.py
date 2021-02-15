import torch
from openbiolink.evaluation.dataLoader import DataLoader
from openbiolink.evaluation.evaluation import Evaluator


class SafranEvaluator(Evaluator):

    def __init__(self, dataset_name, evaluation_file_path):
        dl = DataLoader(dataset_name)
        super().__init__(dl)

        with open(evaluation_file_path) as infile:
            content = infile.readlines()
        content = [x.strip() for x in content]

        self.predictions = dict()

        for i in range(0, len(content), 3):
            head, rel, tail = content[i].split(" ")

            head = self.dl.entity_to_id[head]
            rel = self.dl.relation_to_id[rel]
            tail = self.dl.entity_to_id[tail]

            pos_head = 0.0
            neg_head = []
            head_predictions = content[i+1]
            if(head_predictions == "Heads:"):
                continue
            else:
                head_predictions = head_predictions[len("Heads: "):].split("\t")
                for j in range(0, len(head_predictions), 2):
                    head_prediction = self.dl.entity_to_id[head_predictions[j]]
                    confidence = float(head_predictions[j+1])
                    if head == head_prediction:
                        # Correct prediction
                        pos_head = confidence
                    else:
                        # False prediction
                        neg_head.append((head_prediction, confidence))

            pos_tail = 0.0
            neg_tail = []
            tail_predictions = content[i+2]
            if tail_predictions == "Tails:":
                continue
            else:
                tail_predictions = tail_predictions[len("Tails: "):].split("\t")
                for j in range(0, len(tail_predictions), 2):
                    tail_prediction = self.dl.entity_to_id[tail_predictions[j]]
                    confidence = float(tail_predictions[j+1])
                    if tail == tail_prediction:
                        # Correct prediction
                        pos_tail = confidence
                    else:
                        # False prediction
                        neg_tail.append((tail_prediction, confidence))
            self.predictions[f"{str(head)};{str(rel)};{str(tail)}"] = (pos_head, neg_head, pos_tail, neg_tail)



    def score_batch(self, batch):
        pos_score_head = torch.zeros((len(batch),), dtype=torch.float)
        neg_score_head = torch.zeros((100, self.num_neg), dtype=torch.float)
        pos_score_tail = torch.zeros((len(batch),), dtype=torch.float)
        neg_score_tail = torch.zeros((100, self.num_neg), dtype=torch.float)

        for i in range(batch.shape[0]):
            head, rel, tail = batch[i,:]
            key = f"{str(head.item())};{str(rel.item())};{str(tail.item())}"

            if key in self.predictions:
                (pos_head, neg_heads, pos_tail, neg_tails) = self.predictions[key]
                pos_score_head[i] = pos_head
                for neg_head, confidence in neg_heads:
                    neg_score_head[i, neg_head] = confidence

                pos_score_tail[i] = pos_tail
                for neg_tail, confidence in neg_tails:
                    neg_score_tail[i, neg_tail] = confidence
            else:
                pass


        return pos_score_head, neg_score_head, pos_score_tail, neg_score_tail


if __name__ == "__main__":

    evaluation_file_path = r"G:\prediction.txt"

    evaluator = SafranEvaluator("HQ_DIR", evaluation_file_path)
    result = evaluator.evaluate(100, 1, filtering=False)
    print(result)