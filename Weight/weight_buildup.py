import os,sys,inspect

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import numpy as np 
import constants
import Weight.weight_estimation
import horizontal_surf_sizing.hor_Sref
import horizontal_surf_sizing.MAC


def prelim_weight(Sref_wing, T0):

	#Horizontal tail calculation
	c_MAC_wing, _ = MAC(constants.c_root, constants.w_lambda, constants.b) #m
	#finds total required area
	S_total = hor_Sref(constants.c_HT, c_MAC_wing, Sref_wing, constants.L_HT) #m^2
	#formula explanation: new tail area = (tail only area * distance to tail - distance to canard * area of canard)/distance to tail
	S_HT = (S_total*constants.L_HT - constants.Sref_c*constants.L_c)/constants.L_HT #m^2

	#weight calcuations
	w_wing = 2.5*Sref_wing
	w_HT = 2.0*S_HT
	w_VT = 2.0*S_VT
	w_c = 2.0*constants.Sref_c
	w_fuse = 1.4*Swet_fuse

	# print w_wing, w_HT, w_VT, w_c, w_fuse
		
	w_0, _, _, _ = Weight.weight_estimation.calcWeights(constants.R,constants.L_D, constants.SFC, M=constants.machCruise)

	# w_0 = 94965.0 #lb
	w_landing_gear = w_0*0.057 #lb
	w_nose_gear = w_landing_gear*0.15 #lb
	w_main_gear = 0.85*w_landing_gear/2.0 #lb
	w_engine = 16096.3201*1.4 #lb
	w_all_else = 0.1*w_0 #lb

	# engine weight calculations

	# print w_nose_gear, w_main_gear, w_engine, w_all_else

	# print w_wing+w_HT+w_VT+w_c+w_fuse+w_landing_gear+w_engine*2+w_all_else

	return MTOW

if __name__ == '__main__':
