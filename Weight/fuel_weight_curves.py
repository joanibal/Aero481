import os,sys,inspect

sys.path.insert(1, os.path.join(sys.path[0], '..'))
import numpy as np
from weight_buildup import *
import matplotlib.pyplot as plt

def fuel_weight(sref_range, t_range):
	Z = np.empty([len(t_range), len(sref_range)])
	X, Y = np.meshgrid(sref_range, t_range)
	# for i in range(0, len(sref_range)-1):
	# 	for j in range(0, len(t_range)-1):
	# 		_, Z[j][i] = prelim_weight(sref_range[i], t_range[j])
	# return Z
	Z = prelim_weight(X, Y)

if __name__ == '__main__':
	fuel_curves = fuel_weight(np.linspace(750, 1400, 10), np.linspace(100, 30000, 20))
	# print fuel_curves
	# X, Y = np.meshgrid(np.linspace(4000, 30000, 20), np.linspace(750, 1400, 20))
	plt.contour(X, Y, fuel_curves)
	plt.show()