"""Most Global Cited Authors
===============================================================================

>>> from techminer2 import *
>>> directory = "data/"
>>> file_name = "sphinx/_static/most_global_cited_authors.html"

>>> most_global_cited_authors(
...     directory,
...     top_n=20,
...     min_occ=None,
...     max_occ=None,
...     plot="cleveland",
...     database="documents",
... ).write_html(file_name)

.. raw:: html

    <iframe src="_static/most_global_cited_authors.html" height="600px" width="100%" frameBorder="0"></iframe>

"""
from .bar_chart import bar_chart
from .cleveland_chart import cleveland_chart
from .column_chart import column_chart
from .line_chart import line_chart
from .pie_chart import pie_chart
from .terms_list import terms_list
from .word_cloud import word_cloud


def most_global_cited_authors(
    directory="./",
    top_n=20,
    min_occ=None,
    max_occ=None,
    plot="bar",
    database="documents",
):
    """Plots the number of global citations by author using the specified plot."""

    if database == "documents":
        title = "Most Global Cited Authors"
    elif database == "references":
        title = "Most Global Cited Authors in References"
    elif database == "cited_by":
        title = "Most Global Cited Authors in citing documents"
    else:
        raise ValueError(
            "Invalid database name. Database must be one of: 'documents', 'references', 'cited_by'"
        )

    indicators = terms_list(
        column="authors",
        metric="global_citations",
        top_n=top_n,
        min_occ=min_occ,
        max_occ=max_occ,
        directory=directory,
        database=database,
    )

    plot_function = {
        "bar": bar_chart,
        "column": column_chart,
        "line": line_chart,
        "circle": pie_chart,
        "cleveland": cleveland_chart,
        "wordcloud": word_cloud,
    }[plot]

    return plot_function(
        dataframe=indicators,
        metric="global_citations",
        title=title,
    )