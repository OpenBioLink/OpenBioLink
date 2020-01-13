import os

import pandas

import openbiolink.train_test_set_creation.ttsConfig as ttsConst
from openbiolink import globalConfig as globConst


class TrainTestSetWriter():
    def __init__(self):
        self.folder_path = os.path.join(globConst.WORKING_DIR, ttsConst.TTS_FOLDER_NAME)
        os.makedirs(self.folder_path, exist_ok=True)

    def print_sets(self, train_val_set_tuples: list, test_set, nodes_in_train_val_set, nodes_in_test_set,
                   new_val_nodes=None, new_test_nodes=None):
        if new_test_nodes is None:
            new_test_nodes = []
        if new_val_nodes is None:
            new_val_nodes = [None] * len(train_val_set_tuples)

        num_folds = len(train_val_set_tuples)

        test_set[globConst.COL_NAMES_SAMPLES].to_csv(os.path.join(self.folder_path, ttsConst.TEST_FILE_NAME),
                                                     sep='\t',
                                                     index=False,
                                                     header=False)

        train_val_nodes_df = pandas.DataFrame({'id': list(nodes_in_train_val_set)})
        train_val_nodes_df['nodeType'] = [x[0] for x in train_val_nodes_df['id'].str.split('_')]
        train_val_nodes_df.to_csv(os.path.join(self.folder_path, ttsConst.TRAIN_VAL_NODES_FILE_NAME),
                                  sep='\t',
                                  index=False,
                                  header=False)
        test_nodes_df = pandas.DataFrame({'id': list(nodes_in_test_set)})
        test_nodes_df['nodeType'] = [x[0] for x in test_nodes_df['id'].str.split('_')]
        test_nodes_df.to_csv(os.path.join(self.folder_path, ttsConst.TEST_NODES_FILE_NAME),
                             sep='\t',
                             index=False,
                             header=False)

        if new_test_nodes:
            with open(os.path.join(self.folder_path, ttsConst.NEW_TEST_NODES_FILE_NAME), 'w', newline='\n') as file:
                file.writelines(list('\n'.join(new_test_nodes)))

        if num_folds > 1:
            t_set, v_set = train_val_set_tuples[0]
            fill_train_set = t_set.append(v_set)
            fill_train_set[globConst.COL_NAMES_SAMPLES].to_csv(os.path.join(self.folder_path, ttsConst.TRAIN_FILE_NAME),
                                                               sep='\t',
                                                               index=False,
                                                               header=False)
            self.folder_path = os.path.join(self.folder_path, ttsConst.CROSS_VAL_FOLDER_NAME)

        i = 0
        for (train_set, val_set), new_val_nodes_for_fold in zip(train_val_set_tuples, new_val_nodes):
            if num_folds > 1:
                fold_folder_path = os.path.join(self.folder_path, ttsConst.FOLD_FOLDER_PREFIX + str(i))
            else:
                fold_folder_path = self.folder_path
            os.makedirs(fold_folder_path, exist_ok=True)
            if not train_set.empty:
                train_set[globConst.COL_NAMES_SAMPLES].to_csv(os.path.join(fold_folder_path, ttsConst.TRAIN_FILE_NAME),
                                                              sep='\t',
                                                              index=False,
                                                              header=False)
            if not val_set.empty:
                val_set[globConst.COL_NAMES_SAMPLES].to_csv(os.path.join(fold_folder_path, ttsConst.VAL_FILE_NAME),
                                                            sep='\t',
                                                            index=False,
                                                            header=False)
            if new_val_nodes_for_fold:
                with open(os.path.join(fold_folder_path, ttsConst.NEW_VAL_NODES_FILE_NAME), 'w', newline='\n') as file:
                    file.writelines(list('\n'.join(new_val_nodes_for_fold)))

            i += 1

    def print_vanished_edges(self, vanished_edges):
        self.folder_path = os.path.join(globConst.WORKING_DIR, ttsConst.TTS_FOLDER_NAME)
        vanished_edges.to_csv(os.path.join(self.folder_path, ttsConst.VANISHED_FILE_NAME),
                              sep='\t',
                              index=False,
                              header=False)
