"""
Matrix Viewer --- ChatGPT
===============================================================================



Examples
-------------------------------------------------------------------------------

* Matrix view for a occurrence matrix.

>>> root_dir = "data/regtech/"

>>> file_name = "sphinx/_static/vantagepoint__matrix_viewer-0.html"

>>> from techminer2 import vantagepoint
>>> co_occ_matrix = vantagepoint.analyze.co_occ_matrix(
...     criterion='author_keywords',
...     other_criterion='authors',
...     topic_min_occ=2,
...     topics_length=10,
...     root_dir=root_dir,
... )
>>> co_occ_matrix_list = vantagepoint.analyze.list_cells_in_matrix(
...     co_occ_matrix)
>>> co_occ_matrix_list.cells_list_.head()
                row                       column  OCC
0    Arner DW 3:185  financial regulation 04:035    2
1    Arner DW 3:185               regtech 28:329    2
2   Brennan R 2:014            compliance 07:030    2
3   Brennan R 2:014               regtech 28:329    2
4  Buckley RP 3:185  financial regulation 04:035    2

>>> chart = vantagepoint.analyze.matrix_viewer(
...     co_occ_matrix, xaxes_range=(-2,2)
... )
>>> chart.plot_.write_html(file_name)

.. raw:: html

    <iframe src="../../../../../_static/vantagepoint__matrix_viewer-0.html"
    height="600px" width="100%" frameBorder="0"></iframe>


>>> print(chart.prompt_)
Analyze the table below, which contains the the occurrence values for author_keywords and authors. Identify any notable patterns, trends, or outliers in the data, and discuss their implications for the research field. Be sure to provide a concise summary of your findings in no more than 150 words.
<BLANKLINE>
|    | row               | column                         |   OCC |
|---:|:------------------|:-------------------------------|------:|
|  0 | Arner DW 3:185    | financial regulation 04:035    |     2 |
|  1 | Arner DW 3:185    | regtech 28:329                 |     2 |
|  2 | Brennan R 2:014   | compliance 07:030              |     2 |
|  3 | Brennan R 2:014   | regtech 28:329                 |     2 |
|  4 | Buckley RP 3:185  | financial regulation 04:035    |     2 |
|  5 | Buckley RP 3:185  | regtech 28:329                 |     2 |
|  6 | Butler T/1 2:041  | fintech 12:249                 |     2 |
|  7 | Butler T/1 2:041  | regtech 28:329                 |     2 |
|  8 | Crane M 2:014     | compliance 07:030              |     2 |
|  9 | Crane M 2:014     | regtech 28:329                 |     2 |
| 10 | Hamdan A 2:018    | regulatory technology 07:037   |     2 |
| 11 | Lin W 2:017       | regtech 28:329                 |     2 |
| 12 | Singh C 2:017     | regtech 28:329                 |     2 |
| 13 | Turki M 2:018     | regulatory technology 07:037   |     2 |
| 14 | Arner DW 3:185    | financial services 04:168      |     1 |
| 15 | Arner DW 3:185    | fintech 12:249                 |     1 |
| 16 | Barberis JN 2:161 | financial regulation 04:035    |     1 |
| 17 | Barberis JN 2:161 | financial services 04:168      |     1 |
| 18 | Barberis JN 2:161 | regtech 28:329                 |     1 |
| 19 | Buckley RP 3:185  | financial services 04:168      |     1 |
| 20 | Buckley RP 3:185  | fintech 12:249                 |     1 |
| 21 | Butler T/1 2:041  | regulation 05:164              |     1 |
| 22 | Butler T/1 2:041  | risk management 03:014         |     1 |
| 23 | Hamdan A 2:018    | anti-money laundering 03:021   |     1 |
| 24 | Lin W 2:017       | anti-money laundering 03:021   |     1 |
| 25 | Lin W 2:017       | artificial intelligence 04:023 |     1 |
| 26 | Singh C 2:017     | anti-money laundering 03:021   |     1 |
| 27 | Singh C 2:017     | artificial intelligence 04:023 |     1 |
| 28 | Turki M 2:018     | anti-money laundering 03:021   |     1 |
<BLANKLINE>
<BLANKLINE>

* Matrix view for a co-occurrence matrix.

>>> file_name = "sphinx/_static/vantagepoint__matrix_viewer-1.html"

>>> co_occ_matrix = vantagepoint.analyze.co_occ_matrix(
...     criterion='author_keywords',
...     topic_min_occ=7,
...     root_dir=root_dir,
... )
>>> co_occ_matrix_list = vantagepoint.analyze.list_cells_in_matrix(
...     co_occ_matrix)
>>> co_occ_matrix_list.cells_list_.head()
                 row             column  OCC
0     regtech 28:329     regtech 28:329   28
1     fintech 12:249     fintech 12:249   12
2     fintech 12:249     regtech 28:329   12
3     regtech 28:329     fintech 12:249   12
4  compliance 07:030  compliance 07:030    7

>>> chart = vantagepoint.analyze.matrix_viewer(
...     co_occ_matrix,
...     nx_k=0.5,
...     nx_iterations=5,
...     xaxes_range=(-2,2),
... )
>>> chart.plot_.write_html(file_name)

.. raw:: html

    <iframe src="../../../../../_static/vantagepoint__matrix_viewer-1.html"
    height="600px" width="100%" frameBorder="0"></iframe>

    
>>> print(chart.prompt_)
Analyze the table below, which contains the the co-occurrence values for \
author_keywords. Identify any notable patterns, trends, or outliers in the \
data, and discuss their implications for the research field. Be sure to \
provide a concise summary of your findings in no more than 150 words.
<BLANKLINE>
|    | row               | column                       |   OCC |
|---:|:------------------|:-----------------------------|------:|
|  2 | fintech 12:249    | regtech 28:329               |    12 |
|  5 | compliance 07:030 | regtech 28:329               |     7 |
|  8 | compliance 07:030 | fintech 12:249               |     2 |
| 10 | regtech 28:329    | regulatory technology 07:037 |     2 |
| 12 | compliance 07:030 | regulatory technology 07:037 |     1 |
| 13 | fintech 12:249    | regulatory technology 07:037 |     1 |
<BLANKLINE>
<BLANKLINE>


"""
from dataclasses import dataclass

