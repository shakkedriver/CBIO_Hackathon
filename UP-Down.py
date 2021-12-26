import numpy as np
import Node

GENS = 10
#total genes at creature

n = 10
#number of creatures

#
#     1       0
# 1  0.9     0.1
# 0  0.1     0.9

class UP:
    def __init__(self, R_mtarix, root):
        self._R_mtarix = R_mtarix
        self._root = root
        self._U = np.zeros((2,2*n-1, GENS))
        self._orderArr = []
        self._orderArrDict = {}
        self._curPosGen = 0
        self._curPosNode = 0


    def createStack(self, Node, arr):
        if Node:
            # First recur on left child
            self.createStack(self._root.left,arr)

            # the recur on right child
            self.createStack(self._root.right,arr)

            # now print the data of node
            arr.append(Node)
        self._orderArr = arr
        self._orderArrDict = {n:i for i,n in enumerate(self._orderArr)}

    def isLeave(self, node):
        if node.left or node.right:
            return False
        return True

    def onePosCal(self, pos):
        # (2, 2 * n - 1, GENS)
        for node_num, node in enumerate(self._orderArr):
            if self.isLeave(node):
                for a in range(2):
                    if node.gens[pos] == a:
                        self._U[a, node_num, pos] = 1
                    # else:\
            else:
                for a in range(2):
                    self._U[a, node_num, pos] = 1

                    # for j in [node.right, node.left]
                    s = 0
                    for b in range(2):
                        s+= self._U[b, self._orderArrDict[node.right], pos] * np.exp(node.weightright* self._R_mtarix[a,b])
                    self._U[a, node_num, pos]*=s
                    s = 0
                    for b in range(2):
                        s += self._U[b, self._orderArrDict[node.left], pos] * np.exp(
                            node.weightleft * self._R_mtarix[a, b])
                    self._U[a, node_num, pos] *= s


                            # self._U[b, self._orderArrDict[j], pos] = 1
                            # sLeft+= self._U[a, self._orderArrDict[node.left],pos]
                            # sRight += self._U[a, self._orderArrDict[node.right], pos]
                            # self._U[a, node_num, pos] =  sLeft+sRight








    def fill_table(self):
        for node_num, node in enumerate(self._orderArr):
            for pos in
            if self.isLeave(node):
                self._U[]

