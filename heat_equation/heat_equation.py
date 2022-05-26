import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import scipy.ndimage as sci
from functools import partial

#raycasts
def in_poly(P, boundary):
    cnt = 0
    
    for i, point in enumerate(boundary[0 : len(boundary)-2]):
        next_point = boundary[i+1]
        print(i)
        print(point)
        m = (next_point[1]-point[1])/(next_point[0]-point[0])
        if abs(m) < 0.00001:
            continue
        inter = (P[1]-point[1])/m +point[0]
        
        if inter > P[0]:
            cnt+=1

    if cnt % 2 == 1:
        return 1
    else:
        return 0
    
theta = np.linspace(0.0, 2*np.pi, 100)
r = np.cos(4*theta)+2.0
x, y = r*np.cos(theta), r*np.sin(theta)
plt.plot(x, y)

N = 10
in_shape = np.zeros((N, N), dtype=bool)
axis = np.linspace(-3.5, 3.5, N) 
xx, yy = np.meshgrid(axis, axis)
yy = np.flipud(yy)
boundary = [(x[i], y[i]) for i in range(len(x))]

for i in range(N):
    for j in range(N):
        in_shape[i, j] = in_poly((xx[i, j], yy[i, j]), boundary)

print(in_shape)


