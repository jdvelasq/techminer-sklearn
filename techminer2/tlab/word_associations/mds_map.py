"""
2D-MDS Map --- ChatGPT
===============================================================================

Plots the 2D-MDS of the normalized co-occurrence. The plot is based on the
MDS technique used in T-LAB's words associations.

**Algorithm**

1. Computes the co-occurrence matrix.

2. Apply MDS to the co-occurrence matrix with `n_components=2`.

3. Plot the decomposed matrix.



>>> # working directory
>>> root_dir = "data/regtech/"
>>> # computes the co-occurrence matrix
>>> from techminer2 import vantagepoint
>>> co_occ_matrix = vantagepoint.analyze.co_occ_matrix(
...     criterion='author_keywords',
...     topics_length=20,
...     root_dir=root_dir,
... )
>>> # computes the MDS
>>> from techminer2 import tlab
>>> mds_map = tlab.word_associations.svd_map(co_occ_matrix)
>>> file_name = "sphinx/_static/tlab__word_associations__mds_map.html"
>>> mds_map.plot_.write_html(file_name)

.. raw:: html

    <iframe src="../../../_static/tlab__word_associations__mds_map.html"
    height="800px" width="100%" frameBorder="0"></iframe>


>>> mds_map.table_.head()
                                 Dim_00    Dim_01
row                                              
regtech 28:329                32.386508 -2.623531
fintech 12:249                17.171575  5.275711
regulatory technology 07:037   3.500129  1.437108
compliance 07:030              8.945366 -4.175846
regulation 05:164              6.700788  3.488011

"""

from ..multidimensional_scaling import multidimensional_scaling


def mds_map(
    obj,
    # Technique parameters
    normalization=None,
    # MDS parameters
    metric=True,
    n_init=4,
    max_iter=300,
    eps=0.001,
    n_jobs=None,
    random_state=0,
    dissimilarity="euclidean",
    # Map parameters
    node_size_min=12,
    node_size_max=50,
    textfont_size_min=8,
    textfont_size_max=20,
    xaxes_range=None,
    yaxes_range=None,
):
    """2D SVD Map."""

    return multidimensional_scaling(
        obj,
        dim_x=0,
        dim_y=1,
        # Technique parameters
        is_2d=True,
        normalization=normalization,
        # MDS parameters
        metric=metric,
        n_init=n_init,
        max_iter=max_iter,
        eps=eps,
        n_jobs=n_jobs,
        random_state=random_state,
        dissimilarity=dissimilarity,
        # Map parameters
        node_size_min=node_size_min,
        node_size_max=node_size_max,
        textfont_size_min=textfont_size_min,
        textfont_size_max=textfont_size_max,
        xaxes_range=xaxes_range,
        yaxes_range=yaxes_range,
    )