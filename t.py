import matplotlib.pyplot as plt
import numpy as np

mat = np.random.random((100, 100))
def hit_map(mat):
    plt.imshow(mat,cmap = "hot")
    plt.savefig("u.png")

def get_two_groups(mat, threshold):
    corlated = np.where(mat>=threshold)
    corlated = list(zip(corlated[0],corlated[1]))
    uncoralted = np.where(mat<threshold)
    uncoralted = list(zip(uncoralted[0], uncoralted[1]))
    # uncoralted = [a for a in uncorlated if a[0] > a[1]]
    return corlated,uncoralted



if __name__ == "__main__":
    hit_map(mat)