import itertools
import logging
import sys
from typing import List, Optional

from openbiolink import globalConfig, globalConfig as glob, graphProperties as graphProp
from openbiolink.evaluation.embedded.embeddedTraining import EmbeddedTraining
from openbiolink.evaluation.embedded.embeddedEvaluation import EmbeddedEvaluation
from openbiolink.evaluation.symbolic.symbolicTraining import SymbolicTraining
from openbiolink.evaluation.symbolic.symbolicEvaluation import SymbolicEvaluation
from openbiolink.evaluation.dataset import Dataset
from openbiolink.evaluation.metricTypes import RankMetricType, ThresholdMetricType
from openbiolink.evaluation.embedded.models.modelTypes import ModelTypes as EmbeddedModelTypes
from openbiolink.evaluation.symbolic.models.modelTypes import ModelTypes as SymbolicModelTypes
from openbiolink.graph_creation.graphCreation import Graph_Creation
from openbiolink.graph_creation.types.qualityType import QualityType


def create_graph(
        directed: bool,
        dbs: List[str],
        mes: List[str],
        qscore,
        skip_existing_files: bool,
        interactive_mode: bool,
        do_download=True,
        do_create_input_files=True,
        do_create_graph=True,
        output_multi=False,
        quality_type: Optional[QualityType] = None,
        output_format: Optional[str] = None,
        output_sep: Optional[str] = None,
):
    graphProp.DIRECTED = directed
    graphProp.QUALITY = quality_type
    globalConfig.INTERACTIVE_MODE = interactive_mode
    globalConfig.SKIP_EXISTING_FILES = skip_existing_files

    # todo via enums
    use_db_metadata_classes = None
    if dbs:
        db_module_names = [".".join(y) for y in [x.split(".")[0:-1] for x in dbs]]
        db_cls_names = [x.split(".")[-1] for x in dbs]
        use_db_metadata_classes = [
            getattr(sys.modules[module_name], cls_name) for module_name, cls_name in zip(db_module_names, db_cls_names)
        ]

    use_edge_metadata_classes = None
    if mes:
        db_module_names = [".".join(y) for y in [x.split(".")[0:-1] for x in mes]]
        db_cls_names = [x.split(".")[-1] for x in mes]
        use_edge_metadata_classes = [
            getattr(sys.modules[module_name], cls_name) for module_name, cls_name in zip(db_module_names, db_cls_names)
        ]

    graph_creator = Graph_Creation(
        folder_path=glob.WORKING_DIR,
        use_db_metadata_classes=use_db_metadata_classes,
        use_edge_metadata_classes=use_edge_metadata_classes,
    )

    logging.info("###### (1) GRAPH CREATION ######")
    if do_download:
        graph_creator.download_db_files()

    if do_create_input_files:
        graph_creator.create_input_files()

    if do_create_graph:
        graph_creator.create_graph(
            format=output_format, file_sep=output_sep, multi_file=output_multi, print_qscore=qscore,
        )
    logging.info("##### Graph creation done! #####")


def train_embedded(
        model_cls: str,
        training_path,
        negative_training_path,
        nodes,
        config
):
    model_cls = EmbeddedModelTypes[model_cls].value
    if config:
        model = model_cls(config)
    else:
        model = model_cls()

    print("starting training")

    dataset = Dataset(
        training_set_path=training_path,
        negative_training_set_path=negative_training_path,
        nodes_path=nodes
    )

    e = EmbeddedTraining(
        model=model,
        dataset=dataset
    )

    e.train()


def evaluate_embedded(
        model_cls: str,
        trained_model,
        config,
        testing_path,
        negative_testing_path,
        nodes,
        metrics,
        ks
):
    model_cls = EmbeddedModelTypes[model_cls].value
    model = model_cls()
    model.kge_model = model_cls.load_model(config)

    print("starting evaluation")
    metrics_to_use = list(
        itertools.chain(RankMetricType.__members__.values(), ThresholdMetricType.__members__.values())
    )
    if metrics is not None:
        metrics_to_use = [x for x in metrics_to_use if x.name in metrics]
    if ks is None:
        int_ks = [1, 3, 5, 10]
    else:
        int_ks = [int(k) for k in ks]

    dataset = Dataset(
        test_set_path=testing_path,
        negative_test_set_path=negative_testing_path,
        nodes_path=nodes,
        mappings_avail=True
    )
    e = EmbeddedEvaluation(model, dataset)
    e.evaluate(metrics=metrics_to_use, ks=int_ks)


def train_symbolic(model_cls, training_path, testing_path, valid_path, policy, reward, epsilon, snapshot_at,
                   worker_threads):
    model_cls = SymbolicModelTypes[model_cls].value
    model = model_cls()
    model.config["policy"] = policy
    model.config["reward"] = reward
    model.config["epsilon"] = epsilon
    model.config["snapshot_at"] = snapshot_at
    model.config["worker_threads"] = worker_threads

    print("starting training")
    dataset = Dataset(
        training_set_path=training_path,
        test_set_path=testing_path,
        valid_set_path=valid_path,
        mapping=False,
        write_triples=True
    )

    e = SymbolicTraining(model, dataset)
    e.train()


def evaluate_symbolic(
        model_cls,
        training_path,
        testing_path,
        valid_path,
        snapshot_at,
        discrimination_bound,
        unseen_negative_examples,
        top_k_output,
        worker_threads,
        threshold_confidence,
        no_fast,
        discrimination_unique,
        no_intermediate_discrimination,
        metrics,
        ks
):
    model_cls = SymbolicModelTypes[model_cls].value
    model = model_cls()

    model.config["snapshot_at"] = snapshot_at
    model.config["discrimination_bound"] = discrimination_bound
    model.config["unseen_negative_examples"] = unseen_negative_examples
    model.config["top_k_output"] = top_k_output
    model.config["worker_threads"] = worker_threads
    model.config["threshold_confidence"] = threshold_confidence
    model.config["fast"] = not no_fast
    model.config["discrimination_unique"] = discrimination_unique
    model.config["intermediate_discrimination"] = not no_intermediate_discrimination

    print("starting evaluation")
    metrics_to_use = list(
        itertools.chain(RankMetricType.__members__.values(), ThresholdMetricType.__members__.values())
    )
    if metrics is not None:
        metrics_to_use = [x for x in metrics_to_use if x.name in metrics]
    if ks is None:
        int_ks = [1, 3, 5, 10]
    else:
        int_ks = [int(k) for k in ks]

    dataset = Dataset(
        training_set_path=training_path,
        test_set_path=testing_path,
        valid_set_path=valid_path,
        mapping=False,
        write_triples=True
    )

    e = SymbolicEvaluation(model, dataset)
    e.evaluate(metrics=metrics_to_use, ks=int_ks)
