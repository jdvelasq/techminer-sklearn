# flake8: noqa
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=missing-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
"""
Network Edges Frame
===============================================================================

## >>> from techminer2.pkgs.network.main_path import network_edges_frame
## >>> (
## ...     NetworkEdgesDataFrame()
## ...     #
## ...     # UNIT OF ANALYSIS:
## ...     .having_terms_in_top(None)
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
## ... )
--INFO-- Paths computed.
--INFO-- Points per link computed.
--INFO-- Points per path computed.
                                      citing_article  ... points
0  Gomber P., 2018, J MANAGE INF SYST, V35, P220 ...  ...      3
1  Gomber P., 2018, J MANAGE INF SYST, V35, P220 ...  ...      3
2                   Hu Z., 2019, SYMMETRY, V11 1:176  ...      4
3       Alt R., 2018, ELECTRON MARK, V28, P235 1:150  ...      1
4       Alt R., 2018, ELECTRON MARK, V28, P235 1:150  ...      2
5  Gozman D., 2018, J MANAGE INF SYST, V35, P145 ...  ...      3
<BLANKLINE>
[6 rows x 3 columns]


"""
from .internals.compute_main_path import internal__compute_main_path


def network_edges_frame(
    #
    # COLUMN PARAMS:
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
    """:meta private:"""

    #
    # Creates a table with citing and cited articles
    _, data_frame = internal__compute_main_path(
        #
        # NETWORK PARAMS:
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

    return data_frame
