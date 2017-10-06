def regression():
	import numpy as np
	import scipy
	import matplotlib.pyplot as plt

	# WTO = np.array([92500, 69600, 73000, 99600])
	# WE = np.array([50861, 43500, 36100, 54000])

	WTO = np.array([92500, 69600, 73000, 174200, 99600, 30800, 51000, 23500, 91000, 120152, 33500, 41000, 13870, 1268000, 987000])
	WE = np.array([50861, 43500, 36100, 102100, 54000, 18656, 30500, 14640, 48300, 70841, 24200, 20735, 8540, 610000, 485300])

	# (a_lin, b_lin)= np.polyfit(np.log10(WTO[:-3]),np.log10(WE[:-3]),1)
	(a_lin, b_lin)= np.polyfit(np.log10(WTO),np.log10(WE),1)

	c = a_lin-1
	a = 10**b_lin

	# print (a, c)

	# plt.plot(np.log10(WTO), np.log10(WE), 'o', label='Original data', markersize=10)
	# plt.plot(np.log10(WTO), a_lin*np.log10(WTO) + b_lin, 'r', label='Fitted line')
	# plt.legend()
	# plt.show()
	return a, c
