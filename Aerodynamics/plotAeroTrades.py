
import matplotlib.pyplot as plt
import string

filenames = ["results_sweep.txt", "results_taper.txt", "results_ar.txt", "results_sref.txt"]
xlabels = ['Sweep, ' + '$\Lambda$' + ' (deg)', 'Taper, ' + '$\lambda$', 'Aspect Ratio, AR', '$S_{ref}$']
ylabels = ["CL/CD", "CL/CD", "CL/CD", "CL/CD"]
titles = ["Aerodynamics: Sweep Study", "Aerodynamics: Taper Ratio Study", "Aerodynamics: Aspect Ratio Study", "Aerodynamics: Reference Area Study"]
#x_min = [0, 0, 1, 900]
#x_max = [40, 1, 16, 2500]

for j in range(len(filenames)):
	file = open(filenames[j], "r")
	flines = file.readlines()

	x = []
	y = []

	for n in range(0, len(flines)):
		txt = string.split(flines[n]) 
		x.append(float(txt[ 0]))
		y.append(float(txt[ 1]))

	plt.axis('auto')
	plt.plot(x,y, linewidth=2)
	plt.title(titles[j])
	plt.ylabel('${C_L}/{C_D}$')
	plt.xlabel(xlabels[j])
	#plt.xlim(x_min[j], x_max[j])
	#axes = plt.gca()
	#axes.set_xlim([x_min[j],x_max[j]])
	#plt.xlabel(xlabels[j])
	#plt.ylabel(ylabels[j])
	plt.show()

