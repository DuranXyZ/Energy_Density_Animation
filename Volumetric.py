import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from mpl_toolkits.axes_grid1 import make_axes_locatable
# Initial conditions
v,q=2.15,800  # Battery characteristics (Note 'e' is porosity)
Seperator,Anode,Cathode=0.0015,0.00045,0.00075 # Dead thicknesses
p_bi,p_sp,p_s,p_li=1.76,1.6,2.07,0.534 # Density of binder, conductive, sulfur,lithium
e_seperator=39 # Seperator porosity
V=v*q/(10**6)
# # Variables we can change
k=100                        # Lithium Excess %
b=60                         # Sulfur content %
e=40                         # Cathode porosity %
p_h=0.17                   # Host density
# Animation Frames
N = 150 # Meshsize
fps = 25 # frame per sec
frn = 300 # frame number of the animation
frames=frn
x = np.linspace(1,10,N+1)
x, y = np.meshgrid(x, x)
zarray = np.zeros((N+1, N+1, frn))
def V_func(x,y,p_h,e):
   p_theoretical = ((b/100)/p_s+(0.85-(b/100))/p_h+0.10/p_sp+0.05/p_bi)**-1 # Theoretical density of the cathode
   C = x*0.001/(p_theoretical*(b/100))/(1-(e/100))                      # Cathode thickness
   E = 0.001*(y*x)-(e_seperator/100)*Seperator-(e/100)*C                # Electrolyte thickness
   E[E < 0] = 0                                                        # Makes all negative matrix values 0
   Li = 14*(1+(k/100))*x/(32*1000*p_li)                               # Anode thickness
   Z = 1000*(V*x)/(C+Seperator+Anode+Cathode+E+Li)
   return Z

for i in range(frn):
    if i<frn/4:
        zarray[:, :, i] = V_func(x, y, 4.88 , 50 + 30 * np.sin(i * 2 * np.pi / (frn/4)))
    elif i<round(frn/2):
        zarray[:, :, i] = V_func(x, y, 3.27 , 50 + 30 * np.sin(i * 2 * np.pi / (frn/4)))
    elif i<round(3*frn/4):
        zarray[:, :, i] = V_func(x, y, 1.2, 50 + 30 * np.sin(i * 2 * np.pi / (frn /4)))
    else:
        zarray[:, :, i] = V_func(x, y, 0.17, 50 + 30 * np.sin(i * 2 * np.pi / (frn /4)))
def update_plot(frn, zarray, plot):
    plot[0].remove()
    plot[0] = ax.plot_surface(x, y, zarray[:,:,frn], cmap="jet")
    c = round(50 + 30 * np.sin(frn * 8 * np.pi /(i+1)),1)
    if frn<round(frames/4):
      tx.set_text('TiC Host, Cathode Porosity {0} % '.format(c))
    elif frn<round(frames/2):
      tx.set_text('Mn$O_2$ Host, Cathode Porosity {0} % '.format(c))
    elif frn<round(3*frames/4):
      tx.set_text('Ketjen Black Host, Cathode Porosity {0} % '.format(c))
    else:
      tx.set_text('COF-108 Host, Cathode Porosity {0} % '.format(c))
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
div = make_axes_locatable(ax)
tx = ax.set_title('Lithium Excess 50+50*np.sin(i*2*np.pi/frn)')
plot = [ax.plot_surface(x, y, zarray[:,:,0], color='0.75', rstride=1, cstride=1)]
ax.set_xlim([1, 10])
ax.set_ylim([1, 10])
ax.set_zlim([50, 600])
ax.set_xlabel('Sulfur loading mg/$cm^2$')
ax.set_ylabel('E/S ratio (uL/mg)')
ax.zaxis.set_rotate_label(False)
ax.set_zlabel('Specific energy $W_V$ (Wh/L)', rotation=90)
ax.view_init(24,37)
ani = animation.FuncAnimation(fig, update_plot, frn, fargs=(zarray, plot), interval=1000/fps)
ani.save('VolumetricPorosityCombo.gif', writer='pillow', fps=20)
plt.show()

