import itertools
import logging
import sys
from typing import List, Optional

from openbiolink import globalConfig, globalConfig as glob, graphProperties as graphProp
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
