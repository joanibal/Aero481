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
		eng_coeff = constants.numEngines/(constants.numEngines -1)
	else:				# else - OEI false
		eng_coeff = 1		

	#modifier for landing
	if landing == 1: 	# 1 - true
		CTOL_coeff = 0.65 	#estimate (high estimate, from notes)
	else:				# else - landing false
		CTOL_coeff = 1
	
	#adjusted T/W
	TW_corrected = 1/0.80 * thrust_coeff * eng_coeff * CTOL_coeff * TW

	return TW_corrected

if __name__ == '__main__':
	#import C_d0 and K data
	C_d0_clean, C_d0_takeoff_flaps_gear_down, C_d0_takeoff_flaps_gear_up, C_d0_landing_flaps_gear_down, C_d0_landing_flaps_gear_up, k_clean, k_takeoff, k_landing = DragPolar()
	
	#sorting data into arrays for each stage
	#order of climbs: TO, transition seg, 2nd seg, enroute, balked landing, balked landing (OEI)
	#used in calculating T/W (uncorrected)
	CL_max_array = np.array([1.8, 1.8, 1.8, 1.2, 2.0, 2.0*0.85]) #based on Roskam
	C_d0_array = np.array([C_d0_takeoff_flaps_gear_up, C_d0_takeoff_flaps_gear_down, C_d0_takeoff_flaps_gear_up, C_d0_clean, C_d0_landing_flaps_gear_down, (C_d0_landing_flaps_gear_down+C_d0_takeoff_flaps_gear_down)/2])
	ks_array = np.array([1.2, 1.15, 1.2, 1.25, 1.3, 1.5])
	K_array = np.array([k_takeoff, k_takeoff, k_takeoff, k_clean, k_landing, k_landing])
	G_array = np.array([0.012, 0.00, 0.024, 0.012, 0.032, 0.021])

	#used in calculating T/W (corrected), 0-1 indicate condition active or not
	thrust_mod_array = np.array([0, 0, 0, 1, 1, 1])
	eng_mod_array = np.array([1, 1, 1, 1, 0, 1])
	CTOL_mod_array = np.array([0, 0, 0, 0, 1, 1])

	#preallocation
	TW_array = np.array([])
	TW_corrected_array = np.array([])

	#calculating uncorrected climb
	for i in range(0,6):
		TW = TWcalc(CL_max_array[i], C_d0_array[i], ks_array[i], K_array[i], G_array[i])
		# print TW
		TW_corrected = TWcorrection(thrust_mod_array[i], eng_mod_array[i], CTOL_mod_array[i], TW)
		# print TW_corrected
		# print TW, TW_corrected

		TW_array = np.append(TW_array,TW)
		TW_corrected_array = np.append(TW_corrected_array, TW_corrected)

	# print TW_array
	print TW_corrected_array
	# print C_d0_array