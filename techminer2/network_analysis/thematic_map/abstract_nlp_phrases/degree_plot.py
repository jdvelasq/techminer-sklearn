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


>>> from techminer2.network_analysis.thematic_map.abstract_nlp_phrases import degree_plot
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
>>> plot.fig_.write_html("sphinx/_static/network_analysis/thematic_map/abstract_nlp_phrases/degree_plot.html")

.. raw:: html

    <iframe src="../../../../../../_static/network_analysis/thematic_map/abstract_nlp_phrases/degree_plot.html" 
    height="600px" width="100%" frameBorder="0"></iframe>


>>> plot.df_.head()
   Node                                Name  Degree
0     0        REGULATORY_TECHNOLOGY 17:266      19
1     1       FINANCIAL_INSTITUTIONS 15:194      17
2     2        REGULATORY_COMPLIANCE 07:198      14
3     3  FINANCIAL_SERVICES_INDUSTRY 05:315      14
4     4      ARTIFICIAL_INTELLIGENCE 07:033      13

>>> print(plot.prompt_)
Your task is to generate an analysis about the degree of the nodes in a \\
networkx graph of a co-ocurrence matrix. Analyze the table below, delimited \\
by triple backticks, identifying any notable patterns, trends, or outliers \\
in the data, and discuss their implications in the network.
<BLANKLINE>
Table:
```
|    |   Node | Name                               |   Degree |
|---:|-------:|:-----------------------------------|---------:|
|  0 |      0 | REGULATORY_TECHNOLOGY 17:266       |       19 |
|  1 |      1 | FINANCIAL_INSTITUTIONS 15:194      |       17 |
|  2 |      2 | REGULATORY_COMPLIANCE 07:198       |       14 |
|  3 |      3 | FINANCIAL_SERVICES_INDUSTRY 05:315 |       14 |
|  4 |      4 | ARTIFICIAL_INTELLIGENCE 07:033     |       13 |
|  5 |      5 | FINANCIAL_SYSTEM 04:178            |       13 |
|  6 |      6 | FINANCIAL_SECTOR 07:169            |       12 |
|  7 |      7 | FINANCIAL_REGULATION 06:330        |       12 |
|  8 |      8 | INFORMATION_TECHNOLOGY 05:177      |       12 |
|  9 |      9 | DIGITAL_INNOVATION 03:164          |       12 |
| 10 |     10 | FINANCIAL_CRISIS 06:058            |       11 |
| 11 |     11 | RISK_MANAGEMENT 04:015             |       11 |
| 12 |     12 | FINANCIAL_TECHNOLOGY 05:173        |       10 |
| 13 |     13 | REGTECH_SOLUTIONS 05:018           |       10 |
| 14 |     14 | FINANCIAL_MARKETS 03:151           |        9 |
| 15 |     15 | COMPLIANCE_COSTS 03:002            |        9 |
| 16 |     16 | GLOBAL_FINANCIAL_CRISIS 06:177     |        8 |
| 17 |     17 | MACHINE_LEARNING 04:007            |        8 |
| 18 |     18 | NEW_TECHNOLOGIES 04:012            |        7 |
| 19 |     19 | REGTECH 03:034                     |        3 |
```
<BLANKLINE>


"""
from ....nx_create_co_occurrence_graph import nx_create_co_occurrence_graph
from ....nx_create_degree_plot import nx_create_degree_plot

FIELD = "abstract_nlp_phrases"


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
        association_index="association",
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