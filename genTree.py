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
	
	def buildQ_matrixR_matrix(dim):
		r_matrix = np.sum(D, axis=0) / (n-2) 
		Q_matrix = np.zeros((dim,dim))
		for i in range(dim):
			for j in range(dim):
				Q_matrix[i][j] = r_matrix[i] + r_matrix[j] - D[i][j] 
		return Q_matrix, r_matrix
	
	newnode = None
	for _ in range(n):
		Q_matrix, r_matrix = buildQ_matrixR_matrix(k)
		i,j = np.unravel_index(
			np.argmax(Q_matrix), Q_matrix.shape)
		newnode = connect(leafs[i], leafs[j])
		leafs.append(newnode)
		
		for m in range(k):
			D[k][m] = 0.5*(D[i][m] + D[j][m] - D[i][j])  
		
		k += 1

	print(newnode)
	# should be the root 
	return newnode
	print(i,j)

def test():
	dist = np.array([
		[1 , 2 ,3],
		[4 , 6 ,3],
		[1 , 2 ,7]])
	generateTree(dist)
if __name__ == "__main__":
	test()