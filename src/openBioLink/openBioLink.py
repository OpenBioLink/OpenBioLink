import argparse
import cProfile
import logging
import os
import sys

from . import globalConfig as glob
from .graph_creation import graphCreationConfig as gcConst
from . import graphProperties as graphProp
from .graph_creation.types.qualityType import QualityType
from .graph_creation.graphCreation import Graph_Creation

from .train_test_set_creation.trainTestSplitCreation import TrainTestSetCreation


def create_graph(args):
    graphProp.DIRECTED = not args.undir
    graphProp.QUALITY = args.qual
    gcConst.INTERACTIVE_MODE = not args.no_interact
    gcConst.SKIP_EXISTING_FILES = args.skip

    use_db_metadata_classes = None
    use_edge_metadata_classes = None
    if args.dbs:
        db_module_names = ['.'.join(y) for y in [x.split('.')[0:-1] for x in args.dbs]]
        db_cls_names = [x.split('.')[-1] for x in args.dbs]
        use_db_metadata_classes = [getattr(sys.modules[module_name],cls_name) for module_name, cls_name in zip(db_module_names,db_cls_names)]
    if args.mes:
        db_module_names = ['.'.join(y) for y in [x.split('.')[0:-1] for x in args.mes]]
        db_cls_names = [x.split('.')[-1] for x in args.mes]
        use_edge_metadata_classes = [getattr(sys.modules[module_name],cls_name) for module_name, cls_name in zip(db_module_names,db_cls_names)]

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
                single_sep= single_sep.replace('n', '\n').replace('t','\t')
        else:
            single_sep = None
        if 'm' in args.out_format[0]:
            multisep_sep = args.out_format[1][args.out_format[0].index('m')]
            if multisep_sep == 'n' or multisep_sep == 't':
                multisep_sep= multisep_sep.replace('n', '\n').replace('t','\t')
        else:
            multisep_sep = None

        graph_creator.create_graph(one_file_sep=single_sep, multi_file_sep=multisep_sep, print_qscore=(not args.no_qscore))


def create_train_test_splits(args):
    if args.meta:
        pass
        #fixme read out triplets from path
    tts = TrainTestSetCreation(graph_path=args.edges,
                               tn_graph_path=args.tn_edges,
                               nodes_path=args.nodes,
                               meta_edge_triples=args.meta,
                               t_minus_one_graph_path=args.tmo_edges,
                               t_minus_one_tn_graph_path=args.tmo_tn_edges,
                               t_minus_one_nodes_path=args.tmo_nodes)
    tts.time_slice_split()
    #tts = TrainTestSetCreation(graph_path=args.edges, tn_graph_path=args.tn_edges, nodes_path=args.nodes, meta_edge_triples=args.meta)
    #tts.random_edge_split(val_frac=args.val_frac, test_frac=args.test_frac, crossval=args.crossval, folds=args.folds)



    #tts.random_edge_split(graph_path=args.edges, tn_graph_path=args.tn_edges, nodes_path=args.nodes,
    #                      val_frac=args.val_frac, test_frac=args.test_frac, crossval=args.crossval, folds=args.folds, meta_edge_triples=args.meta)
    #tts.random_edge_split('test\\test_data\\edges.csv', 'test\\test_data\\TN_edges.csv',  'test\\test_data\\nodes.csv', val_frac=0.2, test_frac = 0.2, crossval= None, folds = None)


def check_args_validity(args, parser):
    if not (args.g or args.s or args.c or args.t or args.e):
        parser.error("at least one action is required [-g, -s, -c, -t, -e]")
    if args.skip and args.no_interact is None:
        parser.error("option --skip requires --no_interact")
        #fixme


def main(args_list=None):
    if (len(sys.argv) < 2) and not args_list:
        glob.GUI_MODE = True
        from . import gui
        gui.start_gui()
        return

    parser = argparse.ArgumentParser('OpenBioLink Toolbox')

    # Global config
    parser.add_argument('-p', type=str, default= os.getcwd(),help='specify a working directory (default = current working dictionary')

    # Graph Creation
    parser.add_argument('-g', action='store_true', help='Generate Graph')
    parser.add_argument('--undir', action='store_true', help='Output-Graph should be undirectional (default = directional)')
    parser.add_argument('--qual', type=str, help= 'quality level od the output-graph, options = [hq, mq, lq], (default = None -> all entries are used)')
    parser.add_argument('--no_interact', action='store_true', help='Disables interactive mode - existing files will be replaced (default = interactive)')
    parser.add_argument('--skip', action='store_true', help='Existing files will be skipped - in combination with --no_interact (default = replace)')
    #todo list would be nicer
    parser.add_argument('--no_dl', action='store_true', help='No download is being performed (e.g. when local data is used)')
    parser.add_argument('--no_in', action='store_true', help='No input_files are created (e.g. when local data is used)')
    parser.add_argument('--no_create', action='store_true', help='No graph is created (e.g. when only in-files should be created)')
    parser.add_argument('--out_format', nargs=2,type=list, default='s t', help='Format of graph output, takes 2 arguments: list of file formats [s= single file, m=multiple files] and list of separators (e.g. t=tab, n=newline, or any other character) (default= s t)')
    parser.add_argument('--no_qscore', action='store_true', help='The output files will contain no scores')
    parser.add_argument('--dbs', nargs='+', help='custom source databases selection to be used, full class name, options --> see doc')
    parser.add_argument('--mes', nargs='+', help='custom meta edges selection to be used, full class name, options --> see doc')

    # Train- Test Split Generation
    parser.add_argument('-s', action='store_true', help='Generate Train-,Validation-, Test-Split')
    parser.add_argument('--edges', type=str, help='Path to edges.csv file (required with action -s')
    parser.add_argument('--tn_edges', type=str, help='Path to true_negatives_edges.csv file (required with action -s)')
    parser.add_argument('--nodes', type=str, help='Path to nodes.csv file (required with action -s)')
    parser.add_argument('--mode', type=str, help='Mode of train-test-set split, options=[rand, time]')

    parser.add_argument('--test_frac', type=float, default='0.2', help='Fraction of test set as float (default= 0.2)')
    parser.add_argument('--crossval', action='store_true', help='Multiple train-validation-sets are generated')
    parser.add_argument('--val', type=float, default='0.2',help='Fraction of validation set as float (default= 0.2) or number of folds as int')
    #parser.add_argument('--folds', type=int, default=0, help='Define the number of folds - if not specified, number is calculated via val_frac)')
    #parser.add_argument('--meta', type=str, help='Path to meta_edge triples (only required if meta-edges are not in BiMeG)')
    parser.add_argument('--tmo_edges', type=str, help='Path to edges.csv file of t-minus-one graph (required for --mode time')
    parser.add_argument('--tmo_tn_edges', type=str, help='Path to true_negatives_edges.csv file of t-minus-one graph (required for --mode time')
    parser.add_argument('--tmo_nodes', type=str, help='Path to nodes.csv file of t-minus-one graph (required for --mode time')

    # Hyperparameter Optimization
    parser.add_argument('-c', action='store_true', help='Apply hyperparameter optimization via cross validation')

    # Training
    parser.add_argument('-t', action='store_true', help='Apply Training')

    # Testing and Evaluation
    parser.add_argument('-e', action='store_true', help='Apply Test and Evaluation')

    #todo info from config file

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
    pr.print_stats( sort="time")