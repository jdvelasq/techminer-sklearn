# flake8: noqa
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=missing-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
"""
Data Frame
===============================================================================

>>> from techminer2.database.metrics.performance_metrics import DataFrame
>>> (
...     DataFrame()
...     #
...     .with_source_field("author_keywords")
...     .select_top_n_terms(10)
...     .order_terms_by("OCC")
...     .having_term_occurrences_between(None, None)
...     .having_term_citations_between(None, None)
...     .having_terms_in(None)
...     #
...     .where_directory_is("example/")
...     .where_database_is("main")
...     .where_record_years_between(None, None)
...     .where_record_citations_between(None, None)
...     #
...     .build()
... )
                      rank_occ  rank_gcs  rank_lcs  ...  h_index  g_index  m_index
author_keywords                                     ...                           
FINTECH                      1         1         1  ...       31       12     7.75
INNOVATION                   2         2         2  ...        7        7     1.75
FINANCIAL_SERVICES           3         4        15  ...        4        4     1.00
FINANCIAL_INCLUSION          4         5         3  ...        3        3     0.75
FINANCIAL_TECHNOLOGY         5        15        45  ...        3        3     1.00
CROWDFUNDING                 6        23        16  ...        3        3     1.00
MARKETPLACE_LENDING          7        25        51  ...        3        3     1.50
BUSINESS_MODELS              8         3        14  ...        2        2     1.00
CYBER_SECURITY               9        21         9  ...        2        2     1.00
CASE_STUDY                  10        22        10  ...        2        2     0.67
<BLANKLINE>
[10 rows x 16 columns]


"""
from ....internals.mixins import InputFunctionsMixin
from ...load import DatabaseLoader, load__user_stopwords

SELECTED_COLUMNS = {
    "OCC": [
        "OCC",
        "global_citations",
        "local_citations",
        "_name_",
    ],
    #
    "global_citations": [
        "global_citations",
        "local_citations",
        "OCC",
        "_name_",
    ],
    # -------------------------------------------
    "local_citations": [
        "local_citations",
        "global_citations",
        "OCC",
        "_name_",
    ],
}


