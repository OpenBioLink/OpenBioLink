import os

COL_NAMES_SAMPLES = ''
class TrainTestSetWriter():
    def __init__(self, col_names_samples):
        global  COL_NAMES_SAMPLES
        COL_NAMES_SAMPLES = col_names_samples


    def print_sets(self, train_val_set_tuples, test_set):
        num_folds = len(train_val_set_tuples)
        folder_path = os.path.join(os.getcwd(), "train_test_data")

        test_set[COL_NAMES_SAMPLES].to_csv(os.path.join(folder_path, "test_sample.csv"),
                                           sep='\t',
                                           index=False,
                                           header=False)
        if num_folds>1:
            folder_path = os.path.join(folder_path, "cross_val")
        i = 0
        for train_set, val_set in train_val_set_tuples:
            if num_folds > 1:
                folder_path = os.path.join(folder_path, "fold_%d" % (i))
            os.makedirs(folder_path, exist_ok=True)
            train_set[COL_NAMES_SAMPLES].to_csv(os.path.join(folder_path, "train_sample.csv"),
                                                sep='\t',
                                                index=False,
                                                header=False)
            val_set[COL_NAMES_SAMPLES].to_csv(os.path.join(folder_path, "val_sample.csv"),
                                              sep='\t',
                                              index=False,
                                              header=False)
            i += 1

