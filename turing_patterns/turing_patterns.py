import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import scipy.ndimage as sci
from functools import partial
 
plt.style.use("ggplot")
 
#initializes static elements
def init_fig(fig, axes, artist):
    axes.axes.get_xaxis().set_visible(False)
    axes.axes.get_yaxis().set_visible(False)
    axes.get_xaxis().tick_bottom()
    artist.set_clim([0.0, 1.0])
    artist.set_cmap("rainbow")
    artist.set_interpolation("quadric")
    fig.colorbar(heat_map)
    return artist,
 
#returns data needed to update artist
def animate(t, N, heat_map, A, B, D_A, D_B, kern, f, k):
    print(t)
    
    #derivative matrix
    dA = np.zeros([N, N])
    dB = np.zeros([N, N])

    #calculate derivative
    laplace_A, laplace_B = sci.convolve(A, kern, mode="constant", cval=1.0), sci.convolve(B, kern, mode="constant", cval=0.0)
    reaction = A*B**2
    dA = D_A*laplace_A - reaction + f*(1-A)
    dB = D_B*laplace_B + reaction - (k+f)*B
 
    #evolving
    A += dA
    B += dB
 
    heat_map.set_data(A)
    return heat_map,
 
#Laplace operator at a point
def laplace(matrix, cell, conv):
    values = matrix[cell[0]-1 : cell[0]+2, cell[1]-1 : cell[1]+2]
    return np.sum(conv*values)
 
#initial data
kern = np.array([[0.05, 0.2, 0.05], [0.2, -1.0, 0.2], [0.05, 0.2, 0.05]])
D_A, D_B, f, k = 1.0, 0.5, 0.0545, 0.062
t = 7000
 
N = 256
A, B = np.ones([N, N]), np.zeros([N, N])
for i in range(-int(N/4), int(N/4)):
    for j in range(-int(N/4), int(N/4)):
        B[int(N/2)-10+i, int(N/2)-10+j] = 1.0
 
#figure setup
fig, axes = plt.figure(), plt.axes(frameon = True)
heat_map = axes.imshow(A, animated = True)
 
init = partial(init_fig, fig=fig, axes=axes, artist=heat_map)
 
#animate
anim = FuncAnimation(fig, func=animate, frames=t, init_func=init, blit=True, fargs=(N, heat_map, A, B, D_A, D_B, kern, f, k))
anim.save("out.mp4", fps=40)
