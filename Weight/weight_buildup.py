import os,sys,inspect

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import numpy as np 
import constants
import Weight.weight_estimation
import Sizing.horizontal_surf_sizing

def prelim_weight(Sref_wing, T0): #Sref in ft^2, T0 in lbs

	#Horizontal tail calculation
	c_MAC_wing, _ = Sizing.horizontal_surf_sizing.MAC(constants.c_root, constants.w_lambda, constants.b) #m
	#finds total required area
	S_total = Sizing.horizontal_surf_sizing.hor_Sref(constants.c_HT, c_MAC_wing, 0.092903*Sref_wing, constants.L_HT) #m^2
	#formula explanation: new tail area = (tail only area * distance to tail - distance to canard * area of canard)/distance to tail
	S_HT = (S_total*constants.L_HT - constants.Sref_c*constants.L_c)/constants.L_HT #m^2

	#weight calcuations (constants = lb/ft^2)
	w_wing = 2.5*Sref_wing
	w_HT = 2.0*S_HT*10.7639
	# w_VT = 2.0*S_VT*10.7639
	w_VT = 2.0*16.1519601701*10.7369 #needs to be replaced by previous line
	w_c = 2.0*constants.Sref_c*10.7639
	w_fuse = 1.4*constants.Swet_fuse

	# engine weight calculations (lbs)
	w_eng_dry = 0.521*(T0)**0.9
	w_eng_oil = 0.082*(T0)**0.65
	w_eng_rev = 0.034*(T0)
	w_eng_control = 0.26*(T0)**0.5
	w_eng_start = 9.33*(w_eng_dry/1000.0)**1.078
	w_eng = w_eng_dry + w_eng_oil + w_eng_rev + w_eng_control + w_eng_start

	#iterating for MTOW	
	w_0, _, _, w_crew_payload = Weight.weight_estimation.calcWeights(constants.R,constants.L_D, constants.SFC, M=constants.machCruise)
	tolerance = 0.1
	converged = 0

	while True:
	# for i in range(1000):
		fuel_fraction  = 0.41 #needs fuel fraction calculation
		w_f = fuel_fraction*w_0
		w_landing_gear = w_0*0.057 #lb
		w_nose_gear = w_landing_gear*0.15 #lb
		w_main_gear = 0.85*w_landing_gear/2.0 #lb
		w_xtra = 0.1*w_0 #lb
		w_0new = constants.numEngines*w_eng + w_wing + w_HT + w_c + w_VT + w_fuse + w_xtra + w_landing_gear + w_f + w_crew_payload

		#convergence check
		if abs(w_0new - w_0) <= tolerance:
			converged = 1
			break
		w_0 += 0.1*(w_0new - w_0)
		print w_0


	# print w_nose_gear, w_main_gear, w_engine, w_all_else

	# print w_wing+w_HT+w_VT+w_c+w_fuse+w_landing_gear+w_engine*2+w_all_else

	return w_0

if __name__ == '__main__':
	MTOW = prelim_weight(constants.Sref*10.7639, constants.engine_thrust)
