# flake8: noqa
# pylint: disable=import-outside-toplevel
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=missing-docstring
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
"""
Load Filtered Database
===============================================================================



>>> from techminer2.database.load import DatabaseLoader
>>> (
...     DatabaseLoader()
...     .where_directory_is("example/")
...     .where_database_is("main")
...     .where_record_years_between(None, None)
...     .where_record_citations_between(None, None)
...     .order_records_by(None)
...     .where_records_match(None)
...     .build()
... ).head() # doctest: +ELLIPSIS
                                                   link  ...                                  raw_abstract_copy
934   https://www.scopus.com/inward/record.uri?eid=2...  ...  THIS_PAPER examined THE_ACCEPTANCE of PAYMENT_...
935   https://www.scopus.com/inward/record.uri?eid=2...  ...  THE_RAPID_DEVELOPMENT of INFORMATION_AND_COMMU...
1031  https://www.scopus.com/inward/record.uri?eid=2...  ...  THE_PURPOSE of TECHNOLOGY is not to make FINAN...
1059  https://www.scopus.com/inward/record.uri?eid=2...  ...  GLOBAL_ECONOMY , GROWING_IMPORTANCE of INNOVAT...
1075  https://www.scopus.com/inward/record.uri?eid=2...  ...  THIS_PAPER examines THE_GROWING_IMPORTANCE of ...
<BLANKLINE>
[5 rows x 70 columns]

"""
import pathlib

import pandas as pd  # type: ignore

from ...internals.mixins import InputFunctionsMixin


class DatabaseLoader(
    InputFunctionsMixin,
):
    # -------------------------------------------------------------------------
    def _get_records_from_file(self):

        file_path = pathlib.Path(self.params.root_dir) / "databases/database.csv.zip"

        data_frame = pd.read_csv(
            file_path,
            encoding="utf-8",
            compression="zip",
        )

        criteria = {
            "main": "db_main",
            "references": "db_references",
            "cited_by": "db_cited_by",
        }[self.params.database]

        data_frame = data_frame[data_frame[criteria]]

        return data_frame

    # -------------------------------------------------------------------------
    def _filter_records_by_year(self, data_frame):

        years_range = self.params.record_years_range

        if years_range is None:
            return data_frame

        if not isinstance(years_range, tuple):
            raise TypeError(
                "The record_years_range parameter must be a tuple of two values."
            )

        if len(years_range) != 2:
            raise ValueError(
                "The record_years_range parameter must be a tuple of two values."
            )

        start_year, end_year = years_range

        if start_year is not None:
            data_frame = data_frame[data_frame.year >= start_year]

        if end_year is not None:
            data_frame = data_frame[data_frame.year <= end_year]

        return data_frame

    # -------------------------------------------------------------------------
    def _filter_records_by_citations(self, data_frame):

        citations_range = self.params.record_citations_range

        if citations_range is None:
            return data_frame

        if not isinstance(citations_range, tuple):
            raise TypeError(
                "The record_years_range parameter must be a tuple of two values."
            )

        if len(citations_range) != 2:
            raise ValueError(
                "The record_years_range parameter must be a tuple of two values."
            )

        cited_by_min, cited_by_max = citations_range

        if cited_by_min is not None:
            data_frame = data_frame[data_frame.global_citations >= cited_by_min]

        if cited_by_max is not None:
            data_frame = data_frame[data_frame.global_citations <= cited_by_max]

        return data_frame

    # -------------------------------------------------------------------------
    def _apply_filters_to_records(self, data_frame):

        filters = self.params.records_match

        if filters is None:
            return data_frame

        for filter_name, filter_value in filters.items():

            if filter_name == "article":

                data_frame = data_frame[data_frame["article"].isin(filter_value)]

            else:

                # Split the filter value into a list of strings
                database = data_frame[["article", filter_name]]
                database.loc[:, filter_name] = database[filter_name].str.split(";")

                # Explode the list of strings into multiple rows
                database = database.explode(filter_name)

                # Remove leading and trailing whitespace from the strings
                database[filter_name] = database[filter_name].str.strip()

                # Keep only records that match the filter value
                database = database[database[filter_name].isin(filter_value)]
                data_frame = data_frame[data_frame["article"].isin(database["article"])]

        return data_frame

    # -------------------------------------------------------------------------
    def _apply_sort_by(self, data_frame):
        #
        # sort_by: - date_newest
        #          - date_oldest
        #          - global_cited_by_highest
        #          - global_cited_by_lowest
        #          - local_cited_by_highest
        #          - local_cited_by_lowest
        #          - first_author_a_to_z
        #          - first_author_z_to_a
        #          - source_title_a_to_z
        #          - source_title_z_to_a

        sort_by = self.params.records_order_by

        if sort_by is None:
            return data_frame

        if sort_by == "date_newest":
            data_frame = data_frame.sort_values(
                ["year", "global_citations", "local_citations"],
                ascending=[False, False, False],
            )

        if sort_by == "date_oldest":
            data_frame = data_frame.sort_values(
                ["year", "global_citations", "local_citations"],
                ascending=[True, False, False],
            )

        if sort_by == "global_cited_by_highest":
            data_frame = data_frame.sort_values(
                ["global_citations", "year", "local_citations"],
                ascending=[False, False, False],
            )

        if sort_by == "global_cited_by_lowest":
            data_frame = data_frame.sort_values(
                ["global_citations", "year", "local_citations"],
                ascending=[True, False, False],
            )

        if sort_by == "local_cited_by_highest":
            data_frame = data_frame.sort_values(
                ["local_citations", "year", "global_citations"],
                ascending=[False, False, False],
            )

        if sort_by == "local_cited_by_lowest":
            data_frame = data_frame.sort_values(
                ["local_citations", "year", "global_citations"],
                ascending=[True, False, False],
            )

        if sort_by == "first_author_a_to_z":
            data_frame = data_frame.sort_values(
                ["authors", "global_citations", "local_citations"],
                ascending=[True, False, False],
            )

        if sort_by == "first_author_z_to_a":
            data_frame = data_frame.sort_values(
                ["authors", "global_citations", "local_citations"],
                ascending=[False, False, False],
            )

        if sort_by == "source_title_a_to_z":
            data_frame = data_frame.sort_values(
                ["source_title", "global_citations", "local_citations"],
                ascending=[True, False, False],
            )

        if sort_by == "source_title_z_to_a":
            data_frame = data_frame.sort_values(
                ["source_title", "global_citations", "local_citations"],
                ascending=[False, False, False],
            )

        return data_frame

    # -------------------------------------------------------------------------
    def build(self):

        data_frame = self._get_records_from_file()
        data_frame = self._filter_records_by_year(data_frame)
        data_frame = self._filter_records_by_citations(data_frame)
        data_frame = self._apply_filters_to_records(data_frame)
        data_frame = self._apply_sort_by(data_frame)

        return data_frame