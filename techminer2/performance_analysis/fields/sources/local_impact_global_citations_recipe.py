# flake8: noqa
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=missing-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
"""
Local Impact --- Global Citations (Recipe)
===============================================================================

>>> from techminer2.performance_analysis import item_metrics
>>> root_dir = "data/regtech/"
>>> items = item_metrics(
...     #
...     # ITEMS PARAMS:
...     field='source_abbr',
...     metric="global_citations",
...     #
...     # CHART PARAMS:
...     title=None,
...     field_label=None,
...     metric_label=None,
...     textfont_size=10,
...     marker_size=7,
...     line_width=1.5,
...     yshift=4,
...     #
...     # ITEM FILTERS:
...     top_n=10,
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
>>> print(items.df_.to_markdown())
| source_abbr                   |   rank_gc |   global_citations |   local_citations |   global_citations_per_document |   local_citations_per_document |   global_citations_per_year |
|:------------------------------|----------:|-------------------:|------------------:|--------------------------------:|-------------------------------:|----------------------------:|
| J ECON BUS                    |         1 |                153 |                17 |                           153   |                           17   |                       25.5  |
| NORTHWEST J INTL LAW BUS      |         2 |                150 |                 0 |                           150   |                            0   |                       21.43 |
| J BANK REGUL                  |         3 |                 35 |                 9 |                            17.5 |                            4.5 |                        8.75 |
| PALGRAVE STUD DIGIT BUS ENABL |         4 |                 33 |                14 |                            33   |                           14   |                        6.6  |
| DUKE LAW J                    |         5 |                 30 |                 0 |                            30   |                            0   |                        3.75 |
| J RISK FINANC                 |         6 |                 21 |                 8 |                            21   |                            8   |                        3.5  |
| J MONEY LAUND CONTROL         |         7 |                 14 |                 3 |                            14   |                            3   |                        3.5  |
| J FINANC CRIME                |         8 |                 13 |                 4 |                             6.5 |                            2   |                        3.25 |
| FINANCIAL INNOV               |         9 |                 13 |                 1 |                            13   |                            1   |                        6.5  |
| ICEIS - PROC INT CONF ENTERP  |        10 |                 12 |                 3 |                            12   |                            3   |                        3    |




>>> items.fig_.write_html("sphinx/_static/performance_analysis/fields/sources/global_citations_chart.html")

.. raw:: html

    <iframe src="../../../../_static/performance_analysis/fields/sources/global_citations_chart.html" 
    height="600px" width="100%" frameBorder="0"></iframe>

    
>>> print(items.prompt_)
Your task is to generate an analysis about the bibliometric indicators of \\
the 'source_abbr' field in a scientific bibliography database. Summarize \\
the table below, sorted by the 'global_citations' metric, and delimited by \\
triple backticks, identify any notable patterns, trends, or outliers in the \\
data, and discuss their implications for the research field. Be sure to \\
provide a concise summary of your findings in no more than 150 words.
<BLANKLINE>
Table:
```
| source_abbr                   |   rank_gc |   global_citations |   local_citations |   global_citations_per_document |   local_citations_per_document |   global_citations_per_year |
|:------------------------------|----------:|-------------------:|------------------:|--------------------------------:|-------------------------------:|----------------------------:|
| J ECON BUS                    |         1 |                153 |                17 |                           153   |                           17   |                       25.5  |
| NORTHWEST J INTL LAW BUS      |         2 |                150 |                 0 |                           150   |                            0   |                       21.43 |
| J BANK REGUL                  |         3 |                 35 |                 9 |                            17.5 |                            4.5 |                        8.75 |
| PALGRAVE STUD DIGIT BUS ENABL |         4 |                 33 |                14 |                            33   |                           14   |                        6.6  |
| DUKE LAW J                    |         5 |                 30 |                 0 |                            30   |                            0   |                        3.75 |
| J RISK FINANC                 |         6 |                 21 |                 8 |                            21   |                            8   |                        3.5  |
| J MONEY LAUND CONTROL         |         7 |                 14 |                 3 |                            14   |                            3   |                        3.5  |
| J FINANC CRIME                |         8 |                 13 |                 4 |                             6.5 |                            2   |                        3.25 |
| FINANCIAL INNOV               |         9 |                 13 |                 1 |                            13   |                            1   |                        6.5  |
| ICEIS - PROC INT CONF ENTERP  |        10 |                 12 |                 3 |                            12   |                            3   |                        3    |
```
<BLANKLINE>

"""