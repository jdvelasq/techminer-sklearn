# flake8: noqa
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=missing-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
"""
Node Degree Plot
===============================================================================

>>> from techminer2.pkgs.networks.co_occurrence.author_keywords import NodeDegreePlot
>>> plot = (
...     NodeDegreePlot()
...     #
...     # FIELD:
...     .having_terms_in_top(20)
...     .having_terms_ordered_by("OCC")
...     .having_term_occurrences_between(None, None)
...     .having_term_citations_between(None, None)
...     .having_terms_in(None)
...     #
...     # NETWORK:
...     .using_association_index("association")
...     #
...     # PLOT:
...     .using_line_color("black")
...     .using_line_width(1.5)
...     .using_marker_size(7)
...     .using_textfont_size(10)
...     .using_yshift(4)
...     #
...     # DATABASE:
...     .where_directory_is("example/")
...     .where_database_is("main")
...     .where_record_years_between(None, None)
...     .where_record_citations_between(None, None)
...     .where_records_match(None)
...     #
...     .build()
... )
>>> # plot.write_html("sphinx/_static/co_occurrence_network/node_degree_plot.html")

.. raw:: html

    <iframe src="../_static/co_occurrence_network/node_degree_plot.html" 
    height="600px" width="100%" frameBorder="0"></iframe>




"""
"""Node Degree Plot"""
from .....internals.mixins import InputFunctionsMixin
from ..internals.node_degree_plot import InternalNodeDegreePlot


class NodeDegreePlot(
    InputFunctionsMixin,
):
    """:meta private:"""

    def build(self):
        """:meta private:"""

        return (
            InternalNodeDegreePlot()
            .update_params(**self.params.__dict__)
            .with_field("author_keywords")
            .build()
        )
