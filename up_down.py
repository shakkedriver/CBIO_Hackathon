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
# MATRIXP = FLIP 

def isleaf(node):
	return ( node.left is None) and (node.right is None)

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
					FLIP[ (assignment, assleft, assright) ] *node.weightleft*node.weightright*\
						 node.left.gensprob[:, assleft]*node.right.gensprob[:, assright]
	return 

def up_down_down_stage(node):
	if node is None:
		return  
	node.gens = np.argmax(node.gensprob, axis=1)
	up_down_down_stage(node.left)
	up_down_down_stage(node.right)

def diff(node):
	if isleaf(node):
		return
	cc = 0
	for i in range(len(node.left.gens)):
		if node.left.gens[i] != node.right.gens[i]:
			cc = 1
	if (cc == 1):
		print("diff")
	else:
		print("equl")
	diff(node.left)
	diff(node.right)


	
