import os,sys,inspect

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import numpy as np 

def weight_calc(Sref, AR, tc, taper_ratio, sweep_angle, constants):

	M = constants[0]
	N = constants[1]
	wing_mounted_area = constants[2]
	b = constants[3]
	c_root = constants[4]

	sweep_halfchord = np.arctan((0.5*b*np.arctan(sweep_angle)-0.25*c_root + 0.25*taper_ratio*c_root)/(0.5*b))

	Wwing_carichner = (0.00428*Sref**0.48)*((AR*M**0.43)/(100*tc)**0.76)*((w_0*N)**0.84*taper_ratio**0.14)/(np.cos(sweep_halfchord)**1.54)
	Wwing_raymer = 0.0051*((w_0*N)**0.557)*(Sref**0.649)*(AR**0.5)*(tc**(-0.4))*((1+taper_ratio)**0.1)*(np.cos(sweep_angle)**(-1))*(wing_mounted_area**0.1)

	Wwing = (Wwing_carichner + Wwing_raymer)/2.0
	return Wwing


if __name__ == '__main__':
	import constants as consts
	from Weight.weight_refined import *
	import matplotlib.pyplot as plt
	
	Sref_0 = consts.S_wing 
	AR_0 = consts.AR
	tc_0 = consts.tc
	taper_0 = consts.w_lambda
	sweep_0 = consts.sweep #quarterchord sweep angle
	
	constants = [consts.M, consts.N, consts.wing_mounted_area, consts.b, consts.c_root]
	# M = consts.M
	# N = consts.N
	# wing_mounted_area = consts.wing_mounted_area
	# b = consts.b
	# c_root = consts.c_root
	w_0, _ = prelim_weight(consts.Sref, consts.thrust_req, consts)


	#varying Sref
	Sref_range = np.linspace(100, 2000, 20)
	W_Sref = weight_calc(Sref_range, AR_0, tc_0, taper_0, sweep_0, constants)
	# print 'W_Sref complete'

	#varying AR
	AR_range = np.linspace(1.0, 15.0, 20)
	W_AR = weight_calc(Sref_0, AR_range, tc_0, taper_0, sweep_0, constants)
	# print 'W_AR complete'

	#varying tc
	tc_range = np.linspace(0.03, 0.25, 20)
	W_tc = weight_calc(Sref_0, AR_0, tc_range, taper_0, sweep_0, constants)
	# print 'W_tc complete'

	#varying taper
	taper_range = np.linspace(0.0, 1.0, 20)
	W_taper = weight_calc(Sref_0, AR_0, tc_0, taper_range, sweep_0, constants)
	# print 'W_taper complete'

	#varying sweep
	sweep_range = np.linspace(0.0, 45.0, 20)
	W_sweep = weight_calc(Sref_0, AR_0, tc_0, taper_0, np.deg2rad(sweep_range), constants)
	# print 'W_sweep complete'

	plt.plot(Sref_range, W_Sref)
	plt.show()
	plt.plot(AR_range, W_AR)
	plt.show()
	plt.plot(tc_range, W_tc)
	plt.show()
	plt.plot(taper_range, W_taper)
	plt.show()
	plt.plot(sweep_range, W_sweep)
	plt.show()