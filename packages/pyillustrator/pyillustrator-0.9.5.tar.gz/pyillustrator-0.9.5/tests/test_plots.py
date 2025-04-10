from pyillustrator.plots import grid_plot, grid_plot_double
import matplotlib.pyplot as plt

config = {}
config['xlim']  = [0,2]

#grid_plot(3,2,config)
grid_plot_double(3,2,config,'Horizontal')
grid_plot_double(3,2,config,'Vertical')

plt.show()