import numpy as np

from Node import Node


def dfs_alg(root: Node, node: Node, twod_hist):
    """
    this function gose over a tree in dfs order and counts for each couple of indexes in the vector how many times the
    indexes got zerod one after the other
    :param root: the root of the tree
    :return:
    """
    # stopping condition for recursion
    if node is None:
        return
    # first level
    if root is node:
        node.change = np.zeros_like(node.gens)
        dfs_alg(root, node.left, twod_hist)
        dfs_alg(root, node.right, twod_hist)
        return
    # this would be run for each node
    # indexes with value lower than one means the parent had the gean but the node dose not
    node.change = node.gens - node.parent.gens
    # a list of indexes that where changed_in_node
    changed_in_node = np.where(node.change < 0)[0]
    # a list of indexes that where changed_in_parent
    changed_in_parent = np.where(node.parent.change < 0)[0]
    couples = [(i, j) for i in changed_in_node for j in changed_in_parent]
    # this is a list of all couples (i,j) where i>j and i is from  changed_in_node and j is from changed_in_parent
    couples = [a for a in couples if a[0] > a[1]]
    # this loop updates the histogram
    for c in couples:
        twod_hist[c[0], c[1]] += 1
    # recursive calls
    dfs_alg(root, node.left, twod_hist)
    dfs_alg(root, node.right, twod_hist)
    return
