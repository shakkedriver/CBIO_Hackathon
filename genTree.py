import numpy as np
from Node import Node

def connect(left, right):
	newnode = Node() 
	newnode.left, newnode.right = left, right
	left.parent, right.parent = newnode, newnode
	return newnode

def generateTree(dist):
	
	n = dist.shape[0]

	D = np.zeros( (2*n,2*n) )	
	k = n

	for i in range(n):
		for j in range(n):
			D[i][j] = dist[i][j]

	leafs = [ Node() for _ in range(n)]
	
	r_matrix = np.sum(dist, axis=0) / (n-2) 
	print(r_matrix)
	Q_matrix = np.zeros((n,n))
	for i, ri in enumerate(r_matrix):
		for j, rj in enumerate(r_matrix):
			Q_matrix[i][j] = ri + rj - dist[i][j] 
	
	i,j = np.unravel_index(
		np.argmax(Q_matrix), Q_matrix.shape)
	
	newnode = connect(leafs[i], leafs[j])
	for j, rj in enumerate(r_matrix):
		Q_matrix[i][j] = ri + rj - dist[i][j] 
		
	leafs.append(  )
	


	print(i,j)

def test():
	dist = np.array([
		[1 , 2 ,3],
		[4 , 6 ,3],
		[1 , 2 ,7]])
	generateTree(dist)
if __name__ == "__main__":
	test()