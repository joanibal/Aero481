import os,sys,inspect

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from constants import *
import numpy as np
from Sizing.horizontal_surf_sizing import MAC

root = 14.5 #ft
ratio = 0.75
sweep = 0.628319 #radians (36 degrees)

c_MAC, _ = MAC(root, ratio, 0)

x = c_MAC*np.tan(sweep)
Lvt = (fuse_length-63.97)-root+x
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

_, y_MAC = MAC(root, ratio, span)

print c_MAC*0.3048 , y_MAC #m
