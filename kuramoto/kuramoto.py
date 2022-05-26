import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint
from matplotlib.animation import FuncAnimation
from functools import partial

#system
def kuramoto(theta, t, A, N):
    difference_matrix = np.column_stack([theta - theta[k] for k in range(N)])
    theta_prime = np.array([np.dot(A[:, k], difference_matrix[:, k]) for k in range(N)])
    return 0.7*theta_prime

#initialize window for blitting
def init(fig, axes, scatter, N, points_map, A):
    plt.xlim([-1.5, 1.5])
    plt.ylim([-1.5, 1.5])
    plt.grid(False)
    plt.axis("off")
    #axes.patch.set_facecolor("black")

    #we draw the line connecting vertices once
    for i in range(N):
        curr = points_map[i]
        row = A[i]
        for j, connected in enumerate(row):
            if connected:
                conn_point = points_map[j]
                plt.plot([curr[0], conn_point[0]], [curr[1], conn_point[1]], color="black", markersize=1.0)
   
    return scatter,

#animates one frame
def animate(t, sols, scatter):
    print(t)
    
    scatter.set_array((sols[t] - 0.03*t) % 2*np.pi)

    return scatter,

#point generation
N = 20
axis = np.linspace(0.0, 2*np.pi, N+1)[0 : N]
points = np.column_stack([np.cos(axis), np.sin(axis)])
points_map = dict(zip(range(N), zip(points[:, 0], points[:, 1])))

#connecting vertices
np.random.seed(1000)
rand = np.random.rand(N, N)
A = np.zeros((N, N))
for i in range(N):
    for j in range(i, N):
        if rand[i, j] > 0.75:
            A[i, j], A[j, i] = 1, 1

#solving
total = 5.0
delta = 0.01
M = int(total/delta)
t = np.linspace(0.0, total, M)
sols = odeint(kuramoto, axis, t, args=tuple([A, N]))

#setup
fig, axes = plt.figure(), plt.axes(frameon=True)
scatter = plt.scatter(points[:, 0], points[:, 1], animated=True, c=axis, vmin=0.0, vmax=2*np.pi, cmap="rainbow", s=100)
anim = FuncAnimation(fig, func=animate, frames=M, init_func=partial(init, fig, axes, scatter, N, points_map, A), blit=True, fargs=(sols, scatter), repeat=False)
anim.save("out.mp4", fps=40)
