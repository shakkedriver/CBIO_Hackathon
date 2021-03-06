
from plots import pltTree, plot_groups
from up_down import up_down, up_down_down_stage, up_down_assignment, tree_to_arr, create_table
from plots import pltTree
import numpy as np
from Node import Node, GENS
from file_editor import main as matrixgen
from dfs_alg import dfs_estimate
import matplotlib.pyplot as plt
from operator import itemgetter



def connect(left, right):
	newnode = Node()
	newnode.left, newnode.right = left, right
	left.parent, right.parent = newnode, newnode
	return newnode

def generateTree(dist, gens_vec):

	n = dist.shape[0]

	D = np.zeros( (2*n,2*n) ).astype(np.float32)
	k = n

	for i in range(n):
		for j in range(i+1, n):
			D[i][j] = dist[i][j]

	leafs = [ Node() for _ in range(n)]
	for _ in range(n):
		leafs[_].gens = gens_vec[_]

	def buildQ_matrixR_matrix(dim):
		r_matrix = np.sum(D, axis=0) / (n-2)
		Q_matrix = np.ones((dim,dim)) * - np.inf
		for i in range(dim):
			for j in range(i+1, dim):
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
			D[m][k] = 0.5*(
					max(D[i][m], D[m][i]) + \
					max(D[j][m], D[m][j])  - \
					max(D[i][j], D[j][i]))
			D[k][m] = 0

		newnode.weightleft 	= 1 
		newnode.weightright = 1 
		

		k += 1

	return newnode



def test():
	dist = np.array([
		[1 , 2 ,3, 2, 2, 9],
		[4 , 6 ,3, 4, 2, 9],
		[1 , 2 ,7, 1, 2, 9],
		[1 , 2 ,7, 1, 2, 9],
		[1 , 2 ,7, 1, 2, 9],
		[1 , 2 ,7, 1, 2, 9]], dtype=np.float32)

	# dist = np.random.random( (300,300) )
	# gens_vec = np.int64(np.random.randint(2, size=(300,GENS)))
	# print(gens_vec)
	dist, gens_vec = matrixgen()
	print("hi")
	# dist, gens_vec = dist[:100, :40], gens_vec[:40]
	n = dist.shape[0]
	for i in range(n):
		for j in range(i,n):
			dist[j][i] = 0
	newnode = generateTree(dist, gens_vec)

	up_down(newnode)
	up_down_down_stage(newnode)
	# diff(newnode)

	prob = [[ [] for i in range( len(newnode.gens) )]\
		 for j in range( len(newnode.gens) ) ]

	dfs_estimate(newnode, prob)
	# temporary
	meanprob = np.zeros( shape=(len(newnode.gens), len(newnode.gens)) )
	for i in range( len(newnode.gens) ):
		for j in range( len(newnode.gens) ):
			meanprob[i][j] = sum(prob[i][j]) /\
				 len(prob[i][j]) if len(prob[i][j]) != 0 else 0

	import matplotlib.pyplot as plt
	plt.imshow(meanprob)
	plt.show()

	from t import get_two_groups
	corlated, uncoralted = get_two_groups(meanprob, 0.5)#corlated
	print(corlated)
	corlated, uncoralted = get_two_groups(meanprob, 0.5)
	plt.hist(corlated)
	plt.show()

	# print(meanprob)
	# print(prob)
	# def dfs(_newnode, _str):
	# 	if _newnode is None:
	# 		return
	# 	dfs(_newnode.left, _str + " ")
	# 	print(_str + "hi")
	# 	dfs(_newnode.right, _str + " ")
	# dfs(newnode, "")

if __name__ == "__main__":
	test()