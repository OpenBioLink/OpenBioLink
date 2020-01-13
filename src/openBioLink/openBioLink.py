import argparse
import cProfile
import logging
import os
import sys

import openbiolink.graphProperties as graphProp
from openbiolink import globalConfig
from openbiolink import globalConfig as glob
from openbiolink.evaluation.evaluation import Evaluation
from openbiolink.evaluation.metricTypes import RankMetricType, ThresholdMetricType
from openbiolink.evaluation.models.modelTypes import ModelTypes
from openbiolink.graph_creation.graphCreation import Graph_Creation
from openbiolink.graph_creation.types.qualityType import QualityType
from openbiolink.train_test_set_creation.trainTestSplitCreation import TrainTestSetCreation


def create_graph(args):
    graphProp.DIRECTED = not args.undir
    graphProp.QUALITY = args.qual
    globalConfig.INTERACTIVE_MODE = not args.no_interact
    globalConfig.SKIP_EXISTING_FILES = args.skip

    use_db_metadata_classes = None
    use_edge_metadata_classes = None
    # todo via enums
    if args.dbs:
        db_module_names = ['.'.join(y) for y in [x.split('.')[0:-1] for x in args.dbs]]
        db_cls_names = [x.split('.')[-1] for x in args.dbs]
        use_db_metadata_classes = [getattr(sys.modules[module_name], cls_name) for module_name, cls_name in
                                   zip(db_module_names, db_cls_names)]
    if args.mes:
        db_module_names = ['.'.join(y) for y in [x.split('.')[0:-1] for x in args.mes]]
        db_cls_names = [x.split('.')[-1] for x in args.mes]
        use_edge_metadata_classes = [getattr(sys.modules[module_name], cls_name) for module_name, cls_name in
                                     zip(db_module_names, db_cls_names)]

    graph_creator = Graph_Creation(folder_path=glob.WORKING_DIR,
                                   use_db_metadata_classes=use_db_metadata_classes,
                                   use_edge_metadata_classes=use_edge_metadata_classes)

    logging.info('###### (1) GRAPH CREATION ######')
    if not args.no_dl:
        print("\n\n############### downloading files #################################")
        logging.info('## Start downloading files ##')
        graph_creator.download_db_files()

    if not args.no_in:
        print("\n\n############### creating graph input files #################################")
        logging.info('## Start creating input files ##')
        graph_creator.create_input_files()

    if not args.no_create:
        print("\n\n############### creating graph #################################")
        logging.info('## Start creating graph ##')
        if 's' in args.out_format[0]:
            single_sep = args.out_format[1][args.out_format[0].index('s')]
            if single_sep == 'n' or single_sep == 't':
                single_sep = single_sep.replace('n', '\n').replace('t', '\t')
        else:
            single_sep = None
        if 'm' in args.out_format[0]:
            multisep_sep = args.out_format[1][args.out_format[0].index('m')]
            if multisep_sep == 'n' or multisep_sep == 't':
                multisep_sep = multisep_sep.replace('n', '\n').replace('t', '\t')
        else:
            multisep_sep = None

        graph_creator.create_graph(one_file_sep=single_sep, multi_file_sep=multisep_sep,
                                   print_qscore=(not args.no_qscore))

        # with open(os.path.join(globalConfig.WORKING_DIR, globalConfig.GRAPH_PROP_FILE_NAME), 'w') as f:
        #    graph_prop_dict  = {x: y for x, y in graphProp.__dict__.items() if not x.startswith('__')}
        #    for k,v in  graph_prop_dict.items():
        #        if not type(v)==str:
        #            graph_prop_dict[k] = str(v)
        #    json.dump(graph_prop_dict, f, indent=4)


def create_train_test_splits(args):
    if args.tts_sep == 't':
        sep = '\t'
    elif args.tts_sep == 'n':
        sep = '\n'
    else:
        sep = args.tts_sep
    tts = TrainTestSetCreation(graph_path=args.edges,
                               tn_graph_path=args.tn_edges,
                               all_nodes_path=args.nodes,
                               sep=sep,
                               # meta_edge_triples=args.meta,
                               t_minus_one_graph_path=args.tmo_edges,
                               t_minus_one_tn_graph_path=args.tmo_tn_edges,
                               t_minus_one_nodes_path=args.tmo_nodes)
    if args.mode == 'time':
        print("\n\n############### creating time slice split #################################")
        logging.info('## Start creating time slice split ##')
        tts.time_slice_split()
    elif args.mode == 'rand':
        print("\n\n############### creating random slice split #################################")
        logging.info('## Start creating random slice split ##')
        tts.random_edge_split(val=args.val, test_frac=args.test_frac, crossval=args.crossval)
    # tts.random_edge_split(crossval=False)


