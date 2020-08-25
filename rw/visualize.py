# quick module to visualize
	# histograms
	# x/y plots
	#
# made for random walks visualization

from matplotlib import pyplot as plt 
import numpy as np

def lineplot(x, y):
	plt.plot(x,y)
	plt.show(block=True)