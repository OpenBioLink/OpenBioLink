import itertools
import logging
import sys
from typing import List, Optional

from openbiolink import globalConfig, globalConfig as glob, graphProperties as graphProp
from openbiolink.evaluation.evaluation import Evaluation
from openbiolink.evaluation.metricTypes import RankMetricType, ThresholdMetricType
from openbiolink.evaluation.models.modelTypes import ModelTypes
from openbiolink.graph_creation.graphCreation import GraphCreator
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
    quality_type: Optional[QualityType] = None,
    output_format: Optional[str] = None,
    output_single_sep: Optional[str] = None,
    output_multisep_sep: Optional[str] = None,
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

    graph_creator = GraphCreator(
        folder_path=glob.WORKING_DIR,
        use_db_metadata_classes=use_db_metadata_classes,
        use_edge_metadata_classes=use_edge_metadata_classes,
    )

    logging.info("###### (1) GRAPH CREATION ######")
    if do_download:
        print("\n\n############### downloading files #################################")
        logging.info("## Start downloading files ##")
        graph_creator.download_db_files()

    if do_create_input_files:
        print("\n\n############### creating graph input files #################################")
        logging.info("## Start creating input files ##")
        graph_creator.create_input_files()

    if do_create_graph:
        print("\n\n############### creating graph #################################")
        logging.info("## Start creating graph ##")
        graph_creator.create_graph(
            format=output_format,
            one_file_sep=output_single_sep,
            multi_file_sep=output_multisep_sep,
            print_qscore=qscore,
        )

        # with open(os.path.join(globalConfig.WORKING_DIR, globalConfig.GRAPH_PROP_FILE_NAME), 'w') as f:
        #    graph_prop_dict  = {x: y for x, y in graphProp.__dict__.items() if not x.startswith('__')}
        #    for k,v in  graph_prop_dict.items():
        #        if not type(v)==str:
        #            graph_prop_dict[k] = str(v)
        #    json.dump(graph_prop_dict, f, indent=4)


def train_and_evaluate(
    model_cls: str,
    trained_model,
    training_set_path,
    test_set_path,
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

    e = Evaluation(
        model=model,
        training_set_path=training_set_path,
        test_set_path=test_set_path,
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
            itertools.chain(RankMetricType.__members__.values(), ThresholdMetricType.__members__.values(), )
        )
        if metrics is not None:
            metrics_to_use = [x for x in metrics_to_use if x.name in metrics]
        if ks is None:
            int_ks = [1, 3, 5, 10]
        else:
            int_ks = [int(k) for k in ks]
        e.evaluate(metrics=metrics_to_use, ks=int_ks)