def train_and_evaluate(args):
    model_cls = ModelTypes[args.model_cls].value
    if args.trained_model:  # fixme when model provided, config also has to be
        if args.config:
            config = args.config
            # model = model_cls(args.config)
        else:
            config = None
        model = model_cls()
        model.kge_model = model_cls.load_model(config)
        # model.kge_model.load_state_dict(torch.load(args.trained_model))
        # testme
    elif args.config:
        model = model_cls(args.config)
    else:
        model = model_cls()
    e = Evaluation(model=model, training_set_path=args.train, test_set_path=args.test, nodes_path=args.eval_nodes,
                   mappings_avail=bool(args.trained_model))
    # todo doku: mappings have to be in model folder with correct name, or change here
    if not args.no_train:
        print('starting training')
        e.train()
    if not args.no_eval:
        print('starting evaluation')

        metric_strings = args.metrics
        metrics = [x for x in list(RankMetricType.__members__.values()) if x.name in metric_strings] + \
                  [x for x in list(ThresholdMetricType.__members__.values()) if x.name in metric_strings]
        int_ks = [int(k) for k in args.ks]

        e.evaluate(metrics=metrics, ks=int_ks)


def check_args_validity(args, parser):
    # global checks
    if not (args.g or args.s or args.e):
        parser.error("at least one action is required [-g, -s, -e]")
    if args.skip and args.no_interact is None:
        parser.error("option --skip requires --no_interact")
    # graph creation checks
    if args.g:
        if args.no_in and not args.no_dl and not args.no_create:
            parser.error(
                "Graph Creation: downloading graph files and creating the graph without creating in_files is not possible")
    # train test split checks
    if args.s:
        if not args.edges or not args.tn_edges or not args.nodes:
            parser.error("Train Test Split: paths to the edge file (--edges), negative edge file (--tn_edges) "
                         "and nodes file (--nodes) must be provided with option -s")
        if args.crossval:
            n_folds = args.val
            if n_folds == 0 or n_folds == 1 or (n_folds > 1 and not float(n_folds).is_integer()):
                parser.error(
                    "fold entry must be either an int>1 (number of folds) or a float >0 and <1 (validation fraction)")
        if args.mode == 'time':
            if not (bool(args.tmo_edges) and bool(args.tmo_tn_edges) and (bool(args.tmo_nodes))):
                parser.error(
                    'for time slice mode, edge-, tn-edge- and node-file of the t-minus-one graph must be provided')
    # if args.crossval and (not args.tmo_edges or not args.tmo_tn_edges or not args.tmo_nodes):
    #            parser.error("Train Test Split: paths to the t-1 edge file (--tmo_edges),"
    #                         " t-1 negative edge file (--tmo_tn_edges) and t-1 nodes file (--tmo_nodes) "
    #                         "must be provided with option --crossval") #todo what?


