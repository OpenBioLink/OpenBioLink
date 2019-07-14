import os
import globalConfig as globConst
import train_test_set_creation.ttsConfig as ttsConst

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
        folder_path = os.path.join(globConst.WORKING_DIR, ttsConst.TTS_FOLDER_NAME)
        os.makedirs(folder_path, exist_ok=True)

        test_set[COL_NAMES_SAMPLES].to_csv(os.path.join(folder_path, ttsConst.TEST_FILE_NAME),
                                           sep='\t',
                                           index=False,
                                           header=False)
        if new_test_nodes:
            with open(os.path.join(folder_path, ttsConst.NEW_TEST_NODES_FILE_NAME), 'w', newline='\n') as file:
                file.writelines(list('\n'.join(new_test_nodes)))


        if num_folds>1:
            t_set, v_set = train_val_set_tuples[0]
            fill_train_set = t_set.append(v_set)
            fill_train_set[COL_NAMES_SAMPLES].to_csv(os.path.join(folder_path, ttsConst.TRAIN_FILE_NAME),
                                                sep='\t',
                                                index=False,
                                                header=False)
            folder_path = os.path.join(folder_path, ttsConst.CROSS_VAL_FOLDER_NAME)

        i = 0
        for (train_set, val_set), new_val_nodes_for_fold in zip(train_val_set_tuples,new_val_nodes):
            if num_folds > 1:
                fold_folder_path = os.path.join(folder_path, ttsConst.FOLD_FOLDER_PREFIX +str(i))
            else:
                fold_folder_path = folder_path
            os.makedirs(fold_folder_path, exist_ok=True)
            if not train_set.empty :
                train_set[COL_NAMES_SAMPLES].to_csv(os.path.join(fold_folder_path, ttsConst.TRAIN_FILE_NAME),
                                                    sep='\t',
                                                    index=False,
                                                    header=False)
            if not val_set.empty:
                val_set[COL_NAMES_SAMPLES].to_csv(os.path.join(fold_folder_path, ttsConst.VAL_FILE_NAME),
                                                  sep='\t',
                                                  index=False,
                                                  header=False)
            if new_val_nodes_for_fold:
                with open(os.path.join(fold_folder_path, ttsConst.NEW_VAL_NODES_FILE_NAME), 'w', newline='\n') as file:
                    file.writelines(list('\n'.join(new_val_nodes_for_fold)))

            i += 1

