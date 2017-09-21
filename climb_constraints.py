import numpy as np
from calcDragPolar import DragPolar
import constants
from weight_estimation import calcWeights

def TWcalc(CL_max, CD0, ks, K, G):
	TW = ks**2/CL_max*CD0 + CL_max/ks**2*K + G
	return TW

def TWcorrection(max_cont_thrust, OEI, landing, TW):

	#correction conditions
	#modifier for max continuous thrust
	if max_cont_thrust == 1:	# 1 - true
		thrust_coeff = 1/0.94
	else:						#else - max cont. thrust false
		thrust_coeff = 1

	#modifier for OEI
	if OEI == 1: 		# 1 - true
		eng_coeff = constants.numEngines/(1 - constants.numEngines)
	else:				# else - OEI false
		eng_coeff = 1		

	#modifier for landing
	if landing == 1: 	# 1 - true
		CTOL_coeff = 1
	else:				# else - landing false
		CTOL_coeff = 1
	
	#adjusted T/W
	TW_corrected = 1/0.80 * thrust_coeff * eng_coeff * CTOL_coeff * TW

	return TW_corrected

if __name__ == '__main__':
	#import C_d0 and K data
	C_d0_clean, C_d0_takeoff_flaps_gear_down, C_d0_takeoff_flaps_gear_up, C_d0_landing_flaps_gear_down, C_d0_landing_flaps_gear_up, k_clean, k_takeoff, k_landing = DragPolar()
	
	#calculating uncorrected climb
	TW_climb1 = TWcalc(2, C_d0_landing_flaps_gear_up, 1.2, k_landing, 0.012)
