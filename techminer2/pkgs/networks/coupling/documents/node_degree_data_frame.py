# flake8: noqa
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=missing-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
"""
Network Degree Frame
===============================================================================

## >>> from techminer2.pkgs.networks.coupling.articles  import NodeDegreeDataFrame
## >>> (
## ...     NodeDegreeDataFrame()
## ...     #
## ...     # UNIT OF ANALYSIS:
## ...     .having_terms_in_top(20)
## ...     .having_citation_threshold(0)
## ...     #
## ...     # DATABASE:
## ...     .where_directory_is("example/")
## ...     .where_database_is("main")
## ...     .where_record_years_between(None, None)
## ...     .where_record_citations_between(None, None)
## ...     .where_records_match(None)
## ...     #
## ...     .build()
## ... ).head()



"""
from .....internals.mixins import InputFunctionsMixin

# from ....internals.nx.nx_degree_frame import nx_degree_frame
from ..internals.from_documents.create_nx_graph import internal__create_nx_graph


class NodeDegreeDataFrame(
    InputFunctionsMixin,
):
    """:meta private:"""

    def build(self):
        pass


def _node_degree_frame(
    #
    # ARTICLE PARAMS:
    top_n=None,
    citations_threshold=0,
    #
    # DATABASE PARAMS:
    root_dir="./",
    database="main",
    year_filter=(None, None),
    cited_by_filter=(None, None),
    **filters,
):

    nx_graph = internal__create_nx_graph(
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

    return nx_degree_frame(
        #
        # FUNCTION PARAMS:
        nx_graph=nx_graph,
    )
