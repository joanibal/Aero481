import os,sys,inspect

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import Sizing.horizontal_surf_sizing
from Aerodynamics.calcCoeff import *
import Sizing.Svt_calc
import Weight.weight_estimation
import numpy as np
import matplotlib.pyplot as plt

# def cruiseFuel(c, S, Cf, R, speed, CL_cruise):  # S must be in [m^2]
#     CD = Cf*(Swet_rest + 2.0*S)/S + CL_cruise/(np.pi*AR*e['cruise'])
#     cruiseFrac = np.exp(R*c*CD/(speed_kts*CL_cruise))
#     return cruiseFrac


def fuel_fraction(c, CD, R, speed, CL):
	ff1 = 0.99		#warmup
	ff2 = 0.995 	#taxi
	ff3 = 0.995	 	#TO
	ff4 = 0.98		#climb

	ff6 = 0.99 		#descent
	ff7 = 0.992		#landing
	
	cruiseFrac = np.exp(R*c*CD/(speed*CL))
	ff5 = 1/cruiseFrac
	ff = ff1*ff2*ff3*ff4*ff5*ff6*ff7
	# print cruiseFrac, ff5, ff, 1-ff
	return 1-ff




def prelim_weight(Sref_wing, T0, consts):
	'''
	#Sref in ft^2, T0 in lbs
	'''

	try:
		c_MAC_wing, _ = Sizing.horizontal_surf_sizing.MAC(consts.c_root, consts.w_lambda, consts.b) #m
		#finds total required area
		S_total = Sizing.horizontal_surf_sizing.hor_Sref(consts.c_HT, c_MAC_wing, 0.092903*Sref_wing, consts.L_HT) #m^2
		
		#formula explanation: new tail area = (tail only area * distance to tail - distance to canard * area of canard)/distance to tail
		S_HT = (S_total*consts.L_HT - consts.Sref_c*consts.L_c)/consts.L_HT #m^2
		S_VT = Sizing.Svt_calc.calcS_VT(consts.L_VT, consts.c_VT, consts.b, Sref_wing/10.7639)
		w_c = 4.0*consts.Sref_c_actual*10.7639
		# print w_c

	except:
		S_HT = consts.S_HT
		S_VT = consts.S_VT
		w_c = 0



	# w_wing = 7.5*Sref_wing
	# w_HT = 4.0*S_HT*10.7639
	# w_VT = 4.0*S_VT*10.7639
	# # w_VT = 2.0*16.1519601701*10.7369 #needs to be replaced by previous line


	# w_fuse = 3.5*consts.Swet_fuse



	w_wing = 6.5*Sref_wing
	w_HT = 3.5*S_HT*10.7639
	w_VT = 3.5*S_VT*10.7639
	# w_VT = 2.0*16.1519601701*10.7369 #needs to be replaced by previous line
	# print 'wing', w_wing
	# print 'ht', w_HT
	# print 'vt', w_VT
	# print 'canard', w_c

	w_fuse = 2.5*consts.Swet_fuse
	# print 'fuse', w_fuse


	# # engine weight calculations (lbs)
	w_eng_dry = 0.521*(T0)**0.9
	w_eng_oil = 0.082*(T0)**0.65
	w_eng_rev = 0.034*(T0)	
	w_eng_control = 0.26*(T0)**0.5
	w_eng_start = 9.33*(w_eng_dry/1000.0)**1.078
	w_eng = w_eng_dry + w_eng_oil + w_eng_rev + w_eng_control + w_eng_start


	#iterating for MTOW	
	w_0, _, _, w_crew_payload = Weight.weight_estimation.calcWeights(consts.R,consts.L_D, consts.SFC, consts.machCruise, consts.w_payload)


	tolerance = 1.0
	converged = 0


	while True:
	# for i in range(1000):
		# CL = calcCL(w_0/Sref_wing)

		CD0 = consts.C_f*(consts.Swet_rest + 2.0*Sref_wing)/Sref_wing
		
		CL = np.sqrt(CD0*np.pi*consts.AR*consts.e['cruise'])
		CD = CD0 + CL**2/(np.pi*consts.AR*consts.e['cruise'])

		ff = fuel_fraction(consts.SFC, CD, consts.R, consts.speed_kts, CL)
		w_f = ff*w_0
		w_landing_gear = w_0*0.043 #lb
		w_nose_gear = w_landing_gear*0.15 #lb
		w_main_gear = 0.85*w_landing_gear/2.0 #lb
		w_xtra = 0.17*w_0 #lb
		w_0new = consts.numEngines*w_eng + w_wing + w_HT + w_c + w_VT + w_fuse + w_xtra + w_landing_gear + w_f + w_crew_payload

		#convergence check
		if abs(w_0new - w_0) <= tolerance:
			converged = 1
			break	
		w_0 += 0.1*(w_0new - w_0)
		# print w_0
	
	# print('CL ', CL, 'CD0', CD0, ' w_0/Sref_wing ',  w_0/Sref_wing)
	# print w_nose_gear, 2*w_main_gear, w_xtra
	# print w_fuse+w_xtra
	return w_0, w_f

if __name__ == '__main__':

	import numpy as np 
	import constants 
	import constantsG550

	# CD = calcCD(consts.C_f, consts.Swet_rest*10.7639 + 2.0*consts.Sref, consts.Sref,  consts.CL['cruise'], consts.e['cruise'], consts.AR )
	# ff = fuel_fraction(consts.SFC, CD, consts.R, consts.speed_kts, consts.CL['cruise'])
	# print ff

	w_0, w_f = prelim_weight(constants.Sref, constants.thrust_req, constants)

	print 'w_0',w_0 , 'w_f', w_f

	w_0, w_f = prelim_weight(constantsG550.Sref*10.7639, constantsG550.thrust_req, constantsG550)

	print 'w_0',w_0 , 'w_f', w_f


	
	