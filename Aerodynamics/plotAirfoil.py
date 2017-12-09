import os,sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import matplotlib.pyplot as plt
import string

f = open('./ItsCDRdudes.dat', 'r')
# f = open('./Airfoils/sc0012.dat', 'r')
flines = f.readlines()

X = []
Y = []
for j in range(1, len(flines)):
	words = string.split(flines[j]) 
	X.append(float(words[ 0]))
	Y.append(float(words[ 1]))


X.append(X[0])
Y.append(Y[0])


# print(X,Y)
plt.axis('equal')
plt.plot(X,Y, linewidth=2)
plt.ylabel('Y')
plt.xlabel('X')
plt.show()
