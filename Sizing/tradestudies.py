import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))
import numpy as np
# import g550 as plane
import j481 as plane
# from gen_files import gen_geo
import matplotlib.pyplot as plt
from copy import deepcopy

from Aerodynamics.avlLib import  gen_geo
# from Aerodynamics.gen_files import gen_geo

from Weight.weight_refined import prelim_weight



FB_sweep = []
FB_taper = []
FB_AR = []
FB_Sref = []
FB_frac = []

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


print(' ===============  AR ==============')
AR_inital = 5
AR_final = 40
ARs = np.linspace(AR_inital, AR_final, 100)


AR_0 = deepcopy(plane.wing.aspect_ratio)

for ratio in ARs:

	plane.wing.update(aspect_ratio=ratio)
	print plane.wing.aspect_ratio
	for key in plane.e.keys():
		plane.k[key] = 1. / (np.pi * plane.wing.aspect_ratio * plane.e[key])

	# gen_geo(plane.Sref, plane.wing.MAC_c, plane.wing.span,
	#         np.array([plane.wing.offset[0] + plane.wing.MAC_c*.25, 0, 0]), 0, plane, file='Aerodynamics/'+ plane.name+'.avl')

	FB_AR.append(prelim_weight(plane.Sref, plane.thrust_req, plane)[1])

plt.plot(ARs, FB_AR)
plt.plot(AR_0, w_f0, 'ro', label='Design Point')
plt.xlabel('Aspect Ratio', size='x-large')
plt.ylabel('Fuel Burn [lb]', size='x-large')
plt.show()


plane.wing.aspect_ratio = AR_0


# print(' ===============  sweep ==============')
# sweep_inital = 0
# sweep_final = 60
# sweeps = np.linspace(sweep_inital, sweep_final, 100)


# sweep_0 = deepcopy(plane.wing.sweep)

# for param in sweeps:

# 	plane.wing.update(sweep=param)
# 	print plane.wing.sweep

# 	# gen_geo(plane.Sref, plane.wing.MAC_c, plane.wing.span,
# 	#         np.sweepray([plane.wing.offset[0] + plane.wing.MAC_c*.25, 0, 0]), 0, plane, file='Aerodynamics/'+ plane.name+'.avl')

# 	FB_sweep.append(prelim_weight(plane.Sref, plane.thrust_req, plane)[1])

# plt.plot(sweeps, FB_sweep)
# plt.plot(sweep_0, w_f0, 'ro', label='Design Point')
# plt.xlabel('sweep [Deg]', size='x-large')
# plt.ylabel('Fuel Burn [lb]', size='x-large')
# plt.show()


# plane.wing.sweep = sweep_0


# print(' ===============  taper ==============')
# taper_inital = 0.1
# taper_final = 0.6
# tapers = np.linspace(taper_inital, taper_final, 10)


# taper_0 = deepcopy(plane.wing.taper)

# for param in tapers:

# 	plane.wing.update(taper=param)
# 	print plane.wing.taper

# 	# gen_geo(plane.Sref, plane.wing.MAC_c, plane.wing.span,
# 	#         np.taperray([plane.wing.offset[0] + plane.wing.MAC_c*.25, 0, 0]), 0, plane, file='Aerodynamics/'+ plane.name+'.avl')

# 	FB_taper.append(prelim_weight(plane.Sref, plane.thrust_req, plane)[1])

# plt.plot(tapers, FB_taper)
# plt.plot(taper_0, w_f0, 'ro', label='Design Point')
# plt.xlabel('taper')
# plt.ylabel('Fuel Burn [lb]')
# plt.show()


# plane.wing.aspect_ratio = taper_0


# print(' ===============  sref ==============')
# sref_inital = 350.
# sref_final = 2000.
# srefs = np.linspace(sref_inital, sref_final, 100)


# sref_0 = deepcopy(plane.Sref)

# for param in srefs:

# 	# plane..update(sref=param)
# 	print plane.Sref

# 	# gen_geo(plane.Sref, plane.wing.MAC_c, plane.wing.span,
# 	#         np.srefray([plane.wing.offset[0] + plane.wing.MAC_c*.25, 0, 0]), 0, plane, file='Aerodynamics/'+ plane.name+'.avl')

# 	FB_Sref.append(prelim_weight(param, plane.thrust_req, plane)[1])

# plt.plot(srefs, FB_Sref)
# plt.plot(sref_0, w_f0, 'ro', label='Design Point')
# plt.xlabel('Sref [$ft^2$]', size='x-large')
# plt.ylabel('Fuel Burn [lb]', size='x-large')
# plt.show()


# plane.Sref = sref_0

# print(' ===============  sref fac ==============')


# # plane.wing.Nspan = 28 
# # plane.canard.Nspan = 18 

# plane.wing.update()
# plane.canard.update()


# frac_inital = 1/10.
# frac_final = .225
# fracs = np.linspace(frac_inital, frac_final, 100)


# frac_0 = deepcopy(plane.canard_area_ratio)





# for param in fracs:

# 	# plane..update(frac=param)
# 	# print plane.wing.frac
# 	plane.canard_area_ratio = param
# 	plane.wing_area_ratio = 1 - plane.canard_area_ratio
# 	print plane.canard_area_ratio
# 	# gen_geo(plane.frac, plane.wing.MAC_c, plane.wing.span,
# 	#         np.fracray([plane.wing.offset[0] + plane.wing.MAC_c*.25, 0, 0]), 0, plane, file='Aerodynamics/'+ plane.name+'.avl')

# 	FB_frac.append(prelim_weight(plane.Sref, plane.thrust_req, plane)[1])

# plt.plot(fracs, FB_frac)
# plt.plot(frac_0, w_f0, 'ro', label='Design Point')
# plt.xlabel('Canard Area Fraction', size='x-large')
# plt.ylabel('Fuel Burn [lb]', size='x-large')
# plt.show()


# plane.frac = sref_0

