import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage.filters import generic_filter

#computes change matrix
def change(a):
    a = a.reshape((3, 3))

    result = 0
    if a[1, 1] >= 4:
        result -= 4
    if a[0, 1] >= 4:
        result += 1
    if a[1, 0] >= 4:
        result += 1
    if a[1, 2] >= 4:
        result += 1
    if a[2, 1] >= 4:
        result += 1
    return result

#colors grid
def color(a):
    val = a[0]

    if val == 0:
        return 0.0
    elif val == 1:
        return 0.25
    elif val == 2:
        return 0.5
    elif val == 3:
        return 0.75
    else:
        return 1.0

#initial data
N = 128
grid = np.zeros((N, N))
center = (int(N/2)-1, int(N/2)-1)

MASS = 1000000
grid[center] = MASS

#setup
fig, axes = plt.figure(), plt.axes()
pixels = generic_filter(grid, color, size=(1, 1))
heat_map = axes.imshow(pixels, cmap="gist_rainbow")

#computation
steps = 10000000
for step in range(steps):
    print(step)
    
    #find change matrix
    delta = generic_filter(grid, change, size=(3, 3), mode="constant")
    
    #update
    grid += delta
    
    #occasional update
    if step % 5000 == 0:
        pixels = generic_filter(grid, color, size=(1, 1))
        heat_map.set_data(pixels)
        plt.savefig("image"+str(int(step/5000)).zfill(3)+".png")

plt.show()
