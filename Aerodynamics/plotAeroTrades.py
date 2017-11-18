
import matplotlib.pyplot as plt
import string

filenames = ["results_sweep.txt", "results_taper.txt", "results_ar.txt", "results_sref.txt"]
xlabels = ["Sweep", "Taper Ratio", "Aspect Ratio", "Sref"]
ylabels = ["CL/CD", "CL/CD", "CL/CD", "CL/CD"]
x_min = [0, 0, 1, 900]
x_max = [40, 1, 16, 2500]

for j in range(len(filenames)):
	file = open(filenames[j], "r")
	flines = file.readlines()

	x = []
	y = []

	for n in range(1, len(flines)):
		txt = string.split(flines[n]) 
		x.append(float(txt[ 0]))
		y.append(float(txt[ 1]))

	plt.axis('equal')
	plt.plot(x,y, linewidth=2)
	#plt.xlim(x_min[j], x_max[j])
	axes = plt.gca()
	axes.set_xlim([x_min[j],x_max[j]])
	plt.xlabel(xlabels[j])
	plt.ylabel(ylabels[j])
	plt.show()