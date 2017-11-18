
import matplotlib.pyplot as plt
import string

filename = "results_sweep.txt"
file = open(filename, "r")
flines = file.readlines()

filenames = ["results_sweep.txt"]


for j in range(len(filenames)):
	file = open(filename, "r")
	flines = file.readlines()

	x = []
	y = []

	for n in range(1, len(flines)):
		txt = string.split(flines[n]) 
		x.append(float(txt[ 0]))
		y.append(float(txt[ 1]))

	plt.axis('equal')
	plt.plot(x,y, linewidth=2)
	plt.ylabel('Y')
	plt.xlabel('X')
	plt.show()