from ... import network_utils
from .list_cells_in_matrix import list_cells_in_matrix


@dataclass(init=False)
class _Chart:
    plot_: None
    graph_: None
    table_: None
    prompt_: None


def matrix_viewer(
    obj,
    nx_k=0.5,
    nx_iterations=10,
    node_min_size=30,
    node_max_size=70,
    textfont_size_min=10,
    textfont_size_max=20,
    seed=0,
    xaxes_range=None,
    yaxes_range=None,
    show_axes=False,
):
    """Makes cluster map from a ocurrence flooding matrix."""

    matrix_list = list_cells_in_matrix(obj)

    graph = network_utils.create_graph(
        matrix_list,
        node_min_size,
        node_max_size,
        textfont_size_min,
        textfont_size_max,
    )

    graph = network_utils.compute_spring_layout(
        graph, nx_k, nx_iterations, seed
    )

    node_trace = network_utils.create_node_trace(graph)
    text_trace = network_utils.create_text_trace(graph)
    edge_traces = network_utils.create_edge_traces(graph)

    fig = network_utils.create_network_graph(
        edge_traces=edge_traces,
        node_trace=node_trace,
        text_trace=text_trace,
        xaxes_range=xaxes_range,
        yaxes_range=yaxes_range,
        show_axes=show_axes,
    )

    chart = _Chart()
    chart.plot_ = fig
    chart.graph_ = graph
    chart.table_ = matrix_list.cells_list_
    chart.prompt_ = matrix_list.prompt_

    return chart