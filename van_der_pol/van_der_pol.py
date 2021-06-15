import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint
from matplotlib.animation import FuncAnimation
from functools import partial

#system
def van_der_pol(coords, t, mu):
    x, y = coords[0::2], coords[1::2]
    y_prime = mu*(1-x**2)*y-x
    out = np.column_stack([y, y_prime])
    return out.reshape(-1)

#initialize window for blitting
def init(fig, axes, scatter):
    plt.xlim([-3.0, 3.0])
    plt.ylim([-3.0, 3.0])
    axes.patch.set_facecolor("black")
    return scatter,

#animates one frame
def animate(t, sols, scatter):
    print(t)

    scatter.set_offsets(np.column_stack([sols[t][0::2], sols[t][1::2]]))
        
    return scatter,
    
#constants
mu = 0.5

#initial data
M = 50
axis = np.linspace(-2.5, 2.5, M)
init_conds = np.array([(x, y) for x in axis for y in axis])
init_conds = init_conds.reshape(2*M**2)

#solving
total = 20.0
delta = 0.1
N = int(total/delta)
t = np.linspace(0.0, total, N)
sols = odeint(van_der_pol, init_conds, t, args=tuple([mu]))

#setup
fig, axes = plt.figure(), plt.axes(frameon=True)
scatter = plt.scatter([], [], animated=True, c="white", s=1.0)

#animation
anim = FuncAnimation(fig, func=animate, frames=N, init_func=partial(init, fig, axes, scatter), blit=True, fargs=(sols, scatter), repeat=False)
anim.save("out.mp4", fps=40)
