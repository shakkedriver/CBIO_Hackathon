import numpy as np
from Node import Node

def dfs_alg(root:Node,node:Node,twod_hist):
    """
    this function gose over a tree in dfs order and counts for each couple of indexes in the vector how many times the
    indexes got zerod one after the other
    :param root: the root of the tree
    :return:
    """
    if root == node:
        node.c = np.zeros_like(node.gens)
        dfs_alg(root,node.left,twod_hist)
        dfs_alg(root,node.right,twod_hist)
        return

    else:

