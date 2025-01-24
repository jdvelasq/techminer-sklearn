# flake8: noqa
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=missing-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=import-outside-toplevel
"""
World Map
===============================================================================

>>> from techminer2.database.metrics.performance_metrics import RankingPlot
>>> plot = (
...     WorldMap()
...     #
...     .with_source_field("countries")
...     .order_terms_by("OCC")
...     .having_term_occurrences_between(None, None)
...     .having_term_citations_between(None, None)
...     .having_terms_in(None)
...     #
...     .using_title_text("Countries' Scientific Production")
...     .using_colormap("Blues")
...     #
...     .where_directory_is("example/")
...     .where_database_is("main")
...     .where_record_years_between(None, None)
...     .where_record_citations_between(None, None)
...     #
...     .build()
... )
>>> plot.write_html("sphinx/_generated/database/metrics/performance_metrics/world_map.html")

.. raw:: html

    <iframe src="../../../_generated/database/metrics/performance_metrics/world_map.html" 
    height="400px" width="100%" frameBorder="0"></iframe>


"""
from ....internals.mixins.input_functions import InputFunctionsMixin
from ....internals.mixins.world_map import WorldMapMixin
from .data_frame import DataFrame


class WorldMap(
    InputFunctionsMixin,
    WorldMapMixin,
):
    """:meta private:"""

    def build(self):

        data_frame = DataFrame().update_params(**self.params.__dict__).build()

        if self.params.title_text is None:
            self.using_title_text("World Map")

        fig = self.build_world_map(data_frame=data_frame)

        return fig
