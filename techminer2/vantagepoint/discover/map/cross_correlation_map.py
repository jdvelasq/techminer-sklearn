# flake8: noqa
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=missing-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
# pylint: disable=too-many-branches
"""
.. _cross_correlation_map:

Cross-correlation Map
===============================================================================

Creates an Cross-correlation Map.

>>> from techminer2 import vantagepoint
>>> root_dir = "data/regtech/"
>>> file_name = "sphinx/_static/cross_correlation_map.html"
>>> vantagepoint.discover.map.cross_correlation_map(
...     rows_and_columns='authors', 
...     cross_with='countries',
...     top_n=10,
...     root_dir=root_dir,
...     color="#1f77b4", # tab:blue
... ).write_html("sphinx/_static/cross_correlation_map.html")

.. raw:: html

    <iframe src="../../../_static/cross_correlation_map.html" height="600px" width="100%" frameBorder="0"></iframe>

"""
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from ..matrix.cross_correlation_matrix import cross_correlation_matrix
from .correlation_map import correlation_map


def cross_correlation_map(
    #
    # FUNCTION PARAMS:
    rows_and_columns,
    cross_with,
    method="pearson",
    #
    # Map params:
    n_labels=None,
    color="#7793a5",
    nx_k=None,
    nx_iterations=10,
    nx_random_state=0,
    node_size_min=30,
    node_size_max=70,
    textfont_size_min=10,
    textfont_size_max=20,
    xaxes_range=None,
    yaxes_range=None,
    show_axes=False,
    #
    # ITEM PARAMS:
    top_n=None,
    occ_range=(None, None),
    gc_range=(None, None),
    custom_items=None,
    #
    # DATABASE PARAMS:
    root_dir="./",
    database="main",
    year_filter=(None, None),
    cited_by_filter=(None, None),
    **filters,
):
    """Correlation map."""

    corr_matrix = cross_correlation_matrix(
        #
        # FUNCTION PARAMS:
        rows_and_columns=rows_and_columns,
        cross_with=cross_with,
        method=method,
        #
        # ITEM PARAMS:
        top_n=top_n,
        occ_range=occ_range,
        gc_range=gc_range,
        custom_items=custom_items,
        #
        # DATABASE PARAMS:
        root_dir=root_dir,
        database=database,
        year_filter=year_filter,
        cited_by_filter=cited_by_filter,
        **filters,
    ).df_

    similarity = pd.DataFrame(
        cosine_similarity(corr_matrix),
        index=corr_matrix.index,
        columns=corr_matrix.columns,
    )

    return correlation_map(
        similarity=similarity,
        #
        # FUNCTION PARAMS:
        n_labels=n_labels,
        color=color,
        nx_k=nx_k,
        nx_iterations=nx_iterations,
        nx_random_state=nx_random_state,
        node_size_min=node_size_min,
        node_size_max=node_size_max,
        textfont_size_min=textfont_size_min,
        textfont_size_max=textfont_size_max,
        xaxes_range=xaxes_range,
        yaxes_range=yaxes_range,
        show_axes=show_axes,
    )