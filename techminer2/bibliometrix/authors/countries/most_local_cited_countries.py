"""
Most Local Cited Countries
===============================================================================




>>> directory = "data/regtech/"
>>> file_name = "sphinx/_static/most_local_cited_countries.html"

>>> from techminer2 import most_local_cited_countries
>>> most_local_cited_countries(
...     top_n=20,
...     directory=directory,
... ).write_html(file_name)

.. raw:: html

    <iframe src="../../../_static/most_local_cited_countries.html" height="600px" width="100%" frameBorder="0"></iframe>

"""
from ....chart import chart


def most_local_cited_countries(
    directory="./",
    top_n=20,
    plot="cleveland",
):
    """Most Local Cited Countries (from Reference Lists)."""

    return chart(
        column="countries",
        directory=directory,
        top_n=top_n,
        min_occ=None,
        max_occ=None,
        title="Most Local Cited Countries (from Reference Lists)",
        plot=plot,
        database="references",
        metric="local_citations",
    )