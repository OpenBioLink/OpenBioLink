import os
from .. import globalConfig as globConst

COL_NAMES_SAMPLES = ''
class TrainTestSetWriter():
    def __init__(self, col_names_samples):
        global  COL_NAMES_SAMPLES
        COL_NAMES_SAMPLES = col_names_samples


    def print_sets(self, train_val_set_tuples:list, test_set, new_val_nodes=None, new_test_nodes=None):
        if new_test_nodes is None:
            new_test_nodes = []
        if new_val_nodes is None:
            new_val_nodes = [None]*len(train_val_set_tuples)

        num_folds = len(train_val_set_tuples)
        folder_path = os.path.join(globConst.WORKING_DIR, "train_test_data")
        os.makedirs(folder_path, exist_ok=True)

        test_set[COL_NAMES_SAMPLES].to_csv(os.path.join(folder_path, "test_sample.csv"),
                                           sep='\t',
                                           index=False,
                                           header=False)
        if new_test_nodes:
            with open(os.path.join(folder_path, "new_test_nodes.csv"), 'w', newline='\n') as file:
                file.writelines(list('\n'.join(new_test_nodes)))


        if num_folds>1:
            folder_path = os.path.join(folder_path, "cross_val")
        i = 0
        for (train_set, val_set), new_val_nodes_for_fold in zip(train_val_set_tuples,new_val_nodes):
            if num_folds > 1:
                fold_folder_path = os.path.join(folder_path, "fold_%d" % (i))
            else:
                fold_folder_path = folder_path
            os.makedirs(fold_folder_path, exist_ok=True)
            if not train_set.empty :
                train_set[COL_NAMES_SAMPLES].to_csv(os.path.join(fold_folder_path, "train_sample.csv"),
                                                    sep='\t',
                                                    index=False,
                                                    header=False)
            if not val_set.empty:
                val_set[COL_NAMES_SAMPLES].to_csv(os.path.join(fold_folder_path, "val_sample.csv"),
                                                  sep='\t',
                                                  index=False,
                                                  header=False)
            if new_val_nodes_for_fold:
                with open(os.path.join(fold_folder_path, "new_val_nodes.csv"), 'w', newline='\n') as file:
                    file.writelines(list('\n'.join(new_val_nodes_for_fold)))

            i += 1

