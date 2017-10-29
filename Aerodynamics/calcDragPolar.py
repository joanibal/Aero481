#Drag Polar Calculation
import os,sys,inspect

sys.path.insert(1, os.path.join(sys.path[0], '..'))
import math
import numpy as np
import matplotlib.pyplot as plt
from Weight.weight_estimation import calcWeights

def DragPolar(w_0, plot=False):

	#Define regression constants for wetted area
	c = 0.0199
	d = 0.7531

	Swet = 10**c*w_0**d 				#Calculate wetted area
	C_f = 0.0045						#Skin-friction coefficient based on equivalent skin-friction coefficients
	f = C_f*Swet 						#Calculate equivalent parasite area
	Sref = 1055.17						#Estimated aircraft Sref
	Cd0 = f/Sref 						#Calculate parasite drag coefficient
	AR = 9								#Estimated aspect ratio

	#Define drag polar variation constants
	delC_d0_clean = 0
	delC_d0_tof = 0.015
	delC_d0_lf = 0.06
	delC_d0_lg = 0.020

	e = {
		'takeoff':0.825,
		'clean':0.775,
		'landing':0.725
	}


	Cd_0 = {
		'takeoff':{'gear up':Cd0 + delC_d0_tof,
				   'gear down': Cd0 + delC_d0_lg + delC_d0_tof},
		'clean':Cd0 + delC_d0_clean,
		'landing':{'gear up': Cd0 + delC_d0_lf,
				   'gear down': Cd0 + delC_d0_lf + delC_d0_lg}
	}
	
	k = {}
	for key in e.keys():
		k[key] = 1/(np.pi*AR*e[key])
		


	#Print CD per flight mode
	# print("Clean: CD = " + str(C_d0['clean']) + " + " + str(k['clean']) + " * CL^2")
	# print("Takeoff flaps, gear up: CD = " + str(C_d0['takeoff']['gear up']) + " + " + str(k['takeoff']) + " * CL^2")
	# print("Takeoff flaps, gear down: CD = " + str(C_d0['takeoff']['gear down']) + " + " + str(k['takeoff']) + " * CL^2")
	# print("Landing flaps, gear up: CD = " + str(C_d0['landing']['gear up']) + " + " + str(k['landing']) + " * CL^2")
	# print("Landing flaps, gear down: CD = " + str(C_d0['landing']['gear down']) + " + " + str(k['landing']) + " * CL^2")

	# #Display the graph
	# plt.clf(CD_landing_flaps_gear_up)
	# plt.cla()
	# plt.close()

	if plot:
		#Need to update with appropriate CL limits
		import constants as consts

		CL_range_clean = np.linspace(-0.8, consts.CL['max']['cruise'], 100)
		CL_range_landing = np.linspace(0.2, consts.CL['max']['landing'], 100)
		CL_range_takeoff = np.linspace(-0.1, consts.CL['max']['takeoff'], 100)


		CD_clean = Cd_0['clean'] + k['clean']*CL_range_clean**2
		CD_takeoff_flaps_gear_down = Cd_0['takeoff']['gear down'] + k['takeoff']*CL_range_takeoff**2
		CD_takeoff_flaps_gear_up = Cd_0['takeoff']['gear up'] + k['takeoff']*CL_range_takeoff**2
		CD_landing_flaps_gear_down = Cd_0['landing']['gear down'] + k['landing']*CL_range_landing**2
		CD_landing_flaps_gear_up = Cd_0['landing']['gear up'] + k['landing']*CL_range_landing**2

		cruise, = plt.plot(CD_clean, CL_range_clean, linewidth=2, label='Cruise', color='forestgreen')
		takegearup, = plt.plot(CD_takeoff_flaps_gear_up, CL_range_takeoff, linewidth=2, label='Takeoff Gear Up', color='orangered')
		takegeardownd, = plt.plot(CD_takeoff_flaps_gear_down, CL_range_takeoff, linewidth=2, label='Takeoff Gear Down', color='darkred')
		landgearup, = plt.plot(CD_landing_flaps_gear_down, CL_range_landing,  linewidth=2, label='Landing Gear Up', color='skyblue')
		landgeardown, = plt.plot(CD_landing_flaps_gear_up, CL_range_landing, linewidth=2, label='Landing Gear Down', color='darkblue')
		plt.ylabel('CL', weight='bold',size='x-large')
		plt.xlabel('CD', weight='bold',size='x-large')


		lines = [cruise,	takegearup,	takegeardownd,	landgearup,	landgeardown]
		labels = [ x._label for x in lines]
	
		plt.legend(lines, labels)
		plt.legend(loc = 'lower right')



		plt.show()





	'''CL_range = np.array(-1.5, 1.5, 100)
	CD_clean = Cd_0_clean + k_clean*CL_range**2'''


	#return
	return Cd_0, k, e

if __name__ == '__main__':
	#Define w_0
	w_0 = calcWeights((5000+200),15, 0.657, M=0.85)[0]	 # [0] <-- only use the first 
	Cd_0, k = DragPolar(w_0, plot=True)[0:2] # [0:2] <-- only use the first two ouputs 
	print Cd_0

	# test for array inputs
	# w_0 = np.array([calcWeights((5000+200),15, 0.657, M=0.85)[0], calcWeights((5000+100),15, 0.657, M=0.85)[0]])	 # [0] <-- only use the first 
	# Cd_0, k = DragPolar(w_0, plot=False)[0:2] # [0:2] <-- only use the first two ouputs 
	# print Cd_0