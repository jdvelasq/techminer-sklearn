# flake8: noqa
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=missing-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
"""
Network Plot
===============================================================================

## >>> # article:
## >>> from techminer2.pkgs.citation_network.articles import NetworkPlot
## >>> plot = (
## ...     NetworkPlot()
## ...     .set_analysis_params(
## ...         # unit_of_analysis='article',
## ...         top_n=30, 
## ...         citations_threshold=0,
## ...         algorithm_or_dict="louvain",
## ...     #
## ...     # NETWORK:
## ...     .using_spring_layout_k(None)
## ...     .using_spring_layout_iterations(30)
## ...     .using_spring_layout_seed(0)

## ...     #
## ...     .using_node_size_range(30, 70)
## ...     .using_textfont_size_range(10, 20)
## ...     .using_textfont_opacity_range(0.35, 1.00)

## ...         edge_color="#7793a5",
## ...         edge_width_range=(0.8, 3.0),
## ...     #
## ...     .using_xaxes_range(None, None)
## ...     .using_yaxes_range(None, None)
## ...     .using_axes_visible(False)

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
## >>> plot.write_html("sphinx/_generated/citation_network/articles/network_plot.html")

.. raw:: html

    <iframe src="../_generated/citation_network/articles/network_plot.html" 
    height="600px" width="100%" frameBorder="0"></iframe>




"""
from .....internals.nx.assign_constant_to_edge_colors import (
    internal__assign_constant_to_edge_colors,
)
from .....internals.nx.assign_edge_widths_based_on_weight import (
    internal__assign_edge_widths_based_on_weight,
)
from .....internals.nx.assign_node_colors_based_on_group_attribute import (
    internal__assign_node_colors_based_on_group_attribute,
)
from .....internals.nx.assign_node_sizes_based_on_citations import (
    internal__assign_node_sizes_based_on_citations,
)
from .....internals.nx.assign_text_positions_based_on_quadrants import (
    internal__assign_text_positions_based_on_quadrants,
)
from .....internals.nx.assign_textfont_opacity_based_on_citations import (
    internal__assign_textfont_opacity_based_on_citations,
)
from .....internals.nx.assign_textfont_sizes_based_on_citations import (
    internal__assign_textfont_sizes_based_on_citations,
)
from .....internals.nx.cluster_network_graph import internal__cluster_network_graph
from .....internals.nx.compute_spring_layout_positions import (
    internal__compute_spring_layout_positions,
)
from .....internals.nx.plot_network_graph import internal__plot_network_graph
from .internals.create_citation_nx_graph import _create_citation_nx_graph


def _network_plot(
    #
    # COLUMN PARAMS:
    top_n=None,
    citations_threshold=0,
    #
    # NETWORK CLUSTERING:
    algorithm_or_dict="louvain",
    #
    # LAYOUT:
    nx_k=None,
    nx_iterations=30,
    nx_random_state=0,
    #
    # NODES:
    node_size_range=(30, 70),
    textfont_size_range=(10, 20),
    textfont_opacity_range=(0.35, 1.00),
    #
    # EDGES:
    edge_color="#7793a5",
    edge_width_range=(0.8, 3.0),
    #
    # AXES:
    xaxes_range=None,
    yaxes_range=None,
    show_axes=False,
    #
    # DATABASE PARAMS:
    root_dir="./",
    database="main",
    year_filter=(None, None),
    cited_by_filter=(None, None),
    **filters,
):
    """:meta private:"""

    nx_graph = _create_citation_nx_graph(
        #
        # COLUMN PARAMS:
        top_n=top_n,
        citations_threshold=citations_threshold,
        #
        # DATABASE PARAMS:
        root_dir=root_dir,
        database=database,
        year_filter=year_filter,
        cited_by_filter=cited_by_filter,
        **filters,
    )

    nx_graph = internal__cluster_network_graph(
        #
        # FUNCTION PARAMS:
        nx_graph=nx_graph,
        #
        # NETWORK CLUSTERING:
        algorithm_or_dict=algorithm_or_dict,
    )

    nx_graph = internal__compute_spring_layout_positions(
        nx_graph=nx_graph,
        k=nx_k,
        iterations=nx_iterations,
        seed=nx_random_state,
    )

    #
    # Sets the node attributes
    nx_graph = internal__assign_node_colors_based_on_group_attribute(nx_graph)
    #
    nx_graph = internal__assign_node_sizes_based_on_citations(nx_graph, node_size_range)
    nx_graph = internal__assign_textfont_sizes_based_on_citations(
        nx_graph, textfont_size_range
    )
    nx_graph = internal__assign_textfont_opacity_based_on_citations(
        nx_graph, textfont_opacity_range
    )

    #
    # Sets the edge attributes
    nx_graph = internal__assign_edge_widths_based_on_weight(nx_graph, edge_width_range)
    nx_graph = internal__assign_text_positions_based_on_quadrants(nx_graph)
    nx_graph = internal__assign_constant_to_edge_colors(nx_graph, edge_color)

    return internal__plot_network_graph(
        #
        # FUNCTION PARAMS:
        nx_graph=nx_graph,
        #
        # NETWORK PARAMS:
        xaxes_range=xaxes_range,
        yaxes_range=yaxes_range,
        show_axes=show_axes,
        #
        # ARROWS:
        draw_arrows=True,
    )
