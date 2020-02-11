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
from openbiolink.cli_helper import create_graph, train_and_evaluate
from openbiolink.graph_creation.types.qualityType import QualityType
from openbiolink.train_test_set_creation.trainTestSplitCreation import TrainTestSetCreation

logger = logging.getLogger(__name__)


@click.group()
@click.option("-p", "--directory", default=os.getcwd(), help="the working directory")
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
    type=click.Choice(["hq", "mq", "lq"]),
    default="lq",
    show_default=True,
    callback=handle_quality,
    help="quality level od the output-graph (default = None -> all entries are used)",
)
@click.option(
    "--no-interact",
    is_flag=True,
    help="Disables interactive mode - existing files will be replaced (default = interactive)",
)
@click.option(
    "--skip",
    is_flag=True,
    help="Existing files will be skipped - in combination with --no_interact (default = replace)",
)
@click.option("--no-download", is_flag=True, help="No download is being performed (e.g. when local data is used)")
@click.option("--no-input", is_flag=True, help="No input_files are created (e.g. when local data is used)")
@click.option("--no-create", is_flag=True, help="No graph is created (e.g. when only in-files should be created)")
@click.option("--no-qscore", is_flag=True, help="The output files will contain no scores")
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
        dbs=dbs,
        mes=mes,
    )


edges_option = click.option("--edges", required=True, help="Path to edges.csv file")
tn_edges_option = click.option("--tn-edges", required=True, help="Path to true_negatives_edges.csv file")
nodes_option = click.option("--nodes", required=True, help="Path to nodes.csv file")
sep_option = click.option("--sep", default="\t", show_default=True, help="Separator of edge, tn-edge, and nodes file")


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
@click.option("--test-frac", type=float, show_default=True, default=0.2, help="Fraction of test set as float")
@click.option("--crossval", is_flag=True, help="Multiple train-validation-sets are generated")
@click.option(
    "--val",
    type=float,
    default=0.2,
    show_default=True,
    help="Fraction of validation set as float or number of folds as int",
)
def rand(edges, tn_edges, nodes, sep, test_frac, crossval, val):
    """Split randomly."""
    if crossval and (val == 0 or val == 1 or (val > 1 and not float(val).is_integer())):
        click.secho(
            "fold entry must be either an int>1 (number of folds) or a float >0 and <1 (validation fraction)", fg="red",
        )
        sys.exit(-1)

    click.secho("Loading data")
    tts = TrainTestSetCreation(graph_path=edges, tn_graph_path=tn_edges, all_nodes_path=nodes, sep=sep,)
    click.secho("Creating random slice split", fg="blue")
    tts.random_edge_split(val=val, test_frac=test_frac, crossval=crossval)


@main.command()
@click.option("--model-cls", help="class of the model to be trained/evaluated (required with -e)")
@click.option("--config", help="Path to the model' config file")
@click.option("--no-train", is_flag=True, help="No training is being performed, trained model id provided via --model")
@click.option("--trained-model", help="Path to trained model (required with --no-train)")
@click.option("--no-eval", is_flag=True, help="No evaluation is being performed, only training")
@click.option("--test", help="Path to test set file (required with -e)")
@click.option("--train", help="Path to trainings set file")  # (alternative: --cv_folder)')
@click.option(
    "--corrupted", help="path to the corrupted triples (required for ranked triples if no nodes file is provided",
)  # fixme no longer an option
@click.option(
    "--eval-nodes",
    help="path to the nodes file (required for ranked triples if no corrupted triples file is provided and nodes cannot be taken from graph creation",
)
@click.option("--metrics", multiple=True, help="evaluation metrics")
@click.option("--ks", multiple=True, help="k's for hits@k metric")
def train(
    model_cls, trained_model, train, test, eval_nodes, no_train, no_eval, metrics, ks, config,
):
    """Train and evaluate on a graph."""
    train_and_evaluate(
        model_cls=model_cls,
        trained_model=trained_model,
        training_set_path=train,
        test_set_path=test,
        nodes_path=eval_nodes,
        do_training=not no_train,
        do_evaluation=not no_eval,
        metrics=metrics,
        ks=ks,
        config=config,
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
