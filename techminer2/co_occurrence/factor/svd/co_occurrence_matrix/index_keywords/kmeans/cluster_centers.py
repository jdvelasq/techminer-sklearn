# flake8: noqa
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=missing-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
"""
Cluster Centers
===============================================================================


>>> from techminer2.co_occurrence.factor.svd.co_occurrence_matrix.index_keywords.kmeans import cluster_centers
>>> cluster_centers(
...     #
...     # PARAMS:
...     association_index=None,
...     #
...     # ITEM PARAMS:
...     top_n=20,
...     occ_range=(None, None),
...     gc_range=(None, None),
...     custom_items=None,
...     #
...     # SVD PARAMS:
...     n_components=5,
...     algorithm_svd="randomized",
...     n_iter=5,
...     n_oversamples=10,
...     power_iteration_normalizer="auto",
...     random_state=0,
...     tol=0.0, 
...     #
...     # KMEANS PARAMS:
...     n_clusters=6,
...     init="k-means++",
...     n_init=10,
...     max_iter=300,
...     kmeans_tol=0.0001,
...     algorithm_kmeans="auto",
...     #
...     # DATABASE PARAMS:
...     root_dir="data/regtech/",
...     database="main",
...     year_filter=(None, None),
...     cited_by_filter=(None, None),
... )
            DIM_0     DIM_1     DIM_2     DIM_3     DIM_4
LABELS                                                   
CL_0     1.452433  2.408553 -0.111311  1.423050 -0.697610
CL_1     2.553832 -0.728733 -1.116535  0.306800 -0.225982
CL_2     3.805061  2.838379  0.784479 -1.455077  0.122520
CL_3     1.687510 -1.354703  3.088308  1.134300 -0.137336
CL_4     8.006025 -1.400130 -2.524959  0.056379 -0.280002
CL_5    11.685199 -2.515181  2.587363 -0.269164  0.138551


"""
from typing import Literal

from .......factor_analysis import FactorAnalyzer

UNIT_OF_ANALYSIS = "index_keywords"


def cluster_centers(
    #
    # PARAMS:
    association_index=None,
    #
    # ITEM PARAMS:
    top_n=None,
    occ_range=(None, None),
    gc_range=(None, None),
    custom_items=None,
    #
    # SVD PARAMS:
    n_components=None,
    algorithm_svd="randomized",
    n_iter=5,
    n_oversamples=10,
    power_iteration_normalizer="auto",
    random_state=0,
    tol=0.0,
    #
    # KMEANS PARAMS:
    n_clusters=8,
    init="k-means++",
    n_init=10,
    max_iter=300,
    kmeans_tol=0.0001,
    algorithm_kmeans="auto",
    #
    # DATABASE PARAMS:
    root_dir="./",
    database="main",
    year_filter=(None, None),
    cited_by_filter=(None, None),
    **filters,
):
    """
    :meta private:
    """

    analyzer = FactorAnalyzer(field=UNIT_OF_ANALYSIS)

    analyzer.cooc_matrix(
        #
        # COOC PARAMS:
        association_index=association_index,
        #
        # ITEM PARAMS:
        top_n=top_n,
        occ_range=occ_range,
        gc_range=gc_range,
        custom_items=custom_items,
        #
        # DATABASE PARAMS:
        root_dir=root_dir,
        database=database,
        year_filter=year_filter,
        cited_by_filter=cited_by_filter,
        **filters,
    )

    analyzer.svd(
        #
        # SVD PARAMS:
        n_components=n_components,
        algorithm=algorithm_svd,
        n_iter=n_iter,
        n_oversamples=n_oversamples,
        power_iteration_normalizer=power_iteration_normalizer,
        random_state=random_state,
        tol=tol,
    )

    analyzer.compute_embedding()

    analyzer.kmeans(
        #
        # KMEANS PARAMS:
        n_clusters=n_clusters,
        init=init,
        n_init=n_init,
        max_iter=max_iter,
        tol=kmeans_tol,
        random_state=random_state,
        algorithm=algorithm_kmeans,
    )

    analyzer.run_clustering()

    return analyzer.cluster_centers()