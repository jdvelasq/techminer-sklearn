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

## >>> from techminer2.pkgs.co_occurrence_network import NodeDegreePlot
## >>> plot = (
## ...     NodeDegreePlot()
## ...     #
## ...     # FIELD:
## ...     .with_field("author_keywords")
## ...     .having_terms_in_top(20)
## ...     .having_terms_ordered_by("OCC")
## ...     .having_term_occurrences_between(None, None)
## ...     .having_term_citations_between(None, None)
## ...     .having_terms_in(None)
## ...     #
## ...     # NETWORK:
## ...     .using_association_index("association")
## ...     #
## ...     # PLOT:
## ...     .using_line_color("black")
## ...     .using_line_width(1.5)
## ...     .using_marker_size(7)
## ...     .using_textfont_size(10)
## ...     .using_yshift(4)
## ...     #
## ...     # DATABASE:
## ...     .where_directory_is("example/")
## ...     .where_database_is("main")
## ...     .where_record_years_between(None, None)
## ...     .where_record_citations_between(None, None)
## ...     .where_records_match(None)
## ...     #
## ...     .build()
## ... )
## >>> # plot.write_html("sphinx/_static/co_occurrence_network/node_degree_plot.html")

.. raw:: html

    <iframe src="../_static/co_occurrence_network/node_degree_plot.html" 
    height="600px" width="100%" frameBorder="0"></iframe>




"""
"""Node Degree Plot"""
from .....internals.mixins import InputFunctionsMixin
from .....internals.nx import (
    internal__assign_degree_to_nodes,
    internal__collect_node_degrees,
    internal__create_node_degree_plot,
    internal__create_node_degrees_data_frame,
)
from .....internals.nx.assign_degree_to_nodes import internal__assign_degree_to_nodes
from .create_nx_graph import internal__create_nx_graph


class InternalNodeDegreePlot(
    InputFunctionsMixin,
):
    """:meta private:"""

    def build(self):

        nx_graph = internal__create_nx_graph(self.params)
        nx_graph = internal__assign_degree_to_nodes(nx_graph)
        node_degrees = internal__collect_node_degrees(nx_graph)
        data_frame = internal__create_node_degrees_data_frame(node_degrees)
        plot = internal__create_node_degree_plot(self.params, data_frame)

        return plot
