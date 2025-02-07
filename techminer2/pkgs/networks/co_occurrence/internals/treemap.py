# flake8: noqa
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=missing-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
"""
Treemap
===============================================================================

## >>> from techminer2.pkgs.co_occurrence_network import treemap
## >>> plot = treemap(
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
## ...     .using_title_text(None)
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
## >>> # plot.write_html("sphinx/_static/co_occurrence_network/treemap.html")

.. raw:: html

    <iframe src="../_static/co_occurrence_network/treemap.html" 
    height="600px" width="100%" frameBorder="0"></iframe>

"""
from .....internals.mixins import InputFunctionsMixin
from ....internals.nx.assign_node_colors_based_on_group_attribute import (
    internal__assign_node_colors_based_on_group_attribute,
)
from ....internals.nx.cluster_nx_graph import internal__cluster_nx_graph
from ....internals.nx.plot_node_treemap import internal__plot_node_treemap
from ...co_occurrence_matrix.internals.create_co_occurrence_nx_graph import (
    _create_co_occurrence_nx_graph,
)


class InternalTreemap(
    InputFunctionsMixin,
):
    """:meta private:"""

    def build(self):
        """:meta private:"""


def treemap(
    #
    # PARAMS:
    field,
    #
    # COLUMN PARAMS:
    top_n=None,
    occ_range=(None, None),
    gc_range=(None, None),
    custom_terms=None,
    #
    # NETWORK PARAMS:
    algorithm_or_dict="louvain",
    association_index="association",
    #
    # DEGREE PLOT:
    title=None,
    #
    # DATABASE PARAMS:
    root_dir="./",
    database="main",
    year_filter=(None, None),
    cited_by_filter=(None, None),
    **filters,
):
    """:meta private:"""

    nx_graph = _create_co_occurrence_nx_graph(
        #
        # FUNCTION PARAMS:
        rows_and_columns=field,
        #
        # COLUMN PARAMS:
        top_n=top_n,
        occ_range=occ_range,
        gc_range=gc_range,
        custom_terms=custom_terms,
        #
        # NETWORK PARAMS:
        association_index=association_index,
        #
        # DATABASE PARAMS:
        root_dir=root_dir,
        database=database,
        year_filter=year_filter,
        cited_by_filter=cited_by_filter,
        **filters,
    )

    nx_graph = internal__cluster_nx_graph(
        #
        # FUNCTION PARAMS:
        nx_graph=nx_graph,
        #
        # NETWORK CLUSTERING:
        algorithm_or_dict=algorithm_or_dict,
    )

    nx_graph = internal__assign_node_colors_based_on_group_attribute(nx_graph)

    return internal__plot_node_treemap(
        #
        # FUNCTION PARAMS:
        nx_graph=nx_graph,
        #
        # CHART PARAMS:
        title=title,
    )
