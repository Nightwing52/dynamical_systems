import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage as sci
import cmath

#coloring based on root it converged to (if it did)
def filter(a):
    val = a[0]

    if abs(val) < 0.0001:
        return 0.0
    elif abs(val+0.86603) < 0.0001:
        return 0.3
    elif abs(val-0.86603) < 0.0001:
        return 0.6
    return 1.0

#functions
f = lambda x : x**3-1
f_prime = lambda x : 3*x**2
epsilon = complex(0.5, 0.5)

#grid setup
xmax = 4
delta = 0.01
N = int(2*xmax/delta)
axis = np.linspace(-xmax, xmax, N)
xx, yy = np.meshgrid(axis, -axis)
yy = complex(0, 1)*yy
x_n = xx+yy

#applying Newton's method to each point
for i in range(100):
    print(i)

    x_n = x_n - epsilon*f(x_n)/f_prime(x_n)

    #exit if we have gotten close enough everywhere
    if np.all(sci.generic_filter(np.imag(x_n), filter, size=(1, 1)) < 0.8):
        break

#computing pixel color and displaying
fig, axes = plt.figure(), plt.axes()
pixels = sci.generic_filter(np.imag(x_n), filter, size=(1, 1))
heat_map = axes.imshow(pixels, cmap="gist_rainbow")
plt.show()
