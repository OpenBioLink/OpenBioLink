import json
import os

import pandas

import openbiolink.evaluation.evalConfig as evalConst
from openbiolink import globalConfig as globConst


def write_mappings(node_label_to_id=None, node_types_to_id=None, relation_label_to_id=None):
    model_dir = os.path.join(os.path.join(globConst.WORKING_DIR, evalConst.EVAL_OUTPUT_FOLDER_NAME),
                             evalConst.MODEL_DIR)
    os.makedirs(model_dir, exist_ok=True)

    if node_label_to_id is not None:
        with open(os.path.join(model_dir, evalConst.MODEL_ENTITY_NAME_MAPPING_NAME), 'w') as file:
            json.dump(node_label_to_id, file, indent=4, sort_keys=True)
    if node_types_to_id is not None:
        with open(os.path.join(model_dir, evalConst.MODEL_ENTITY_TYPE_MAPPING_NAME), 'w') as file:
            json.dump(node_types_to_id, file, indent=4, sort_keys=True)
    if relation_label_to_id is not None:
        with open(os.path.join(model_dir, evalConst.MODEL_RELATION_TYPE_MAPPING_NAME), 'w') as file:
            json.dump(relation_label_to_id, file, indent=4, sort_keys=True)


def write_metric_results(metrics_results):
    eval_dir = os.path.join(globConst.WORKING_DIR, evalConst.EVAL_OUTPUT_FOLDER_NAME)
    os.makedirs(eval_dir, exist_ok=True)

    with open(os.path.join(eval_dir, evalConst.EVAL_OUTPUT_FILE_NAME), 'w') as fp:
        json_metrics = {x.value: y for x, y in metrics_results.items()}
        json.dump(json_metrics, fp, indent=4)


def read_mapping(path):
    with open(path) as f:
        string = f.read()
        return json.loads(string)


def read_corrupted_triples(path, sep='\t'):
    heads_path = os.path.join(path, evalConst.CORRUPTED_HEADS_FILE_NAME)
    tails_path = os.path.join(path, evalConst.CORRUPTED_TAILS_FILE_NAME)
    if os.path.exists(heads_path) and os.path.exists(tails_path):
        col_names = [evalConst.CORRUPTED_GROUP_COL_NAME,
                     globConst.NODE1_ID_COL_NAME,
                     globConst.EDGE_TYPE_COL_NAME,
                     globConst.NODE2_ID_COL_NAME,
                     globConst.VALUE_COL_NAME]
        all_corrupted_heads = pandas.read_csv(heads_path, names=col_names, sep=sep)
        all_corrupted_tails = pandas.read_csv(tails_path, names=col_names, sep=sep)
        head_groups = all_corrupted_heads[evalConst.CORRUPTED_GROUP_COL_NAME].unique()
        tail_groups = all_corrupted_tails[evalConst.CORRUPTED_GROUP_COL_NAME].unique()
        corrupted_head_dict = {}
        corrupted_tail_dict = {}
        for group in head_groups:
            df = all_corrupted_heads[all_corrupted_heads[evalConst.CORRUPTED_GROUP_COL_NAME] == group]
            df.drop(evalConst.CORRUPTED_GROUP_COL_NAME, axis=1)
            df.reset_index(drop=True, inplace=True)
            h, r, t, _ = tuple(df.iloc[0].values)
            corrupted_head_dict[(h, r, t)] = df
        for group in tail_groups:
            df = all_corrupted_tails[all_corrupted_tails[evalConst.CORRUPTED_GROUP_COL_NAME] == group]
            df.drop(evalConst.CORRUPTED_GROUP_COL_NAME, axis=1)
            df.reset_index(drop=True, inplace=True)
            h, r, t, _ = tuple(df.iloc[0].values)
            corrupted_tail_dict[(h, r, t)] = df
        return corrupted_head_dict, corrupted_tail_dict
