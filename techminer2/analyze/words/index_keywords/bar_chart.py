# flake8: noqa
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=missing-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
"""
Bar Chart
===============================================================================


>>> from techminer2.performance.plots import bar_chart
>>> chart = bar_chart(
...     #
...     # ITEMS PARAMS:
...     field='index_keywords',
...     metric="OCC",
...     #
...     # CHART PARAMS:
...     title="Most Frequent Index Keywords",
...     metric_label=None,
...     field_label=None,
...     #
...     # ITEM FILTERS:
...     top_n=20,
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
>>> chart.fig_.write_html("sphinx/_static/performance/words/index_keywords/bar_chart.html")

.. raw:: html

    <iframe src="../../../../../_static/performance/words/index_keywords/bar_chart.html" 
    height="600px" width="100%" frameBorder="0"></iframe>

    
>>> chart.df_.head()
                        rank_occ  OCC  ...  between_2022_2023  growth_percentage
index_keywords                         ...                                      
REGULATORY_COMPLIANCE          1    9  ...                3.0              33.33
FINANCIAL_INSTITUTIONS         2    6  ...                2.0              33.33
FINANCE                        3    5  ...                2.0              40.00
REGTECH                        4    5  ...                2.0              40.00
ANTI_MONEY_LAUNDERING          5    3  ...                0.0               0.00
<BLANKLINE>
[5 rows x 5 columns]


>>> print(chart.prompt_) # doctest: +ELLIPSIS
Your task is ...




"""