import numpy as np
from Node import Node
from file_editor import main as matrixgen
from dfs_alg import dfs_estimate

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
		Q_matrix = np.ones((dim,dim)) * - np.inf
		for i in range(dim):
			for j in range(i+1, dim):
				Q_matrix[i][j] = r_matrix[i] + r_matrix[j] - D[i][j] 
		# print(Q_matrix)
		return Q_matrix, r_matrix
	
	newnode = None
	for _ in range(n):
		Q_matrix, r_matrix = buildQ_matrixR_matrix(k)
		i,j = np.unravel_index(
			np.argmax(Q_matrix), Q_matrix.shape)
		# print(i,j)
		newnode = connect(leafs[i], leafs[j])
		
		
		# leafs.pop(i)
		# leafs.pop(j)
		leafs.append(newnode)
		
		for m in range(k):
			D[m][k] = 0.5*(
				 max(D[i][m], D[m][i]) +\
				 max(D[j][m], D[m][j])  -\
				 max(D[i][j], D[j][i]))
			D[k][m] = 0
		
		newnode.weightleft = D[i][k]
		newnode.weightleft = D[j][k]
		k += 1

	print(newnode)
	return newnode
	

def test():
	dist = np.array([
		[1 , 2 ,3, 2, 2, 9],
		[4 , 6 ,3, 4, 2, 9],
		[1 , 2 ,7, 1, 2, 9],
		[1 , 2 ,7, 1, 2, 9],
		[1 , 2 ,7, 1, 2, 9],
		[1 , 2 ,7, 1, 2, 9]], dtype=np.float32)
	
	dist = np.random.random( (12,12) ) 
	dist = matrixgen()
	n = dist.shape[0]
	for i in range(n):
		for j in range(i,n):
			dist[j][i] = 0
	newnode = generateTree(dist)

	from plots import pltTree
	# pltTree(newnode)

	prob = [[[] for i in range(n)]\
		 for j in range(n) ]

	dfs_estimate(newnode, prob)
	print(prob)

	def dfs(_newnode, _str):
		if _newnode is None:
			return
		dfs(_newnode.left, _str + " ")
		print(_str + "hi")
		dfs(_newnode.right, _str + " ")
		# print(Q_matrix)
	dfs(newnode, "")

if __name__ == "__main__":
	test()