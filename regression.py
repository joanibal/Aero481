def regression():
	import numpy as np
	import scipy

	WTO = np.array([92500, 69600, 73000, 99600])
	WE = np.array([50861, 43500, 36100, 54000])

	(a_lin, b_lin)= np.polyfit(np.log10(WTO),np.log10(WE),1)

	c = a_lin-1
	a = 10**b_lin

	# print (a, c)
	return a/2, c/2
