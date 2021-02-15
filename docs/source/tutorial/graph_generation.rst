Graph generation
================

Commands 
--------

To generate the default graph (with all edges of all qualifies) in the current directory, use:

.. code-block:: sh

   openbiolink generate

For a list of arguments, use:

.. code-block:: sh

   openbiolink generate --help


File description
----------------

TSV
~~~

.. list-table::
   :header-rows: 1

   * - Default File Name
     - Description
     - Columns
   * - ALL_nodes.csv
     - All nodes present in the graph
     - Node Id, Node type
   * - edges.csv
     - All true positive edges
     - Node 1 ID, Edge type, Node 2 ID, Quality score, Source
   * - edges_list.csv
     - List of edge types present in edges.csv
     - Edge type
   * - nodes.csv
     - All nodes present in edges.csv
     - Node ID, Node type
   * - nodes_list.csv
     - List of node types present in nodes.csv
     - Node type
   * - TN_edges.csv
     - All true negative edges
     - Node 1 ID, Edge type, Node 2 ID, Quality score, Source
   * - TN_edges_list.csv
     - List of edge types present in TN_edges.csv
     - Edge type
   * - TN_nodes.csv
     - All nodes present in TN_edges.csv
     - Node ID, Node type
   * - TN_nodes_list.csv
     - List of node types present in TN_nodes.csv
     - Node type
   * - ids_no_mapping.tsv
     - ID's of nodes that could not be mapped to other ontology systems
     - Node ID, Node type
   * - tn_ids_no_mapping.tsv
     - ID's of nodes that could not be mapped to other ontology systems
     - Node ID, Node type 
   * - stats.txt
     - Statistics about edges.csv and nodes.csv
     - (See column headers of file)
   * - tn_stats.txt
     - Statistics about TN_edges.csv and TN_nodes.csv
     - (See column headers of file)

Biological Expression Language (BEL)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Biological Expression Language (BEL) is a domain specific language that enables the expression of biological relationships in a machine-readable format. It is supported by the `PyBEL <https://github.com/pybel/pybel>`_ software ecosystem.

BEL can be exported with:

.. code-block:: sh

   openbiolink generate --output-format BEL

.. list-table::
   :header-rows: 1

   * - Default File Name
     - Description
   * - positive.bel.gz
     - All true positive edges in `BEL Script <https://language.bel.bio/language/structure/>`_ format (gzipped) for usage in PyBEL or other BEL-aware applications)
   * - positive.bel.nodelink.json.gz
     - All true positive edges in `Nodelink JSON <https://pybel.readthedocs.io/en/latest/reference/io.html#pybel.from_nodelink_gz>`_ format (gzipped) for direct usage with `PyBEL <https://pybel.readthedocs.io>`_
   * - negative.bel.gz
     - All true negative edges in BEL Script format (gzipped)
   * - negative.bel.nodelink.json.gz
     - All true negative edges in Nodelink JSON format (gzipped)


Example opening BEL Script using `pybel.from_bel_script() <https://pybel.readthedocs.io/en/latest/reference/io.html#pybel.from_bel_script>`_ :

.. code-block:: python

   import gzip
   from pybel import from_bel_script
   with gzip.open('positive.bel.gz') as file:
       graph = from_bel_script(file)

Example opening Nodelink JSON using `pybel.from_nodelink_gz() <https://pybel.readthedocs.io/en/latest/reference/io.html#pybel.from_nodelink_gz>`_ :

.. code-block:: python

   from pybel import from_nodelink_gz
   graph = from_nodelink_gz('positive.bel.nodelink.json.gz')

There's an externally hosted copy of OpenBioLink `here <https://zenodo.org/record/3834052>`_ that contains
the exports as BEL.


CURIE's
-------

All node ID's in the graph are encoded as CURIE's, meaning entities can be easily looked up online by concatenating https://identifiers.org/ with the ID, f.e.:

.. list-table::
   :header-rows: 1

   * - CURIE
     - Identifiers.org
   * - GO:0006915
     - https://identifiers.org/GO:0006915
   * - REACTOME:R-HSA-201451
     - https://identifiers.org/REACTOME:R-HSA-201451


Detailed information of how the Identifiers are resolved can be found here https://registry.identifiers.org/
