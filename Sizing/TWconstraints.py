import numpy as np

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
		   + CL_max_climb[flight_condition]/ks[flight_condition]**2*k_climb[flight_condition] + G[flight_condition]

		T_W[flight_condition] = 1/0.80 * thrust_coeff * eng_coeff * CTOL_coeff * T_W[flight_condition]


	return T_W

# ---------------------------- Cruise ---------------------------------------- #
def calcTWCruise(W_S, Cd_0, AR, e, q):
    return (q* CD_0)/W_S + (W_S)*1/(q*np.pi*AR*e)

# ---------------------------- Ceiling --------------------------------------- #
def calcTWCeiling(densCeiling_to_densSL, Cd_0):
    return 1/(densCeiling_to_densSL )**0.6 *\
           ( 0.001 + 2*np.sqrt(Cd_0/(np.pi*9.8*0.85)))  

# ---------------------------- Takeoff --------------------------------------- #
def calcTWTakeoff(W_S, CL_max):
    return W_S/(1*CL_max* 4948/37.5)

# ---------------------------- Landing --------------------------------------- #
def calcWSLanding(runLength, CL_max):
    return (runLength/1.67 - 1000)*CL_max*1/80.0 



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


	N = 1000
	W_S = np.linspace(0, 350, N)
	w_0 = calcWeights((5000+200),15, 0.657)[0]	 # [0] <-- only use the first 
	Cd_0, k = DragPolar(w_0)[0:2] # [0:2] <-- only use the first two ouputs 

	T_W_takeoff = calcTWTakeoff(W_S, consts.CL['max']['takeoff'])
	T_W_cruise =  calcTWCruise(W_S)
	T_W_ceiling = np.ones(N)*calcTWCeiling(consts.Density_Ceiling/consts.Density_SL, Cd_0['clean'])
	T_W_landing = calcWSLanding(consts.runLength,consts.CL['max']['landing'])





	# ---------------------------------- Plotting ------------------------------- #


	ceiling, = plt.plot(W_S,T_W_ceiling , label='Ceiling')
	cruise, = plt.plot(W_S, T_W_cruise, label='Cruise')
	takeoff, = plt.plot(W_S, T_W_takeoff, label='Takeoff')
	landing, = plt.plot([T_W_landing]*2, [ 0, 1], label='Landing')


	T_W_climb = calcTWClimb(consts.CL['max'], Cd_0,k,consts.numEngines)

	lines = [ceiling, cruise, takeoff, landing]
	for key in T_W_climb.keys():
			
		lines.append(plt.plot(W_S, np.ones(np.shape(W_S))*T_W_climb[key],'--', label=key )[0])


	labels = [ x._label for x in lines]


	a = np.logical_and(T_W_cruise>=T_W_climb['balked climb OEI'], T_W_takeoff<=T_W_climb['balked climb OEI'])
	b = np.logical_and(np.logical_not(a), T_W_takeoff<=T_W_climb['balked climb OEI'])
	c = np.logical_and(T_W_takeoff>=T_W_climb['balked climb OEI'], W_S<=T_W_landing)

	plt.fill_between(W_S,T_W_cruise,1,where=a     ,interpolate=True, color='b')
	plt.fill_between(W_S,np.ones(np.shape(W_S))*T_W_climb['balked climb OEI'],1,where=b,interpolate=True, color='b')
	plt.fill_between(W_S,T_W_takeoff,1,where=c,interpolate=True, color='b')

	plt.axis((W_S[0], W_S[-1], 0, 0.5))	

	plt.legend(lines, labels)
	plt.legend(loc = 'upper right')

	plt.ylabel('T/W')
	plt.xlabel('W/S')
	# plt.title('')
	plt.show()
