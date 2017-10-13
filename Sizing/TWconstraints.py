# ----------------------------- Climb ---------------------------------------- #
def calcTWClimb(CL_max, CD0, k, numEngines):
	'''
	CL_max: dict
		CL max for the relevant flight conditions
	CD0_max: dict
		CD0 for the relevant flight conditions
	k: dict
		k for the relevant flight conditions
	numEngines: int
		number of engines on the plane
	'''

	T_W = {}

	G = {
		'takeoff climb': 0.012,
		'trans seg climb': 0.00,
		'2nd seg climb': 0.024,
		'enroute climb': 0.012,
		'balked climb AEO': 0.032,
		'balked climb OEI': 0.021
	}

	ks = {
		'takeoff climb': 1.2,
		'trans seg climb': 1.15,
		'2nd seg climb': 1.2,
		'enroute climb': 1.25,
		'balked climb AEO': 1.30,
		'balked climb OEI': 1.5
	}

	CD0_climb = {
		'takeoff climb': CD0['takeoff']['gear up'],
		'trans seg climb': CD0['takeoff']['gear down'],
		'2nd seg climb': CD0['takeoff']['gear up'],
		'enroute climb': CD0['clean'],
		'balked climb AEO': CD0['landing']['gear down'],
		'balked climb OEI': (CD0['landing']['gear down'] + CD0['takeoff']['gear down'])/2,
	}

	k_climb = {
		'takeoff climb': k['takeoff'],
		'trans seg climb': k['takeoff'],
		'2nd seg climb': k['takeoff'],
		'enroute climb': k['clean'],
		'balked climb AEO': k['landing'],
		# 'balked climb OEI': (k['landing'] + k['takeoff'])/2,
		'balked climb OEI':k['landing'],		
	}

	CL_max_climb = {
		'takeoff climb': CL_max['takeoff'],
		'trans seg climb': CL_max['takeoff'],
		'2nd seg climb': CL_max['takeoff'],
		'enroute climb': CL_max['cruise'],
		'balked climb AEO': CL_max['landing'],
		'balked climb OEI':CL_max['balked landing'],	
	}

	if numEngines == 3: #adjusts the G if 3 engines instead of two
		for keys in G.keys():
			G = G+0.003

	
	for flight_condition in G.keys():
    		

		if flight_condition is 'enroute climb' or 'balked climb AEO' or 'balked climb OEI':
				thrust_coeff = 1/0.94
		else:
				thrust_coeff = 1

		if flight_condition is 'balked climb AEO':
    			eng_coeff = 1
		else:				# else - OEI false
			eng_coeff = numEngines/(numEngines -1.0)
		
		if flight_condition is 'balked climb AEO' or 'balked climb OEI':
			CTOL_coeff = 0.65 	#estimate (high estimate, from notes)
		else:				# else - landing false
			CTOL_coeff = 1
			

		T_W[flight_condition] = ks[flight_condition]**2/CL_max_climb[flight_condition]*CD0_climb[flight_condition]\
		   + CL_max[flight_condition]/ks[flight_condition]**2*K + G

		T_W[flight_condition] = 1/0.80 * thrust_coeff * eng_coeff * CTOL_coeff * T_W[flight_condition]


	return T_W

# ---------------------------- Cruise ---------------------------------------- #
def calcTWCruise(W_S):
    return 1.0/(0.2826**0.6)*(228.8*0.01597)/W_S + (W_S)*1/(228.8*np.pi)

# ---------------------------- Ceiling --------------------------------------- #
def calcTWCeilng(desCeilng_to_densSL, Cd_0):
    return 1/(desCeilng_to_densSL )**0.6 *\
           ( 0.001 + 2*np.sqrt(Cd_0/(np.pi*9.8*0.85)))  

# ---------------------------- Takeoff --------------------------------------- #
def calcTWTakeoff(CL_max):
    return W_S/(1*CL_max* 4948/37.5)

# ---------------------------- Landing --------------------------------------- #
def calcWSLanding(runLength, Cl_max):
    return (runLength/1.6 - 00)*CL_max*1/80.0 



if __name__ == '__main__':
	# ======================== Standard Packages ============================= #
	import os,sys,inspect

	sys.path.insert(1, os.path.join(sys.path[0], '..'))
	import numpy as np
	import matplotlib.pyplot as plt
	# ========================== 481  Packages ===============+=============== #
	import constants as consts

	from Aerodynamics.calcDragPolar import DragPolar
	from Weight.weight_estimation import calcWeights
	# from climb_constraints import calcTWClimb


	N = 10000
	W_S = np.linspace(0, 350, N)
	w_0 = calcWeights((5000+200),15, 0.657)[0]	 # [0] <-- only use the first 
	Cd_0, k = DragPolar(w_0)[0:2] # [0:2] <-- only use the first two ouputs 


	ceiling, = plt.plot(W_S, np.ones(N)*calcTWCeilng(consts.Density_Ceilng/consts.Density_SL, Cd_0['clean']), label='Ceiling')
	cruise, = plt.plot(W_S, calcTWCruise(W_S), label='Cruise')
	takeoff, = plt.plot(W_S, calcTWTakeoff(consts.CL_max['takeoff']), label='Takeoff')
	landing, = plt.plot([calcWSLanding(consts.runLength,consts.Cl_max['landing'])]*2, [ 0, 1], label='Landing')

	quit()

	T_W_climb = calcTWClimb(consts.CL_max, CD0,k,consts.numEngines)


	for key in T_W_climb.keys():
			
		A.append(plt.plot(W_S, np.ones(np.shape(W_S))*TW_corrected_array[i],'--', label=('Climb '+str(i+1))))

	lines = []
	labels = [ x._label for x in lines]
	a = np.logical_and(T_W_cruise>=TW_corrected_array[5], T_W_Takeoff<=TW_corrected_array[5])
	b = np.logical_and(np.logical_not(a), T_W_Takeoff<=TW_corrected_array[5])
	c = np.logical_and(T_W_Takeoff>=TW_corrected_array[5], W_S<=W_S_landing)

	plt.fill_between(W_S,T_W_cruise,1,where=a     ,interpolate=True, color='b')
	plt.fill_between(W_S,np.ones(np.shape(W_S))*TW_corrected_array[5],1,where=b,interpolate=True, color='b')
	plt.fill_between(W_S,T_W_Takeoff,1,where=c,interpolate=True, color='b')

	plt.axis((W_S[0], W_S[-1], 0, 1))	

	plt.legend(handles=[ceiling, cruise, takeoff, landing, A[0][0], A[1][0], A[2][0], A[3][0], A[4][0], A[5][0]])
	plt.legend(loc = 'upper right')

	plt.ylabel('T/W')
	plt.xlabel('W/S')
	# plt.title('')
	plt.show()
