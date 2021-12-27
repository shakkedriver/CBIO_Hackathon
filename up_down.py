import numpy as np
from Node import GENS

FLIP =  {
	(0,0,0) : 0.60,
	(1,0,0) : 0.10,
	(0,1,0) : 0.15,
	(0,0,1) : 0.15,
	(1,1,0) : 0.15,
	(0,1,1) : 0.10,
	(1,0,1) : 0.15,
	(1,1,1) : 0.60
} 

FLIPdown = {
	(0,0) : 0.95,
	(0,1) : 0.05,
	(1,1) : 0.8,
	(1,0) : 0.2
}
# MATRIXP = FLIP

def isleaf(node):
	return ( node.left is None) and (node.right is None)

def create_table(t_arr):
	ij_matrix = np.zeros((GENS, GENS))
	for speciesA in t_arr:
		for speciesB in t_arr:
			if abs(speciesA[1] - speciesB[1])<100:
				for i in range(GENS):
					for j in range(i, GENS):
						if (speciesA[0].gens[i] ==  speciesA[0].gens[j]) and (speciesB[0].gens[i] ==  speciesB[0].gens[j]) :
							if speciesA[0].gens[i] !=  speciesB[0].gens[j]:
								ij_matrix[i][j]+=1
		return ij_matrix





def tree_to_arr(root, arr, counter):
	counter += 1
	if isleaf(root):
		arr.append((root,counter))
		return arr
	tree_to_arr(root.left,arr, counter)
	tree_to_arr(root.right, arr, counter)
	return arr


def up_down(node):
	if node is None or isleaf(node):
		if isleaf(node):
			for j in range(GENS):
				for assignment in [0,1]:
					node.gensprob[j][assignment] = 1\
						 if assignment == node.gens[j] else 0
		return

	up_down(node.left)
	up_down(node.right)

	if node.left is None:
		node.gens = node.right.gens
		for assignment in [0,1]:
			node.gensprob[:, assignment] = node.right.gensprob[:, assignment]  
	
	elif node.right is None: 
		node.gens = node.left.gens
		for assignment in [0,1]:
			node.gensprob[:, assignment] = node.left.gensprob[:, assignment]  
	
	else:
		for assignment in [0,1]:
			for assleft, assright in [ (0,0), (0,1), (1,1), (1,0)]:
				node.gensprob[:, assignment] +=   \
					FLIP[ (assignment, assleft, assright) ] *node.weightleft*\
						 node.left.gensprob[:, assleft]*node.right.gensprob[:, assright]
	return 


def up_down_down_stage(node):
	if (node is None) or isleaf(node):
		if isleaf(node):
			node.gensprobdown = node.gensprob
		return  
	node.gens = np.argmax(node.gensprob, axis=1)
	# node.gens = np.int64(np.random.randint(2, size=GENS))

	if node.parent != None:
		for assignment in [0,1]:
			for assparent in [ 0,1]:
				node.gensprobdown[:, assignment] +=\
					  FLIPdown[assparent, assignment] *\
					 node.parent.gensprobdown[:, assparent]
	else:
		node.gens = np.argmax(node.gensprob, axis=1)
		for j in range(GENS):
			for assignment in [0,1]:
				node.gensprobdown[j][assignment] = 1\
						if assignment == node.gens[j] else 0

	# print(node.gensprobdown)

	# node.gens = np.argmax(node.gensprob * node.gensprobdown , axis=1)
	up_down_down_stage(node.left)
	up_down_down_stage(node.right)

def diff(node,arr):
def up_down_assignment(node):
	if (node is None) or isleaf(node) :
		return
	# print(node.gensprob * node.gensprobdown)
	node.gens = np.argmax(node.gensprob * node.gensprobdown , axis=1)
	print(node.gens)
	up_down_assignment(node.left)
	up_down_assignment(node.right)


