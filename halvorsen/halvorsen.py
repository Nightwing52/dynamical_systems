import matplotlib.pyplot as plt
import numpy as np
from matplotlib import collections as mc
from scipy.integrate import odeint
from mpl_toolkits.mplot3d import art3d as art
from mpl_toolkits.mplot3d import axes3d as axes3d
from functools import partial
from matplotlib.animation import FuncAnimation

#system
def halvorsen(coords, t, a):
    x, y, z = coords[0::3], coords[1::3], coords[2::3]
    x_prime = -a*x-4*y-4*z-y**2
    y_prime = -a*y-4*z-4*x-z**2
    z_prime = -a*z-4*x-4*y-x**2
    out = np.column_stack([x_prime, y_prime, z_prime])
    return out.reshape(-1)

#initialize window for blitting
def init(fig, axes, lc):
    axes.add_collection3d(lc)
    axes.set_zlim(-10.0, 8.0)
    axes.set_ylim(-10.0, 8.0)
    axes.set_xlim(-10.0, 7.0)
    axes.set_axis_off()
    return lc,

#animates one frame
def animate(t, axes, angle, lc):
    print(t)
    axes.view_init(10.0, angle[t])
    return lc,

#constants
a = 1.4

#initial data
M = 4
axis = np.linspace(1.0, 3.0, M)
init_conds = np.array([(x, y, z) for x in axis for y in axis for z in axis])
init_conds = init_conds.reshape(-1)

#solving
total = 10.0
delta = 0.05
N = int(total/delta)
t = np.linspace(0.0, total, N)
sols = odeint(halvorsen, init_conds, t, args=tuple([a]))

#setup
fig = plt.figure()
axes = axes3d.Axes3D(fig)
lines = []
sols = np.transpose(sols)
cut = int(5.0/delta)
for i in range(0, len(sols), 3):
    x, y, z = sols[i][cut:], sols[i+1][cut:], sols[i+2][cut:]
    lines.append(np.column_stack([x, y, z]))
lc = art.Line3DCollection(lines, colors="black")

#animation
M = 720
angle = np.linspace(0.0, M, M)
anim = FuncAnimation(fig, func=animate, frames=M, init_func=partial(init, fig, axes, lc), blit=True, fargs=(axes, angle, lc), repeat=False)
anim.save("out.mp4", fps=40)
