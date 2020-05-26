"""Command line interface for OpenBioLink.

Why does this file exist, and why not put this in ``__main__``? You might be tempted to import things from ``__main__``
later, but that will cause problems--the code will get executed twice:

- When you run ``python3 -m openbiolink`` python will execute``__main__.py`` as a script. That means there won't be any
  ``openbiolink.__main__`` in ``sys.modules``.
- When you import __main__ it will get executed again (as a module) because
  there's no ``openbiolink.__main__`` in ``sys.modules``.

.. seealso:: http://click.pocoo.org/5/setuptools/#setuptools-integration
"""

import logging
import os
import sys

import click

from openbiolink import globalConfig as glob
from openbiolink.cli_helper import create_graph, train_embedded, train_symbolic, evaluate_embedded, evaluate_symbolic
from openbiolink.evaluation.embedded.models.modelTypes import ModelTypes as EmbeddedModelTypes
from openbiolink.evaluation.symbolic.models.modelTypes import ModelTypes as SymbolicModelTypes
from openbiolink.graph_creation.graph_writer import FORMATS
from openbiolink.graph_creation.types.qualityType import QualityType
from openbiolink.train_test_set_creation.trainTestSplitCreation import TrainTestSetCreation

logger = logging.getLogger(__name__)


@click.group()
@click.option(
    "-p",
    "--directory",
    default=os.getcwd(),
    show_default=True,
    type=click.Path(dir_okay=True, file_okay=False),
    help="The output directory. Uses current if not given.",
)
def main(directory: str):
    """OpenBioLink CLI."""
    glob.WORKING_DIR = directory


@main.command()
def gui():
    """Run the OpenBioLink GUI."""
    glob.GUI_MODE = True
    from openbiolink.gui import gui

    gui.start_gui()


def handle_quality(_, __, qual):
    return QualityType.get_quality_type(qual)


@main.command()
@click.option("--undirected", is_flag=True, help="Output-Graph should be undirectional (default = directional)")
@click.option(
    "--qual",
    type=click.Choice(["hq", "mq", "lq", "nq"]),
    default="hq",
    callback=handle_quality,
    help="minimum quality level of the output-graph. If not specified, high quality is used.",
)
@click.option(
    "--no-interact",
    is_flag=True,
    help="Disables interactive mode - existing files will be replaced (default = interactive)",
)
@click.option("--skip", is_flag=True, help="Skip re-downloading existing files.")
@click.option("--no-download", is_flag=True, help="No download is being performed (e.g. when local data is used)")
@click.option("--no-input", is_flag=True, help="No input_files are created (e.g. when local data is used)")
@click.option("--no-create", is_flag=True, help="No graph is created (e.g. when only in-files should be created)")
@click.option("--no-qscore", is_flag=True, help="The output files will contain no scores")
@click.option(
    "--output-format",
    type=click.Choice(list(FORMATS)),
    default="TSV",
    show_default=True,
    help="Format of output files",
)
@click.option("--output-sep", help="The separator used in the output files. Defaults to tab")
@click.option(
    "--output-multi-file",
    is_flag=True,
    help="Edges and nodes are written to multiple files, "
    "instead of single files (accordingly grouped by edge type and node type)",
)
@click.option(
    "--dbs", multiple=True, help="custom source databases selection to be used, full class name, options --> see doc"
)
@click.option(
    "--mes", multiple=True, help="custom meta edges selection to be used, full class name, options --> see doc"
)
def generate(
    undirected: bool,
    qual: QualityType,
    no_interact: bool,
    skip: bool,
    no_download: bool,
    no_input: bool,
    no_create: bool,
    no_qscore: bool,
    output_format: str,
    output_sep: str,
    output_multi_file: bool,
    dbs,
    mes,
):
    """Generate a graph."""
    if no_input and not no_download and not no_create:
        click.secho(
            "Graph Creation: downloading graph files and creating the graph without creating in_files is not possible",
            fg="red",
        )
        sys.exit(-1)

    create_graph(
        directed=not undirected,
        quality_type=qual,
        interactive_mode=not no_interact,
        skip_existing_files=skip,
        do_download=not no_download,
        do_create_input_files=not no_input,
        do_create_graph=not no_create,
        qscore=not no_qscore,
        output_format=output_format,
        output_sep=output_sep,
        output_multi=output_multi_file,
        dbs=dbs,
        mes=mes,
    )


