"""
Cluster Members --- ChatGPT
===============================================================================



Example:
-------------------------------------------------------------------------------

>>> root_dir = "data/regtech/"

>>> from techminer2 import vantagepoint
>>> occ_matrix = vantagepoint.analyze.co_occ_matrix(
...    criterion='author_keywords',
...    topic_min_occ=2,
...    root_dir=root_dir,
... )
>>> graph = vantagepoint.analyze.cluster_criterion(
...    occ_matrix,
...    community_clustering='louvain',
... )
>>> vantagepoint.analyze.cluster_members(graph)
                         CL_00  ...                           CL_04
0               fintech 12:249  ...  artificial intelligence 04:023
1    financial services 04:168  ...    anti-money laundering 03:021
2  financial regulation 04:035  ...              charitytech 02:017
3            innovation 03:012  ...              english law 02:017
4       data protection 02:027  ...                                
5               finance 02:001  ...                                
6             reporting 02:001  ...                                
<BLANKLINE>
[7 rows x 5 columns]


"""

import pandas as pd


def cluster_members(graph):
    """Gets communities from a networkx graph as a dataframe."""

    def extract_communities(graph):
        """Gets communities from a networkx graph as a dictionary."""

        communities = {}

        for node, data in graph.nodes(data=True):
            text = f"CL_{data['group'] :02d}"
            if text not in communities:
                communities[text] = []
            communities[text].append(node)

        return communities

    def sort_community_members(communities):
        """Sorts community members in a dictionary."""

        for key, items in communities.items():
            pdf = pd.DataFrame({"members": items})
            pdf = pdf.assign(
                OCC=pdf.members.map(lambda x: x.split()[-1].split(":")[0])
            )
            pdf = pdf.assign(
                gc=pdf.members.map(lambda x: x.split()[-1].split(":")[1])
            )
            pdf = pdf.sort_values(
                by=["OCC", "gc", "members"], ascending=[False, False, True]
            )
            communities[key] = pdf.members.tolist()

        return communities

    #
    # main:
    #
    communities = extract_communities(graph)
    communities = sort_community_members(communities)
    communities = pd.DataFrame.from_dict(communities, orient="index").T
    communities = communities.fillna("")
    communities = communities.sort_index(axis=1)

    return communities