import numpy as np
import cmath
import scipy.ndimage as sci
import matplotlib.pyplot as plt

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

#setting up x coordinates
x_max = 1000000.0
delta = 0.5
N = int(x_max-1.0)
axis = np.linspace(1.0, x_max, N)
x_n = axis + complex(0, 1)*axis

#computation
for i in range(150):
    print(i)
    
    x_n = x_n - epsilon*f(x_n)/f_prime(x_n)

#plotting
fig, axes = plt.figure(), plt.axes()
results = sci.generic_filter(np.imag(x_n), filter, size=tuple([1]))
line = axes.scatter(axis, results)
plt.xlim([1.0, x_max])
plt.ylim([0.0, 1.0])
plt.show()
    
