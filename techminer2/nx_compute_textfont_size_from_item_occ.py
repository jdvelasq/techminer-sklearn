# flake8: noqa
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=missing-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements

#
# In networkx, the size of the node is specified by the 'node_size' parameter.
# Example: nx.draw_networkx_nodes(G, pos, node_size=node_sizes)
import numpy as np


def nx_compute_textfont_size_from_item_occ(
    nx_graph,
    textfont_size_min,
    textfont_size_max,
):
    #
    # Extracs occurrences from node names. Example: 'regtech 10:100' -> 10
    occ = list(nx_graph.nodes())
    occ = [node.split(" ")[-1] for node in occ]
    occ = [node.split(":")[0] for node in occ]
    occ = np.array([float(node) for node in occ])

    #
    # Set the lower value of the node size to node_size_min
    min_occ = min(occ)
    textfont_sizes = occ - min_occ + textfont_size_min

    #
    # Checks if node_sizes.max() > node_size_max and, if so, rescales
    if textfont_sizes.max() > textfont_size_max:
        #
        # Scales the node size to the range [node_size_min, node_size_max]
        textfont_sizes -= textfont_size_min
        textfont_sizes /= textfont_sizes.max() - textfont_size_min
        textfont_sizes *= textfont_size_max - textfont_size_min
        textfont_sizes += textfont_size_min

    #
    # Sets the value of node_size
    for size, node in zip(textfont_sizes, nx_graph.nodes()):
        nx_graph.nodes[node]["textfont_size"] = size

    return nx_graph