class DataFrame(
    InputFunctionsMixin,
):
    """:meta private:"""

    # -------------------------------------------------------------------------
    def _step_1_load_the_database(self):
        return DatabaseLoader().update_params(**self.params.__dict__).build()

    # -------------------------------------------------------------------------
    def _step_2_select_metric_fields(self, data_frame):
        return (
            data_frame[
                [
                    self.params.source_field,
                    "global_citations",
                    "local_citations",
                    "year",
                ]
            ]
            .dropna()
            .copy()
        )

    # -------------------------------------------------------------------------
    def _step_3_explode(self, data_frame):

        # Explode terms in field
        data_frame = data_frame.copy()
        data_frame[self.params.source_field] = data_frame[
            self.params.source_field
        ].str.split("; ")
        data_frame = data_frame.explode(self.params.source_field)

        # Add calculated columns to compute impact metrics
        # Sorts the data frame
        data_frame = data_frame.sort_values(
            [self.params.source_field, "global_citations", "local_citations"],
            ascending=[True, False, False],
        )

        data_frame = data_frame.assign(
            position=data_frame.groupby(self.params.source_field).cumcount() + 1
        )

        data_frame = data_frame.assign(
            position2=data_frame.position.map(lambda w: w * w)
        )

        data_frame = data_frame.reset_index(drop=True)

        return data_frame

    # -------------------------------------------------------------------------
    def _step_4_compute_initial_performance_metrics(self, data_frame):
        data_frame["OCC"] = 1
        grouped = data_frame.groupby(self.params.source_field).agg(
            {
                "OCC": "sum",
                "global_citations": "sum",
                "local_citations": "sum",
                "year": "min",
            }
        )
        grouped = grouped.rename(columns={"year": "first_publication_year"})
        grouped["last_year"] = data_frame.year.max()
        return grouped

    # -------------------------------------------------------------------------
    def _step_5_compute_derived_performance_metrics(self, grouped):

        grouped["age"] = grouped["last_year"] - grouped["first_publication_year"] + 1
        grouped["global_citations_per_year"] = (
            grouped["global_citations"] / grouped["age"]
        )
        grouped["local_citations_per_year"] = (
            grouped["local_citations"] / grouped["age"]
        )

        grouped["global_citations_per_document"] = (
            grouped["global_citations"] / grouped["OCC"]
        )
        grouped["local_citations_per_document"] = (
            grouped["local_citations"] / grouped["OCC"]
        )
        return grouped

    # -------------------------------------------------------------------------
    def _step_6_compute_impact_metrics(self, data_frame, grouped):

        # H-index
        h_indexes = data_frame.query("global_citations >= position")
        h_indexes = h_indexes.groupby(self.params.source_field, as_index=True).agg(
            {"position": "max"}
        )
        h_indexes = h_indexes.rename(columns={"position": "h_index"})
        grouped.loc[h_indexes.index, "h_index"] = h_indexes.astype(int)
        grouped["h_index"] = grouped["h_index"].fillna(0)

        # G-index
        g_indexes = data_frame.query("global_citations >= position2")
        g_indexes = g_indexes.groupby(self.params.source_field, as_index=True).agg(
            {"position": "max"}
        )
        g_indexes = g_indexes.rename(columns={"position": "g_index"})
        grouped.loc[g_indexes.index, "g_index"] = g_indexes.astype(int)
        grouped["g_index"] = grouped["g_index"].fillna(0)

        # M-index
        grouped = grouped.assign(m_index=grouped.h_index / grouped.age)
        grouped["m_index"] = grouped.m_index.round(decimals=2)

        return grouped

    # -------------------------------------------------------------------------
    def _sort_data_frame_by_metric(self, data_frame, metric):

        data_frame = data_frame.copy()
        data_frame["_name_"] = data_frame.index.tolist()

        columns = SELECTED_COLUMNS[metric]
        ascending = [False] * (len(columns) - 1) + [True]

        data_frame = data_frame.sort_values(columns, ascending=ascending)
        data_frame = data_frame.drop(columns=["_name_"])

        return data_frame

    # -------------------------------------------------------------------------
    def _step_7_add_rank_columns(self, grouped):

        grouped = self._sort_data_frame_by_metric(grouped, "local_citations")
        grouped.insert(0, "rank_lcs", range(1, len(grouped) + 1))

        grouped = self._sort_data_frame_by_metric(grouped, "global_citations")
        grouped.insert(0, "rank_gcs", range(1, len(grouped) + 1))

        grouped = self._sort_data_frame_by_metric(grouped, "OCC")
        grouped.insert(0, "rank_occ", range(1, len(grouped) + 1))

        return grouped

    # -------------------------------------------------------------------------
    def _step_8_remove_stopwords(self, grouped):

        stopwords = load__user_stopwords(root_dir=self.params.root_dir)
        grouped = grouped.drop(stopwords, axis=0, errors="ignore")
        return grouped

    # -------------------------------------------------------------------------
    def _step_9_filter_by_term_occurrences_range(self, grouped):

        if self.params.term_occurrences_range is None:
            return grouped

        min_value, max_value = self.params.term_occurrences_range

        if min_value is not None:
            grouped = grouped[grouped["OCC"] >= min_value]
        if max_value is not None:
            grouped = grouped[grouped["OCC"] <= max_value]

        return grouped

    # -------------------------------------------------------------------------
    def _step_10_filter_by_term_citations_range(self, grouped):

        if self.params.term_citations_range is None:
            return grouped

        min_value, max_value = self.params.term_citations_range

        if min_value is not None:
            grouped = grouped[grouped["global_citations"] >= min_value]
        if max_value is not None:
            grouped = grouped[grouped["global_citations"] <= max_value]

        return grouped

    # -------------------------------------------------------------------------
    def _step_11_filter_by_terms_in(self, grouped):

        if self.params.terms_in is None:
            return grouped

        if self.params.terms_in is not None:
            grouped = grouped[
                grouped[self.params.source_field].isin(self.params.terms_in)
            ]

        return grouped

    # -------------------------------------------------------------------------
    def _step_12_filter_by_top_n_terms(self, grouped):

        if self.params.top_n_terms is not None:
            grouped = grouped.head(self.params.top_n_terms)

        return grouped

    # -------------------------------------------------------------------------
    def _step_13_check_field_types(self, grouped):

        if "OCC" in grouped.columns:
            grouped["OCC"] = grouped["OCC"].astype(int)

        if "global_citations" in grouped.columns:
            grouped["global_citations"] = grouped["global_citations"].astype(int)

        if "local_citations" in grouped.columns:
            grouped["local_citations"] = grouped["local_citations"].astype(int)

        if "h_index" in grouped.columns:
            grouped["h_index"] = grouped["h_index"].astype(int)

        if "g_index" in grouped.columns:
            grouped["g_index"] = grouped["g_index"].astype(int)

        return grouped

    # -------------------------------------------------------------------------
    def build(self):

        data_frame = self._step_1_load_the_database()
        data_frame = self._step_2_select_metric_fields(data_frame)
        data_frame = self._step_3_explode(data_frame)
        grouped = self._step_4_compute_initial_performance_metrics(data_frame)
        grouped = self._step_5_compute_derived_performance_metrics(grouped)
        grouped = self._step_6_compute_impact_metrics(data_frame, grouped)
        grouped = self._step_7_add_rank_columns(grouped)
        grouped = self._step_8_remove_stopwords(grouped)
        grouped = self._step_9_filter_by_term_occurrences_range(grouped)
        grouped = self._step_10_filter_by_term_citations_range(grouped)
        grouped = self._step_11_filter_by_terms_in(grouped)
        grouped = self._step_12_filter_by_top_n_terms(grouped)
        grouped = self._step_13_check_field_types(grouped)

        return grouped


# def performance_metrics_frame(
#     #
#     # ITEMS PARAMS:
#     field,
#     #
#     # FILTER PARAMS:
#     metric="OCCGC",
#     top_n=20,
#     occ_range=(None, None),
#     gc_range=(None, None),
#     custom_terms=None,
#     #
#     # DATABASE PARAMS:
#     root_dir="./",
#     database="main",
#     year_filter=(None, None),
#     cited_by_filter=(None, None),
#     **filters,
# ):
#     """:meta private:"""

#     records = _mt_calculate_global_performance_metrics(
#         #
#         # ITEMS PARAMS:
#         field=field,
#         #
#         # DATABASE PARAMS:
#         root_dir=root_dir,
#         database=database,
#         year_filter=year_filter,
#         cited_by_filter=cited_by_filter,
#         **filters,
#     )

#     filtered_records = _mt_filter_records_by_metric(
#         records=records,
#         metric=metric,
#         top_n=top_n,
#         occ_range=occ_range,
#         gc_range=gc_range,
#         custom_items=custom_terms,
#     )

#     selected_records = _mt_select_record_columns_by_metric(
#         filtered_records,
#         metric,
#     )

#     if metric == "OCCGC":
#         metric = "OCC"

#     return selected_records