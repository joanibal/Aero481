#Drag Polar Calculation

import math
import numpy
import matplotlib.pyplot as plt
from weight_estimation import calcWeights

def DragPolar():
	#Define w_0
	w_0, w_empty, w_fuel, w_payload = calcWeights((5000+200),15, 0.657, M=0.85)	

	#Define regression constants for wetted area
	c = 0.0199
	d = 0.7531

	Swet = 10**c*w_0**d 				#Calculate wetted area
	C_f = 0.0045						#Skin-friction coefficient based on equivalent skin-friction coefficients
	f = C_f*Swet 						#Calculate equivalent parasite area
	Sref = 1055.17						#Estimated aircraft Sref
	C_d0 = f/Sref 						#Calculate parasite drag coefficient
	AR = 9								#Estimated aspect ratio

	#Define drag polar variation constants
	delC_d0_clean = 0
	delC_d0_tof = 0.015
	delC_d0_lf = 0.06
	delC_d0_lg = 0.020
	e_clean = 0.825
	e_tof = 0.775
	e_lf = 0.725
	e_lg = 1

	#Calculate parasite drag coefficients
	C_d0_clean = C_d0 + delC_d0_clean
	C_d0_takeoff_flaps_gear_up = C_d0 + delC_d0_tof
	C_d0_takeoff_flaps_gear_down = C_d0 + delC_d0_lg + delC_d0_tof
	C_d0_landing_flaps_gear_up = C_d0 + delC_d0_lf
	C_d0_landing_flaps_gear_down = C_d0 + delC_d0_lf + delC_d0_lg

	#Calculate k per flight mode
	k_clean = 1/(math.pi*AR*e_clean)
	k_takeoff = 1/(math.pi*AR*e_tof)
	k_landing = 1/(math.pi*AR*e_lf)

	#Print CD per flight mode
	# print("Clean: CD = " + str(C_d0_clean) + " + " + str(k_clean) + " * CL^2")
	# print("Takeoff flaps, gear up: CD = " + str(C_d0_takeoff_flaps_gear_up) + " + " + str(k_takeoff) + " * CL^2")
	# print("Takeoff flaps, gear down: CD = " + str(C_d0_takeoff_flaps_gear_down) + " + " + str(k_takeoff) + " * CL^2")
	# print("Landing flaps, gear up: CD = " + str(C_d0_landing_flaps_gear_up) + " + " + str(k_landing) + " * CL^2")
	# print("Landing flaps, gear down: CD = " + str(C_d0_landing_flaps_gear_down) + " + " + str(k_landing) + " * CL^2")

	# #Display the graph
	# plt.clf()
	# plt.cla()
	# plt.close()

	#Need to update with appropriate CL limits
	CL_range = numpy.linspace(-1.5, 1.5, 100)
	CD_clean = C_d0_clean + k_clean*CL_range**2
	CD_takeoff_flaps_gear_down = C_d0_takeoff_flaps_gear_down + k_takeoff*CL_range**2
	CD_takeoff_flaps_gear_up = C_d0_takeoff_flaps_gear_up + k_takeoff*CL_range**2
	CD_landing_flaps_gear_down = C_d0_landing_flaps_gear_down + k_landing*CL_range**2
	CD_landing_flaps_gear_up = C_d0_landing_flaps_gear_up + k_landing*CL_range**2

	# plt.plot(CD_clean, CL_range)
	# plt.plot(CD_takeoff_flaps_gear_down, CL_range)
	# plt.plot(CD_takeoff_flaps_gear_up, CL_range)
	# plt.plot(CD_landing_flaps_gear_up, CL_range)
	# plt.plot(CD_landing_flaps_gear_down, CL_range)
	# plt.ylabel('CL')
	# plt.xlabel('CD')
	# plt.show()


	'''CL_range = numpy.array(-1.5, 1.5, 100)
	CD_clean = C_d0_clean + k_clean*CL_range**2'''

	#return
	return C_d0_clean, C_d0_takeoff_flaps_gear_down, C_d0_takeoff_flaps_gear_up, C_d0_landing_flaps_gear_down, C_d0_landing_flaps_gear_up, k_clean, k_takeoff, k_landing

if __name__ == '__main__':

	C_d0_clean, C_d0_takeoff_flaps_gear_down, C_d0_takeoff_flaps_gear_up, C_d0_landing_flaps_gear_down, C_d0_landing_flaps_gear_up, k_clean, k_takeoff, k_landing = DragPolar()