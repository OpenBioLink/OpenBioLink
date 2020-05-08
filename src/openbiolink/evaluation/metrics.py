class Metrics:
    ###### calculate metrics ######

    @staticmethod
    def calculate_hits_at_k(ks, ranks_corrupted_heads, ranks_corrupted_tails, num_examples):
        corrupted_heads_hits_at_k = dict()
        corrupted_tails_hits_at_k = dict()
        for k in ks:
            corrupted_heads_hits_at_k[k] = len([x for x in ranks_corrupted_heads if x <= k]) / num_examples
            corrupted_tails_hits_at_k[k] = len([x for x in ranks_corrupted_tails if x <= k]) / num_examples
        return corrupted_heads_hits_at_k, corrupted_tails_hits_at_k

    @staticmethod
    def calculate_mrr(ranks_corrupted_heads, ranks_corrupted_tails, num_examples):
        inverse_ranks_corrupted_heads = [1 / n for n in ranks_corrupted_heads]
        inverse_ranks_corrupted_tails = [1 / n for n in ranks_corrupted_tails]
        mrr_heads = sum(inverse_ranks_corrupted_heads) / num_examples
        mrr_tails = sum(inverse_ranks_corrupted_tails) / num_examples
        return mrr_heads, mrr_tails

    @staticmethod
    def calculate_roc_curve(labels, scores):
        from sklearn.metrics import roc_curve

        fpr, tpr, _ = roc_curve(labels, scores)
        return list(fpr), list(tpr)

    @staticmethod
    def calculate_pr_curve(labels, scores):
        from sklearn.metrics import precision_recall_curve

        precision, recall, thresholds = precision_recall_curve(labels, scores)
        return list(precision), list(recall)

    @staticmethod
    def calculate_auc(x_values, y_values):
        from sklearn.metrics import auc

        auc_value = auc(x_values, y_values)
        return auc_value