# flake8: noqa
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=missing-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
"""
.. _tm2.performance.keywords.word_cloud:

Word Cloud
===============================================================================

>>> from techminer2.performance.plots import word_cloud
>>> chart = word_cloud(
...     #
...     # PERFORMANCE PARAMS:
...     field="keywords",
...     metric="OCC",
...     #
...     # CHART PARAMS:
...     title="Most Frequent Keywords",
...     width=400, 
...     height=400,
...     #
...     # ITEM FILTERS:
...     top_n=50,
...     occ_range=(None, None),
...     gc_range=(None, None),
...     custom_items=None,
...     #
...     # DATABASE PARAMS:
...     root_dir="data/regtech/",
...     database="main",
...     year_filter=(None, None),
...     cited_by_filter=(None, None),
... )
>>> chart.fig_.save("sphinx/_static/performance/words/keywords/word_cloud.png")

.. image:: ../../../../../_static/performance/words/keywords/word_cloud.png
    :width: 900px
    :align: center


"""