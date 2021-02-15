# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import re
import sys
from datetime import date

sys.path.insert(0, os.path.abspath('../../src'))


# -- Project information -----------------------------------------------------

project = 'OpenBioLink'
copyright = '2021, Anna Breit, Simon Ott, Laura Graf, Matthias Samwald'
author = 'Anna Breit, Simon Ott, Laura Graf, Matthias Samwald'

# The full version, including alpha/beta/rc tags
release = '0.1.4'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autosummary',
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
    'sphinx.ext.intersphinx',
    "sphinx.ext.todo",
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinx_autodoc_typehints',
    'sphinx_click.ext',
    'sphinx_automodapi.automodapi',
    'texext',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

intersphinx_mapping = {
    'https://docs.python.org/3/': None,
    'torch': ('https://pytorch.org/docs/stable', None),
    'numpy': ('https://numpy.org/doc/stable', None),
    'optuna': ('https://optuna.readthedocs.io/en/latest', None),
    'pybel': ('https://pybel.readthedocs.io/en/latest/', None),
    'bio2bel': ('https://bio2bel.readthedocs.io/en/latest/', None),
    'pykeen': ('https://pykeen.readthedocs.io/en/stable/', None),
    'boto3': ('https://boto3.amazonaws.com/v1/documentation/api/latest/', None),
}
