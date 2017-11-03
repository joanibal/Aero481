import os,sys,inspect

sys.path.insert(1, os.path.join(sys.path[0], '..'))
import numpy as np
from weight_buildup import *
import matplotlib.pyplot as plt
import constants as consts

def fuel_weight(sref_range, t_range):
	Z = np.empty([len(t_range), len(sref_range)])
	X, Y = np.meshgrid(sref_range, t_range)
	for i in range(len(sref_range)):
		for j in range(len(t_range)):
			_, Z[j][i] = prelim_weight(sref_range[i], t_range[j],consts)
	return X, Y, Z
	# Z = prelim_weight(X, Y)

if __name__ == '__main__':
	X, Y, fuel_curves = fuel_weight(np.linspace(1300, 2000), np.linspace(100, 50000))
	# print fuel_curves
	# X, Y = np.meshgrid(np.linspace(4000, 30000, 20), np.linspace(750, 1400, 20))
	CS = plt.contour(X, Y, fuel_curves)

	cbar = plt.colorbar(CS)
	cbar.ax.set_ylabel('Fuel Weight')

	plt.show()
