
import matplotlib.pyplot as plt
import string

f = open('./sc20612-il.dat', 'r')
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
