# flake8: noqa
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=missing-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=import-outside-toplevel
"""
Column Plot
===============================================================================

>>> from techminer2.database.metrics.performance_metrics import ColumnPlot
>>> plot = (
...     ColumnPlot()
...     #
...     .with_source_field("author_keywords")
...     .select_top_n_terms(10)
...     .order_terms_by("OCC")
...     .having_term_occurrences_between(None, None)
...     .having_term_citations_between(None, None)
...     .having_terms_in(None)
...     #
...     .using_title_text("Ranking Plot")
...     .using_xaxes_title_text("Author Keywords")
...     .using_yaxes_title_text("OCC")
...     #
...     .where_directory_is("example/")
...     .where_database_is("main")
...     .where_record_years_between(None, None)
...     .where_record_citations_between(None, None)
...     #
...     .build()
... )
>>> plot.write_html("sphinx/_generated/database/metrics/performance_metrics/column_plot.html")

.. raw:: html

    <iframe src="../../../_generated/database/metrics/performance_metrics/column_plot.html" 
    height="600px" width="100%" frameBorder="0"></iframe>



"""
from ....internals.mixins.column_plot import ColumnPlotMixin
from ....internals.mixins.input_functions import InputFunctionsMixin
from .data_frame import DataFrame


class ColumnPlot(
    InputFunctionsMixin,
    ColumnPlotMixin,
):
    """:meta private:"""

    def build(self):

        data_frame = DataFrame().update_params(**self.params.__dict__).build()

        if self.params.title_text is None:
            self.using_title_text("Column Plot")

        if self.params.xaxes_title_text is None:
            self.using_xaxes_title_text(
                self.params.source_field.replace("_", " ").upper() + " RANK"
            )

        if self.params.yaxes_title_text is None:
            self.using_yaxes_title_text(
                self.params.terms_order_by.replace("_", " ").upper()
            )

        fig = self.build_column_plot(data_frame)

        return fig