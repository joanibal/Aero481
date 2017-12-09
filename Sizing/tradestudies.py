import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))
import numpy as np
import j481 as plane
# from gen_files import gen_geo
import matplotlib.pyplot as plt
from copy import deepcopy

# from Aerodynamics.avlLib import  changeSref
# from Aerodynamics.gen_files import gen_geo

from Weight.weight_refined import prelim_weight



FB_sweep = []
FB_taper = []
FB_AR = []
FB_Sref = []
FB_SrefSplit = []

w_0, w_f0, w_other = prelim_weight(plane.Sref, plane.thrust_req, plane)





# # # # ===============  Sweep ==============
# print(' ===============  Sweep ==============')
# sweep_inital = 0.0 
# sweep_final = 60.0
# sweeps = np.linspace(sweep_inital, sweep_final, 20)

# sweep_0 = deepcopy(plane.wing.sweep)


# for angle in sweeps:

# 	plane.wing.update(sweep=angle)
# 	FB_sweep.append( prelim_weight(plane.Sref, plane.thrust_req, plane)[1])

# plt.plot(sweeps, FB_sweep)
# plt.plot(sweep_0, w_f0, 'ro', label='Design Point')
# plt.xlabel('Sweep [Degrees]')
# plt.ylabel('Fuel Burn [lb]')
# plt.show()


# plane.wing.sweep = sweep_0
# print plane.wing.sweep
# # # # ===============  Sweep ==============
# print(' ===============  taper ==============')
# taper_inital = 1.0
# taper_final = 0.0
# tapers = np.linspace(taper_inital, taper_final, 20)


# taper_0 = deepcopy(plane.wing.taper)

# for ratio in tapers:

# 	plane.wing.update(taper=ratio)
# 	FB_taper.append(prelim_weight(plane.Sref, plane.thrust_req, plane)[1])

# plt.plot(tapers, FB_taper)
# plt.plot(taper_0, w_f0, 'ro', label='Design Point')
# plt.xlabel('taper [Degrees]')
# plt.ylabel('Fuel Burn [lb]')
# plt.show()


# plane.wing.taper = taper_0
# # # ===============  Sweep ==============
print(' ===============  AR ==============')
AR_inital = 7
AR_final = 13
ARs = np.linspace(AR_inital, AR_final, 20)


AR_0 = deepcopy(plane.wing.aspect_ratio)

for ratio in ARs:

	plane.wing.update(aspect_ratio=ratio)

	for key in plane.e.keys():
		plane.k[key] = 1. / (np.pi * plane.wing.aspect_ratio * plane.e[key])
	FB_AR.append(prelim_weight(plane.Sref, plane.thrust_req, plane)[1])

plt.plot(ARs, FB_AR)
plt.plot(AR_0, w_f0, 'ro', label='Design Point')
plt.xlabel('AR [Degrees]')
plt.ylabel('Fuel Burn [lb]')
plt.show()


plane.wing.aspect_ratio = AR_0
