import os,sys,inspect

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import Sizing.horizontal_surf_sizing
import Sizing.Svt_calc
import Weight.weight_estimation
import constants as consts
import numpy as np
# def cruiseFuel(c, S, Cf, R, speed, CL_cruise):  # S must be in [m^2]
#     CD = Cf*(Swet_rest + 2.0*S)/S + CL_cruise/(np.pi*AR*e['cruise'])
#     cruiseFrac = np.exp(R*c*CD/(speed_kts*CL_cruise))
#     return cruiseFrac

def calcCD(Cf, Swet, Sref, CL, e, AR):
	CD = Cf*Swet/Sref + CL**2/(np.pi*AR*e)
	return CD

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




def prelim_weight(Sref_wing, T0):
	'''
	#Sref in ft^2, T0 in lbs
	'''

	#Horizontal tail calculation
	c_MAC_wing, _ = Sizing.horizontal_surf_sizing.MAC(consts.c_root, consts.w_lambda, consts.b) #m
	#finds total required area
	S_total = Sizing.horizontal_surf_sizing.hor_Sref(consts.c_HT, c_MAC_wing, 0.092903*Sref_wing, consts.L_HT) #m^2
	
	#formula explanation: new tail area = (tail only area * distance to tail - distance to canard * area of canard)/distance to tail
	S_HT = (S_total*consts.L_HT - consts.Sref_c*consts.L_c)/consts.L_HT #m^2

	#weight calcuations (consts = lb/ft^2)
	w_wing = 10.0*Sref_wing
	w_HT = 5.5*244.87
	w_VT = 5.5*140.16
	w_fuse = 5.0*consts.Swet_fuse

	# engine weight calculations (lbs)
	w_eng_dry = 0.521*(T0)**0.9
	w_eng_oil = 0.082*(T0)**0.65
	w_eng_rev = 0.034*(T0)	
	w_eng_control = 0.26*(T0)**0.5
	w_eng_start = 9.33*(w_eng_dry/1000.0)**1.078
	w_eng = w_eng_dry + w_eng_oil + w_eng_rev + w_eng_control + w_eng_start

	#iterating for MTOW	
	w_0, _, _, w_crew_payload = Weight.weight_estimation.calcWeights(6750,17, consts.SFC)
	tolerance = 0.1
	converged = 0
	print w_0

	while True:
	# for i in range(1000):
		CD = calcCD(consts.C_f, consts.Swet_rest*10.7639 + 2.0*Sref_wing, Sref_wing,  consts.CL['cruise'], consts.e['cruise'], consts.AR )
		ff = fuel_fraction(consts.SFC, CD, consts.R, consts.speed_kts, consts.CL['cruise'])
		w_f = ff*w_0
		w_landing_gear = w_0*0.043 #lb
		w_nose_gear = w_landing_gear*0.15 #lb
		w_main_gear = 0.85*w_landing_gear/2.0 #lb
		w_xtra = 0.17*w_0 #lb
		w_0new = consts.numEngines*w_eng + w_wing + w_HT + w_VT + w_fuse + w_xtra + w_landing_gear + w_f + w_crew_payload

		#convergence check
		if abs(w_0new - w_0) <= tolerance:
			converged = 1
			break	
		w_0 += 0.1*(w_0new - w_0)
		# print w_0

	return w_0, w_f

if __name__ == '__main__':

	import numpy as np 
	import constants as consts

	# CD = calcCD(consts.C_f, consts.Swet_rest*10.7639 + 2.0*consts.Sref, consts.Sref,  consts.CL['cruise'], consts.e['cruise'], consts.AR )
	# ff = fuel_fraction(consts.SFC, CD, consts.R, consts.speed_kts, consts.CL['cruise'])
	# print ff

	MTOW, w_f= prelim_weight(1137.00, 2.0*consts.engine_thrust)
	print MTOW, w_f
	