edges_option = click.option("--edges", required=True, help="Path to edges.csv file")
tn_edges_option = click.option("--tn-edges", required=True, help="Path to true_negatives_edges.csv file")
nodes_option = click.option("--nodes", required=True, help="Path to nodes.csv file")
sep_option = click.option("--sep", help="Separator of edge, tn-edge, and nodes file")


@main.group()
def split():
    """Split a graph."""


@split.command()
@edges_option
@tn_edges_option
@nodes_option
@click.option("--tmo-edges", required=True, help="Path to edges.csv file of t-minus-one graph")
@click.option("--tmo-tn-edges", required=True, help="Path to true_negatives_edges.csv file of t-minus-one graph")
@click.option("--tmo-nodes", required=True, help="Path to nodes.csv file of t-minus-one graph")
@sep_option
def time(edges, tn_edges, nodes, tmo_edges, tmo_tn_edges, tmo_nodes, sep):
    """Split based on time."""
    tts = TrainTestSetCreation(
        vars(glob),
        graph_path=edges,
        tn_graph_path=tn_edges,
        all_nodes_path=nodes,
        sep=sep,
        t_minus_one_graph_path=tmo_edges,
        t_minus_one_tn_graph_path=tmo_tn_edges,
        t_minus_one_nodes_path=tmo_nodes,
    )
    click.secho("Creating time slice split", fg="blue")
    tts.time_slice_split()


@split.command()
@edges_option
@tn_edges_option
@nodes_option
@sep_option
@click.option("--test-frac", type=float, show_default=True, default=0.05, help="Fraction of test set as float")
@click.option("--crossval", is_flag=True, help="Multiple train-validation-sets are generated")
@click.option(
    "--val",
    type=float,
    default=0.05,
    show_default=True,
    help="Fraction of validation set as float",
)
@click.option("--no-neg-train-val", is_flag=True, help="If flag is set, negative samples for the training/validation set are generated")
@click.option("--no-neg-test", is_flag=True, help="If flag is set, negative samples for the test set are generated")
def rand(edges, tn_edges, nodes, sep, test_frac, crossval, val, no_neg_train_val, no_neg_test):
    """Split randomly."""
    if crossval and (val == 0 or val == 1 or (val > 1 and not float(val).is_integer())):
        click.secho(
            "fold entry must be a float >0 and <1 (validation fraction)", fg="red",
        )
        sys.exit(-1)

    click.secho("Loading data")
    tts = TrainTestSetCreation(
        vars(glob),
        graph_path=edges,
        tn_graph_path=tn_edges,
        all_nodes_path=nodes,
        sep=sep,
        neg_train_val=not no_neg_train_val,
        neg_test=not no_neg_test
    )
    click.secho("Creating random slice split", fg="blue")
    tts.random_edge_split(val=val, test_frac=test_frac, crossval=crossval)


@main.group()
def train():
    """training"""

@train.command()
@click.option(
    "-m",
    "--model-cls",
    required=True,
    type=click.Choice(list(EmbeddedModelTypes.__members__)),
    help="class of the model to be trained/evaluated",
)
@click.option("--config", help="Path to the model' config file")
@click.option("-s", "--training-path", help="Path to positive trainings set file")  # (alternative: --cv_folder)')
@click.option("-ns", "--negative-training-path", help="Path to negative trainings set file")  # (alternative: --cv_folder)')
@click.option(
    "--nodes",
    help="path to the nodes file (required for ranked triples if no corrupted triples file is provided and nodes cannot be taken from graph creation",
)
def embedded(model_cls, training_path, negative_training_path, nodes, config):
    train_embedded(model_cls, training_path, negative_training_path, nodes, config)


