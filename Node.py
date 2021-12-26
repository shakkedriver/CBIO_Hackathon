import numpy as np

GENS = 100
`
class Node:	
	def __init__(self):
		self.left, self.right, self.parent = None, None, None
		self.weightleft, self.weightright = 0,0 
		self.gens = np.zeros(GENS)
		self.gensprob = np.zeros((GENS,2))
		self.change = None
