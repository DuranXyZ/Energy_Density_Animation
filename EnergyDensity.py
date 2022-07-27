import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import animation
from mpl_toolkits.axes_grid1 import make_axes_locatable
# Initial conditions
p_elec=1.1
dead=6.885
v=2.15
q=800
k=100
##
N = 150 # Meshsize
fps = 10 # frame per sec
frn = 100 # frame number of the animation
x = np.linspace(1,10,N+1)
x, y = np.meshgrid(x, x)
zarray = np.zeros((N+1, N+1, frn))
G= lambda x,y,b:v*q*(x)/(dead+(x/(b/100))+((p_elec*y)*x)+((14/32)*(1+(k/100))*x))

for i in range(frn):
    zarray[:,:,i] = G(x,y,60+20*np.sin(i*2*np.pi/frn))
def update_plot(frn, zarray, plot):
    plot[0].remove()
    plot[0] = ax.plot_surface(x, y, zarray[:,:,frn], cmap="jet")
    c = round(60 + 20 * np.sin(frn * 2 * np.pi /(i+1)),1)
    tx.set_text('Cathode sulfur content {0} %'.format(c))
    # fig.colorbar(plot[0], orientation='vertical', shrink=0.5, aspect=10, pad=0.15)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
div = make_axes_locatable(ax)
tx = ax.set_title('Sulfur content 60+20*np.sin(i*2*np.pi/frn)')
plot = [ax.plot_surface(x, y, zarray[:,:,0], color='0.75', rstride=1, cstride=1)]
ax.set_xlim([1, 10])
ax.set_ylim([1, 10])
ax.set_zlim([50, 450])
ax.set_xlabel('Sulfur loading mg/$cm^2$')
ax.set_ylabel('E/S ratio (uL/mg)')
ax.set_zlabel('Specific energy $W_G$ (Wh/kg)')
ax.view_init(12,135)
ani = animation.FuncAnimation(fig, update_plot, frn, fargs=(zarray, plot), interval=1000/fps)
ani.save('GravimetricContent.gif', writer='pillow', fps=15)
plt.show()

# fig = plt.figure()
# ax = fig.add_subplot(111)

# fig = plt.figure()
# ax = fig.add_subplot(111)
# # I like to position my colorbars this way, but you don't have to
# div = make_axes_locatable(ax)
# cax = div.append_axes('right', '5%', '5%')
#
# def f(x, y):
#     return np.exp(x) + np.sin(y)
#
# x = np.linspace(0, 1, 120)
# y = np.linspace(0, 2 * np.pi, 100).reshape(-1, 1)
#
# # This is now a list of arrays rather than a list of artists
# frames = []
# for i in range(10):
#     x       += 1
#     curVals  = f(x, y)
#     frames.append(curVals)
#
# cv0 = frames[0]
# im = ax.imshow(cv0, origin='lower') # Here make an AxesImage rather than contour
# cb = fig.colorbar(im, cax=cax)
# tx = ax.set_title('Frame 0')
#
# def animate(i):
#     arr = frames[i]
#     vmax     = np.max(arr)
#     vmin     = np.min(arr)
#     im.set_data(arr)
#     im.set_clim(vmin, vmax)
#     tx.set_text('Frame {0}'.format(i))
#     # In this version you don't have to do anything to the colorbar,
#     # it updates itself when the mappable it watches (im) changes
#
# ani = animation.FuncAnimation(fig, animate, frames=10)
#
# plt.show()