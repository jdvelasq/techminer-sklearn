# flake8: noqa
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=missing-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
"""
Degree Plot
===============================================================================

>>> from techminer2.co_authorship.network.authors import degree_plot
>>> plot = degree_plot(
...     #
...     # COLUMN PARAMS:
...     top_n=20,
...     occ_range=(None, None),
...     gc_range=(None, None),
...     custom_items=None,
...     #
...     # NETWORK PARAMS:
...     algorithm_or_dict="louvain",
...     association_index="association",
...     #
...     # DEGREE PLOT:
...     textfont_size=10,
...     marker_size=7,
...     line_color="black",
...     line_width=1.5,
...     yshift=4,
...     #
...     # DATABASE PARAMS:
...     root_dir="data/regtech/",
...     database="main",
...     year_filter=(None, None),
...     cited_by_filter=(None, None),
... )
>>> plot.fig_.write_html("sphinx/_static/co_authorship/network/authors/degree_plot.html")

.. raw:: html

    <iframe src="../../../../../../_static/co_authorship/network/authors/degree_plot.html" 
    height="600px" width="100%" frameBorder="0"></iframe>

>>> plot.df_.head()
   Node               Name  Degree
0     0     Arner DW 3:185       4
1     1   Buckley RP 3:185       4
2     2     Weber RH 1:024       3
3     3  Zetzsche DA 1:024       3
4     4  Barberis JN 2:161       2

>>> print(plot.prompt_)
Your task is to generate an analysis about the degree of the nodes in a \\
networkx graph of a co-ocurrence matrix. Analyze the table below, delimited \\
by triple backticks, identifying any notable patterns, trends, or outliers \\
in the data, and discuss their implications in the network.
<BLANKLINE>
Table:
```
|    |   Node | Name                    |   Degree |
|---:|-------:|:------------------------|---------:|
|  0 |      0 | Arner DW 3:185          |        4 |
|  1 |      1 | Buckley RP 3:185        |        4 |
|  2 |      2 | Weber RH 1:024          |        3 |
|  3 |      3 | Zetzsche DA 1:024       |        3 |
|  4 |      4 | Barberis JN 2:161       |        2 |
|  5 |      5 | Hamdan A 2:018          |        2 |
|  6 |      6 | Turki M 2:018           |        2 |
|  7 |      7 | Brennan R 2:014         |        2 |
|  8 |      8 | Crane M 2:014           |        2 |
|  9 |      9 | Ryan P 2:014            |        2 |
| 10 |     10 | Sarea A 2:012           |        2 |
| 11 |     11 | Butler T 2:041          |        1 |
| 12 |     12 | Lin W 2:017             |        1 |
| 13 |     13 | Singh C 2:017           |        1 |
| 14 |     14 | Grassi L 2:002          |        1 |
| 15 |     15 | Lanfranchi D 2:002      |        1 |
| 16 |     16 | OBrien L 1:033          |        1 |
| 17 |     17 | Arman AA 2:000          |        0 |
| 18 |     18 | Anagnostopoulos I 1:153 |        0 |
| 19 |     19 | Baxter LG 1:030         |        0 |
```
<BLANKLINE>


"""
from ....nx_create_co_occurrence_graph import nx_create_co_occurrence_graph
from ....nx_create_degree_plot import nx_create_degree_plot

FIELD = "authors"


def degree_plot(
    #
    # COLUMN PARAMS:
    top_n=None,
    occ_range=(None, None),
    gc_range=(None, None),
    custom_items=None,
    #
    # NETWORK PARAMS:
    algorithm_or_dict="louvain",
    association_index="association",
    #
    # DEGREE PLOT:
    textfont_size=10,
    marker_size=7,
    line_color="black",
    line_width=1.5,
    yshift=4,
    #
    # DATABASE PARAMS:
    root_dir="./",
    database="main",
    year_filter=(None, None),
    cited_by_filter=(None, None),
    **filters,
):
    """
    :meta private:
    """
    # --------------------------------------------------------------------------
    # TODO: REMOVE DEPENDENCES:
    #
    #
    # LAYOUT:
    nx_k = None
    nx_iterations = 10
    nx_random_state = 0
    #
    # NODES:
    node_size_min = 30
    node_size_max = 70
    textfont_size_min = 10
    textfont_size_max = 20
    #
    # EDGES:
    edge_width_min = 0.8
    edge_width_max = 3.0
    #
    # --------------------------------------------------------------------------

    nx_graph = nx_create_co_occurrence_graph(
        #
        # FUNCTION PARAMS:
        rows_and_columns=FIELD,
        #
        # COLUMN PARAMS:
        top_n=top_n,
        occ_range=occ_range,
        gc_range=gc_range,
        custom_items=custom_items,
        #
        # NETWORK CLUSTERING:
        algorithm_or_dict=algorithm_or_dict,
        association_index=association_index,
        #
        # LAYOUT:
        nx_k=nx_k,
        nx_iterations=nx_iterations,
        nx_random_state=nx_random_state,
        #
        # NODES:
        node_size_min=node_size_min,
        node_size_max=node_size_max,
        textfont_size_min=textfont_size_min,
        textfont_size_max=textfont_size_max,
        #
        # EDGES:
        edge_width_min=edge_width_min,
        edge_width_max=edge_width_max,
        #
        # DATABASE PARAMS:
        root_dir=root_dir,
        database=database,
        year_filter=year_filter,
        cited_by_filter=cited_by_filter,
        **filters,
    )

    return nx_create_degree_plot(
        #
        # FUNCTION PARAMS:
        nx_graph=nx_graph,
        #
        # DEGREE PLOT PARAMS:
        textfont_size=textfont_size,
        marker_size=marker_size,
        line_color=line_color,
        line_width=line_width,
        yshift=yshift,
    )