from constants import *
import numpy as np

root = 14
ratio = 0.7
sweep = 0.628319 #radians
ratio2 = 0.66666666666
MAC1 = (root + ratio*root - (root*root*ratio)/(root+root*ratio))
MAC = MAC1*ratio2
x = MAC*np.tan(sweep)
Lvt = 40.48-root+x
print(Lvt)

Lvt = Lvt*0.3048 #moment arm in m
Svt = c_VT*b*Sref/Lvt
print(Svt)

base = root*0.3048
tip = base*ratio
print base, tip
span = 2*Svt/(base+tip)
print span

AR = span*span/Svt
print(AR)
