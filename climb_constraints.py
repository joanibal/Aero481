import numpy as np
from calcDragPolar import DragPolar
import constants

def TWcalc(CL_max, CD0, ks, K, G):
	TW = ks**2/CL_max*CD0 + CL_max/ks**2*K + G
	return TW

def TWcorrection(max_cont_thrust, OEI, landing, TW):

	#correction conditions
	if max_cont_thrust


	return TW_corrected

if __name__ == '__main__':
	#import C_d0 and K data
	C_d0_clean, C_d0_takeoff_flaps_gear_down, C_d0_takeoff_flaps_gear_up, C_d0_landing_flaps_gear_down, C_d0_landing_flaps_gear_up, k_clean, k_takeoff, k_landing = DragPolar()
	
	#calculating uncorrected climb
	TW_climb1 = TWcalc(2, C_d0_landing_flaps_gear_up, 1.2, k_landing, 0.012)