@train.command()
@click.option(
    "-m",
    "--model-cls",
    required=True,
    type=click.Choice(list(SymbolicModelTypes.__members__)),
    help="class of the model to be trained/evaluated",
)
@click.option("-s", "--training-path", help="Path to positive trainings set file")
@click.option("-t", "--testing-path", required=True, help="Path to positive test set file")
@click.option("-v", "--valid-path", required=True, help="Path to positive validation set file")
@click.option("--policy", default=2, type=click.Choice(["1", "2"]), help="Possible values are 1 (greedy policy) and 2 (weighted policy).")
@click.option("--reward", default=5, type=click.Choice(["1", "3", "5"]), help="Possible values are 1 (correct predictions), 3 (correct predictions weighted by confidence with laplace smoothing), 5 (correct predictions weighted by confidence with laplace smoothing divided by (rule length-1)^2)")
@click.option("--epsilon", default=0.1, type=float, help="Allocates a core with a probability of 0.1 randomly. You can change this to a value of 0.0 to 1.0 (= random policy)")
@click.option("--snapshot-at", default=100, help="Specifies the amount of time used for learning rules")
@click.option("--worker-threads", default=7, help="Amount of threads that are started for learning rules")
def symbolic(model_cls, training_path, testing_path, valid_path, policy, reward, epsilon, snapshot_at, worker_threads):
    train_symbolic(model_cls, training_path, testing_path, valid_path, policy, reward, epsilon, snapshot_at, worker_threads)

@main.group()
def evaluate():
    """evaluation"""

@evaluate.command()
@click.option(
    "-m",
    "--model-cls",
    required=True,
    type=click.Choice(list(EmbeddedModelTypes.__members__)),
    help="class of the model to be trained/evaluated",
)
@click.option("--trained-model", help="Path to trained model", show_default=True, type=click.Path(dir_okay=False, file_okay=True), default="evaluation\\trained_model.pkl")
@click.option("--config", help="Path to the model' config file", show_default=True, type=click.Path(dir_okay=False, file_okay=True), default="evaluation\\configuration.json")
@click.option("-t", "--testing-path", help="Path to positive test set file", type=click.Path(dir_okay=False, file_okay=True))
@click.option("-nt", "--negative-testing-path", help="Path to negative test set file", type=click.Path(dir_okay=False, file_okay=True))
@click.option(
    "--nodes",
    help="path to the nodes file (required for ranked triples if no corrupted triples file is provided and nodes cannot be taken from graph creation",
    type=click.Path(dir_okay=False, file_okay=True)
)
@click.option("--metrics", multiple=True, help="evaluation metrics")
@click.option("--ks", multiple=True, help="k's for hits@k metric")
def embedded(model_cls, trained_model, config, testing_path, negative_testing_path, nodes, metrics, ks):
    trained_model = os.path.join(glob.WORKING_DIR, trained_model)
    config = os.path.join(glob.WORKING_DIR, config)
    evaluate_embedded(model_cls, trained_model, config, testing_path, negative_testing_path, nodes, metrics, ks)


@evaluate.command()
@click.option(
    "-m",
    "--model-cls",
    required=True,
    type=click.Choice(list(SymbolicModelTypes.__members__)),
    help="class of the model to be trained/evaluated",
)
@click.option("-s", "--training-path", required=True, help="Path to positive trainings set file")  # (alternative: --cv_folder)')
@click.option("-t", "--testing-path", required=True, help="Path to positive test set file")
@click.option("-v", "--valid-path", required=True, help="Path to positive validation set file")
@click.option("--snapshot-at", default=100, help="Specifies the learning time of the rule set")
@click.option("--discrimination-bound", type=int, default=1000, help="Returns only results for head or tail computation if the results set has less elements than this bound. The idea is that any results set which has more elements is anyhow not useful for a top-k ranking. Should be set to a value thats higher than the k of the requested top-k (however, the higher the value the more runtime is required)")
@click.option("--unseen-negative-examples", default=5, type=int, help="The number of negative examples for which we assume that they exist, however, we have not seen them. Rules with high coverage are favored the higher the chosen number.")
@click.option("--top-k-output", type=int, default=10,  help="The top-k results that are after filtering kept in the results.")
@click.option("--worker-threads", type=int, default=7, help="Amount of threads that are started to compute the ranked results.")
@click.option("--threshold-confidence", type=float, default=0.001, help="The threshold for the confidence of the refined rule")
@click.option("--no-fast", is_flag=True, help="If set the original rule engine is used (for each testtriple -> for each rule), otherwise a faster version is used which caches intermediate results and requires more memory")
@click.option("--discrimination-unique", is_flag=True, help="If set the unique results are calculated before discrimination.")
@click.option("--no-intermediate-discrimination", is_flag=True, help="If set only the final results are discriminated, but not intermediate results, see DISCRIMINATION_BOUND")
@click.option("--metrics", multiple=True, help="evaluation metrics")
@click.option("--ks", multiple=True, help="k's for hits@k metric")
def symbolic(
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
    evaluate_symbolic(
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
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
