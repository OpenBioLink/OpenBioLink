import itertools
import logging
import sys
from typing import List, Optional

from openbiolink import globalConfig, globalConfig as glob, graphProperties as graphProp
from openbiolink.evaluation.training import Training
from openbiolink.evaluation.metricTypes import RankMetricType, ThresholdMetricType
from openbiolink.evaluation.models.modelTypes import ModelTypes
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


def train_and_evaluate(
    model_cls: str,
    trained_model,
    training_set_path,
    negative_training_set_path,
    validation_set_path,
    negative_validation_set_path,
    test_set_path,
    negative_test_set_path,
    nodes_path,
    do_training,
    do_evaluation,
    metrics=None,
    ks=None,
    config=None,
):
    model_cls = ModelTypes[model_cls].value
    if trained_model:  # fixme when model provided, config also has to be
        model = model_cls()
        model.kge_model = model_cls.load_model(config)
        # model.kge_model.load_state_dict(torch.load(trained_model))
        # testme
    elif config:
        model = model_cls(config)
    else:
        model = model_cls()

    e = Training(
        model=model,
        training_set_path=training_set_path,
        negative_training_set_path=negative_training_set_path,
        valid_set_path=validation_set_path,
        negative_valid_set_path=negative_validation_set_path,
        test_set_path=test_set_path,
        negative_test_set_path=negative_test_set_path,
        nodes_path=nodes_path,
        mappings_avail=bool(trained_model),
    )
    # todo doku: mappings have to be in model folder with correct name, or change here
    if do_training:
        print("starting training")
        e.train()
    if do_evaluation:
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
        e.evaluate(metrics=metrics_to_use, ks=int_ks)
