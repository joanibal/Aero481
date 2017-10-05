from constants import *
import numpy as np

root = 14 #ft
ratio = 0.7
sweep = 0.628319 #radians (36 degrees)
ratio2 = 0.66666666666
MAC1 = (root + ratio*root - (root*root*ratio)/(root+root*ratio))
MAC = MAC1*ratio2
x = MAC*np.tan(sweep)
Lvt = (fuse_length-CG)-root+x
print(Lvt) #in ft

Lvt = Lvt*0.3048 #moment arm in m
Svt = c_VT*b*Sref/Lvt
print(Svt)

base = root*0.3048 #convert to m
tip = base*ratio #m
print base
span = 2*Svt/(base+tip)
print span

AR = span*span/Svt
print(AR)
