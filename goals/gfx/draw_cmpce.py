import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

size = 1500, 1000
figsize = (size[0]/100.0, size[1]/100.0)

figure = plt.figure(figsize = figsize, dpi = 100, facecolor = 'white', edgecolor = 'white')
ident_plot = figure.add_subplot(231)
exp_plot   = figure.add_subplot(232)
log1_plot  = figure.add_subplot(234)
log02_plot  = figure.add_subplot(235)
log001_plot  = figure.add_subplot(236)

span = 1.0
alpha = 2

logval = 1.0, 0.2, 0.05

x,y = np.ogrid[0.0:span:span/1000, 0.0:span:span/1000]
z_ident =  y - x
z_exp   =  np.exp(-alpha*x) - np.exp(-alpha*y)
z_log1   = -np.log((logval[0]+x)/logval[0]) + np.log((logval[0]+y)/logval[0])
z_log02  = -np.log((logval[1]+x)/logval[1]) + np.log((logval[1]+y)/logval[1])
z_log001 = -np.log((logval[2]+x)/logval[2]) + np.log((logval[2]+y)/logval[2])

def configure_subplot(plot, z, title):

    plot.set_title(title, size = 10)
    heatmap = plot.imshow(z, origin='lower', extent=[0.0,span,0.0,span])
    plot.contour(z, origin='lower', extent=[0.0,span,0.0,span])
    plot.tick_params(labelsize = 8)
    plot.set_xlabel('c1', size = 10)
    plot.set_ylabel('c2', size = 10)
    divider = make_axes_locatable(plot)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    cb = figure.colorbar(heatmap, cax = cax)
    cb.ax.tick_params(labelsize=8)

configure_subplot(ident_plot,  z_ident, 'c2 - c1')
configure_subplot(exp_plot,    z_exp,   'exp(-{}*c1) - exp(-{}*c2)'.format(alpha, alpha))
configure_subplot(log1_plot,   z_log1,  '- log(({}+c1)/{}) + log(({}+c2)/{})'.format(logval[0],logval[0],logval[0],logval[0]))
configure_subplot(log02_plot,  z_log02,  '- log(({}+c1)/{}) + log(({}+c2)/{})'.format(logval[1],logval[1],logval[1],logval[1]))
configure_subplot(log001_plot, z_log001,  '- log(({}+c1)/{}) + log(({}+c2)/{})'.format(logval[2],logval[2],logval[2],logval[2]))

figure.subplots_adjust(bottom=0.05, left=0.1, right=0.9, top=0.95, hspace=0.25)
plt.show()