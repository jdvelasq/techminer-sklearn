# flake8: noqa
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=missing-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
"""
Word Frequency over Time
===============================================================================

>>> from techminer2 import bibliometrix
>>> root_dir = "data/regtech/"
>>> file_name = "sphinx/_static/title_nlp_phrases_words_frequency_over_time.html"
>>> words = bibliometrix.title_nlp_phrases.words_frequency_over_time(
...     top_n=5,
...     root_dir=root_dir,
... )
>>> words.fig_.write_html(file_name)

.. raw:: html

    <iframe src="../../../../_static/title_nlp_phrases_words_frequency_over_time.html" height="600px" width="100%" frameBorder="0"></iframe>

    
>>> print(words.df_.to_markdown())
| title_nlp_phrases             |   2016 |   2017 |   2018 |   2019 |   2020 |   2021 |   2022 |   2023 |
|:------------------------------|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|
| REGULATORY_TECHNOLOGY 3:020   |      0 |      0 |      0 |      0 |      1 |      2 |      0 |      0 |
| ARTIFICIAL_INTELLIGENCE 3:017 |      0 |      0 |      0 |      0 |      1 |      1 |      1 |      0 |
| FINANCIAL_REGULATION 2:180    |      1 |      1 |      0 |      0 |      0 |      0 |      0 |      0 |
| FINANCIAL_CRIME 2:012         |      0 |      0 |      0 |      0 |      1 |      1 |      0 |      0 |
| EUROPEAN_UNION 1:024          |      0 |      0 |      0 |      0 |      1 |      0 |      0 |      0 |


>>> print(words.prompt_)
Your task is to generate an analysis about the  occurrences by year of the \\
'title_nlp_phrases' in a scientific bibliography database. Summarize the \\
table below, delimited by triple backticks, identify any notable patterns, \\
trends, or outliers in the data, and disc  uss their implications for the \\
research field. Be sure to provide a concise summary of your findings in no \\
more than 150 words.
<BLANKLINE>
Table:
```
| title_nlp_phrases             |   2016 |   2017 |   2018 |   2019 |   2020 |   2021 |   2022 |   2023 |
|:------------------------------|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|
| REGULATORY_TECHNOLOGY 3:020   |      0 |      0 |      0 |      0 |      1 |      2 |      0 |      0 |
| ARTIFICIAL_INTELLIGENCE 3:017 |      0 |      0 |      0 |      0 |      1 |      1 |      1 |      0 |
| FINANCIAL_REGULATION 2:180    |      1 |      1 |      0 |      0 |      0 |      0 |      0 |      0 |
| FINANCIAL_CRIME 2:012         |      0 |      0 |      0 |      0 |      1 |      1 |      0 |      0 |
| EUROPEAN_UNION 1:024          |      0 |      0 |      0 |      0 |      1 |      0 |      0 |      0 |
```
<BLANKLINE>



"""
from ...vantagepoint.discover import terms_by_year as analyze_terms_by_year

FIELD = "title_nlp_phrases"


def words_frequency_over_time(
    top_n=None,
    occ_range=None,
    gc_range=None,
    custom_items=None,
    cumulative=False,
    root_dir="./",
    database="main",
    year_filter=None,
    cited_by_filter=None,
    **filters,
):
    """Makes a dynamics chat for top words."""

    terms_by_year = analyze_terms_by_year(
        field=FIELD,
        top_n=top_n,
        occ_range=occ_range,
        gc_range=gc_range,
        custom_items=custom_items,
        root_dir=root_dir,
        database=database,
        year_filter=year_filter,
        cited_by_filter=cited_by_filter,
        cumulative=cumulative,
        **filters,
    )

    return terms_by_year