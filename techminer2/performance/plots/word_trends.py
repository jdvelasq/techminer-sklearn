# flake8: noqa
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=missing-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
# pylint: disable=import-outside-toplevel
"""
Word Trends
===============================================================================


>>> from techminer2.performance.plots import word_trends
>>> chart = word_trends(
...     #
...     # ITEMS PARAMS:
...     field='author_keywords',
...     #
...     # CHART PARAMS:
...     title="Total Number of Documents, with Percentage of Documents Published in the Last Years",
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
>>> chart.fig_.write_html("sphinx/_static/performance/plots/word_trends.html")

.. raw:: html

    <iframe src="../../../../../_static/performance/plots/word_trends.html" 
    height="600px" width="100%" frameBorder="0"></iframe>


>>> chart.df_.head()
                       OCC  Before 2022  Between 2022-2023
author_keywords                                           
REGTECH                 28           20                  8
FINTECH                 12           10                  2
COMPLIANCE               7            5                  2
REGULATORY_TECHNOLOGY    7            5                  2
ANTI_MONEY_LAUNDERING    5            5                  0

>>> print(chart.prompt_)
Your task is to generate an analysis about the bibliometric indicators of \\
the 'author_keywords' field in a scientific bibliography database. \\
Summarize the table below, containing the number of documents Before 2022 \\
and Between 2022-2023, and sorted by the total number of documents, and \\
delimited by triple backticks. Identify any notable patterns, trends, or \\
outliers in the data, and discuss their implications for the research \\
field. Be sure to provide a concise summary of your findings in no more \\
than 150 words.
<BLANKLINE>
Table:
```
| author_keywords         |   OCC |   Before 2022 |   Between 2022-2023 |
|:------------------------|------:|--------------:|--------------------:|
| REGTECH                 |    28 |            20 |                   8 |
| FINTECH                 |    12 |            10 |                   2 |
| COMPLIANCE              |     7 |             5 |                   2 |
| REGULATORY_TECHNOLOGY   |     7 |             5 |                   2 |
| ANTI_MONEY_LAUNDERING   |     5 |             5 |                   0 |
| REGULATION              |     5 |             4 |                   1 |
| ARTIFICIAL_INTELLIGENCE |     4 |             3 |                   1 |
| FINANCIAL_REGULATION    |     4 |             2 |                   2 |
| FINANCIAL_SERVICES      |     4 |             3 |                   1 |
| SUPTECH                 |     3 |             1 |                   2 |
| BLOCKCHAIN              |     3 |             3 |                   0 |
| INNOVATION              |     3 |             2 |                   1 |
| RISK_MANAGEMENT         |     3 |             2 |                   1 |
| REPORTING               |     2 |             0 |                   2 |
| FINANCE                 |     2 |             1 |                   1 |
| TECHNOLOGY              |     2 |             1 |                   1 |
| SANDBOXES               |     2 |             2 |                   0 |
| GDPR                    |     2 |             2 |                   0 |
| DATA_PROTECTION_OFFICER |     2 |             2 |                   0 |
| ACCOUNTABILITY          |     2 |             2 |                   0 |
```
<BLANKLINE>



"""
from dataclasses import dataclass

import plotly.express as px

from ...format_prompt_for_dataframes import format_prompt_for_dataframes
from ..performance_metrics import performance_metrics


def word_trends(
    #
    # ITEM PARAMS:
    field,
    #
    # TREND ANALYSIS:
    time_window=2,
    is_trend_analysis=False,
    #
    # CHART PARAMS:
    title=None,
    metric_label=None,
    field_label=None,
    #
    # ITEM FILTERS:
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
    """
    :meta private:
    """

    #
    # Extracs only the performance metrics data frame
    data_frame = performance_metrics(
        #
        # ITEMS PARAMS:
        field=field,
        metric="word_trends",
        #
        # ITEM FILTERS:
        top_n=top_n,
        occ_range=occ_range,
        gc_range=gc_range,
        custom_items=custom_items,
        #
        # TREND ANALYSIS:
        time_window=time_window,
        is_trend_analysis=is_trend_analysis,
        #
        # DATABASE PARAMS:
        root_dir=root_dir,
        database=database,
        year_filter=year_filter,
        cited_by_filter=cited_by_filter,
        **filters,
    ).df_

    metric_label = "OCC" if metric_label is None else metric_label
    field_label = field.replace("_", " ").upper() if field_label is None else field_label

    before = data_frame.columns[1]
    between = data_frame.columns[2]

    fig_data = data_frame[["OCC", before, between]].copy()
    fig_data[field] = fig_data.index
    fig_data = fig_data.reset_index(drop=True)

    fig_data = fig_data.melt(
        id_vars=field,
        value_vars=[before, between],
    )

    fig_data = fig_data.rename(
        columns={
            field: field.replace("_", " ").title(),
            "variable": "Period",
            "value": "Num Documents",
        }
    )

    fig = px.bar(
        fig_data,
        x="Num Documents",
        y=field.replace("_", " ").title(),
        color="Period",
        title=title,
        orientation="h",
        color_discrete_map={
            before: "#7793a5",
            between: "#465c6b",
        },
    )
    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
    )
    fig.update_yaxes(
        linecolor="gray",
        linewidth=2,
        autorange="reversed",
        title=field_label,
    )
    fig.update_xaxes(
        linecolor="gray",
        linewidth=2,
        gridcolor="gray",
        griddash="dot",
    )

    main_text = (
        "Your task is to generate an analysis about the bibliometric indicators of the "
        f"'{field}' field in a scientific bibliography database. Summarize the table below, "
        f"containing the number of documents {before} and {between}, "
        "and sorted by the total number of documents, and delimited by triple backticks. Identify "
        "any notable patterns, trends, or outliers in the data, and discuss their "
        "implications for the research field. Be sure to provide a concise summary "
        "of your findings in no more than 150 words. "
    )
    prompt = format_prompt_for_dataframes(main_text, data_frame.to_markdown())

    @dataclass
    class Results:
        df_ = data_frame
        prompt_ = prompt
        fig_ = fig

    return Results()