def main(args_list=None):
    if (len(sys.argv) < 2) and not args_list:
        glob.GUI_MODE = True
        import openbiolink.gui.gui as gui
        gui.start_gui()
        return

    parser = argparse.ArgumentParser('OpenBioLink Toolbox')

    # Global config
    parser.add_argument('-p', type=str, default=os.getcwd(),
                        help='specify a working directory (default = current working dictionary')

    # Graph Creation
    parser.add_argument('-g', action='store_true', help='Generate Graph')
    parser.add_argument('--undir', action='store_true',
                        help='Output-Graph should be undirectional (default = directional)')
    parser.add_argument('--qual', type=str,
                        help='quality level od the output-graph, options = [hq, mq, lq], (default = None -> all entries are used)')
    parser.add_argument('--no_interact', action='store_true',
                        help='Disables interactive mode - existing files will be replaced (default = interactive)')
    parser.add_argument('--skip', action='store_true',
                        help='Existing files will be skipped - in combination with --no_interact (default = replace)')
    parser.add_argument('--no_dl', action='store_true',
                        help='No download is being performed (e.g. when local data is used)')
    parser.add_argument('--no_in', action='store_true',
                        help='No input_files are created (e.g. when local data is used)')
    parser.add_argument('--no_create', action='store_true',
                        help='No graph is created (e.g. when only in-files should be created)')
    parser.add_argument('--out_format', nargs=2, type=list, default='s t',
                        help='Format of graph output, takes 2 arguments: list of file formats [s= single file, m=multiple files] and list of separators (e.g. t=tab, n=newline, or any other character) (default= s t)')
    parser.add_argument('--no_qscore', action='store_true', help='The output files will contain no scores')
    parser.add_argument('--dbs', nargs='+',
                        help='custom source databases selection to be used, full class name, options --> see doc')
    parser.add_argument('--mes', nargs='+',
                        help='custom meta edges selection to be used, full class name, options --> see doc')

    # Train- Test Split Generation
    parser.add_argument('-s', action='store_true', help='Generate Train-,Validation-, Test-Split')
    parser.add_argument('--edges', type=str, help='Path to edges.csv file (required with action -s')
    parser.add_argument('--tn_edges', type=str, help='Path to true_negatives_edges.csv file (required with action -s)')
    parser.add_argument('--nodes', type=str, help='Path to nodes.csv file (required with action -s)')
    parser.add_argument('--tts_sep', type=str, default='t',
                        help='Separator of edge, tn-edge and nodes file (e.g. t=tab, n=newline, or any other character) (default=t)')
    parser.add_argument('--mode', type=str, default='rand',
                        help='Mode of train-test-set split, options=[rand, time], (default=rand)')
    parser.add_argument('--test_frac', type=float, default='0.2', help='Fraction of test set as float (default= 0.2)')
    parser.add_argument('--crossval', action='store_true', help='Multiple train-validation-sets are generated')
    parser.add_argument('--val', type=float, default='0.2',
                        help='Fraction of validation set as float (default= 0.2) or number of folds as int')
    # niceToHave (1)
    # parser.add_argument('--meta', type=str, help='Path to meta_edge triples (only required if meta-edges are not in OpenBioLink Benchmark Data)')
    parser.add_argument('--tmo_edges', type=str,
                        help='Path to edges.csv file of t-minus-one graph (required for --mode time')
    parser.add_argument('--tmo_tn_edges', type=str,
                        help='Path to true_negatives_edges.csv file of t-minus-one graph (required for --mode time')
    parser.add_argument('--tmo_nodes', type=str,
                        help='Path to nodes.csv file of t-minus-one graph (required for --mode time')

    # Training and Evaluation
    parser.add_argument('-e', action='store_true', help='Apply Training and Evaluation')
    parser.add_argument('--model_cls', type=str, help='class of the model to be trained/evaluated (required with -e)')
    parser.add_argument('--config', type=str, help='Path to the model\' config file')
    parser.add_argument('--no_train', action='store_true',
                        help='No training is being performed, trained model id provided via --model')
    parser.add_argument('--trained_model', type=str, help='Path to trained model (required with --no_train)')
    parser.add_argument('--no_eval', action='store_true', help='No evaluation is being performed, only training')
    parser.add_argument('--test', type=str, help='Path to test set file (required with -e)')
    parser.add_argument('--train', type=str, help='Path to trainings set file')  # (alternative: --cv_folder)')
    parser.add_argument('--corrupted', type=str,
                        help='path to the corrupted triples (required for ranked triples if no nodes file is provided')  # fixme no longer an option
    parser.add_argument('--eval_nodes', type=str,
                        help='path to the nodes file (required for ranked triples if no corrupted triples file is provided and nodes cannot be taken from graph creation')
    parser.add_argument('--metrics', nargs='+', help='evaluation metrics')
    parser.add_argument('--ks', nargs='+', help='k\'s for hits@k metric')
    # parser.add_argument('--cv_folder', type=str, help='Path to cross validation folder (alternative: --train)')

    # niceToHave (7) option to load info from config file

    if args_list:
        args = parser.parse_args(args_list)
    else:
        args = parser.parse_args()

    check_args_validity(args, parser)
    glob.WORKING_DIR = args.p

    if args.qual == 'hq':
        args.qual = QualityType.HQ
    elif args.qual == 'mq':
        args.qual = QualityType.MQ
    elif args.qual == 'lq':
        args.qual = QualityType.LQ

    if args.g:
        create_graph(args)
    if args.s:
        create_train_test_splits(args)
    if args.e:
        train_and_evaluate(args)

    logging.info('Finished!')


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel('INFO')
    pr = cProfile.Profile()
    pr.enable()
    main()
    base_dir = os.path.dirname(os.path.realpath(__file__))
    test_folder = os.path.join(base_dir, 'test')

    pr.disable()
    pr.print_stats(sort="time")

    # todo crossval eval
