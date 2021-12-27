import numpy as np
import matplotlib.pyplot as plt

def pltTree(root):

	def dfs(_newnode, x,y, depth=1, retx = [], rety = []):
		if _newnode is None:
			return
		retx.append(x)
		rety.append(y)
		eps = 1/(2**depth)
		dfs(_newnode.left, x-eps ,y-eps, depth+1, retx, rety)
		retx.append(x)
		rety.append(y)
		dfs(_newnode.right, x+eps, y-eps,depth+1, retx, rety)
		retx.append(x)
		rety.append(y)
	retx, rety = [], []
	dfs(root, 0,20, 1, retx, rety)
	plt.scatter(retx, rety, s=2, color='black')
	plt.plot(retx, rety, linewidth=0.5 )
	plt.title('NJ Tree')



def plot_groups(group, matrix):
	f = [ ]
	for (i,j) in group:
		f.append(matrix[i,j])
	plt.hist(f)
	


def plot_what_we_wish( ):
	q = np.random.normal( 0.8, 0.1, size=10000  )
	plt.hist(q, bins=40)
	plt.title('corlated')
	plt.ylabel('histogram')
	plt.savefig("./svg/what_we_wish_corlated.svg") 
	plt.clf()
	p = np.random.random(size=10000)
	plt.hist(p, bins=40)
	plt.title('uncoralted')
	plt.xlabel('')
	plt.ylabel('histogram')
	plt.savefig("./svg/what_we_wish_uncoralted.svg")
	plt.clf()

if __name__ == "__main__":
	plot_what_we_wish()