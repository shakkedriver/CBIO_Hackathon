import numpy as np
import matplotlib.pyplot as plt

import cairo
from cairo import SVGSurface, Context, Matrix    

def pltTree(root):

	def dfs(_newnode, x,y, retx = [], rety = []):
		if _newnode is None:
			return
		retx.append(x)
		rety.append(y)
		dfs(_newnode.left, x-1,y-1, retx, rety)
		retx.append(x)
		rety.append(y)

		dfs(_newnode.right, x+1, y-1, retx, rety)
		
	retx, rety = [], []
	dfs(root, 0,20, retx, rety)
	plt.scatter(retx, rety, s=2, color='black')
	plt.plot(retx, rety, linewidth=0.5 )
	plt.title('NJ Tree')
	plt.show()
