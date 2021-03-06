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
		'Takeoff Climb': 0.012,
		'Trans. Seg. Climb': 0.00,
		'2nd Seg. Climb': 0.024,
		'Enroute Climb': 0.012,
		'Balked Climb AEO': 0.032,
		'Balked Climb OEI': 0.021
	}

	ks = {
		'Takeoff Climb': 1.2,
		'Trans. Seg. Climb': 1.15,
		'2nd Seg. Climb': 1.2,
		'Enroute Climb': 1.25,
		'Balked Climb AEO': 1.30,
		'Balked Climb OEI': 1.5
	}

	CD0_climb = {
		'Takeoff Climb': CD0['takeoff']['gear up'],
		'Trans. Seg. Climb': CD0['takeoff']['gear down'],
		'2nd Seg. Climb': CD0['takeoff']['gear up'],
		'Enroute Climb': CD0['cruise'],
		'Balked Climb AEO': CD0['landing']['gear down'],
		'Balked Climb OEI': (CD0['landing']['gear down'] + CD0['takeoff']['gear down'])/2,
	}

	k_climb = {
		'Takeoff Climb': k['takeoff'],
		'Trans. Seg. Climb': k['takeoff'],
		'2nd Seg. Climb': k['takeoff'],
		'Enroute Climb': k['cruise'],
		'Balked Climb AEO': k['landing'],
		# 'Balked Climb OEI': (k['landing'] + k['takeoff'])/2,
		'Balked Climb OEI':k['landing'],
	}

	CL_max_climb = {
		'Takeoff Climb': CL_max['takeoff'],
		'Trans. Seg. Climb': CL_max['takeoff'],
		'2nd Seg. Climb': CL_max['takeoff'],
		'Enroute Climb': CL_max['cruise'],
		'Balked Climb AEO': CL_max['landing'],
		'Balked Climb OEI':CL_max['balked landing'],
	}

	if numEngines == 3: #adjusts the G if 3 engines instead of two
		for keys in G.keys():
			G = G+0.003


	for flight_condition in G.keys():


		if flight_condition is 'Enroute Climb' or 'Balked Climb AEO' or 'Balked Climb OEI':
				thrust_coeff = 1/0.94
		else:
				thrust_coeff = 1

		if flight_condition is 'Balked Climb AEO':
    			eng_coeff = 1
		else:				# else - OEI false
			eng_coeff = numEngines/(numEngines -1.0)

		if flight_condition is 'Balked Climb AEO' or 'Balked Climb OEI':
			CTOL_coeff = 0.75 	#estimate (high estimate, from notes)
		else:				# else - landing false
			CTOL_coeff = 1


		T_W[flight_condition] = ks[flight_condition]**2/CL_max_climb[flight_condition]*CD0_climb[flight_condition]\
		   + CL_max_climb[flight_condition]/ks[flight_condition]**2*k_climb[flight_condition] + G[flight_condition]

		T_W[flight_condition] = 1/0.80 * thrust_coeff * eng_coeff * CTOL_coeff * T_W[flight_condition]


	return T_W

# ---------------------------- Cruise ---------------------------------------- #
def calcTWCruise(W_S, Cd_0, AR, e, q):
    return (q* Cd_0)/W_S + (W_S)*1/(q*np.pi*AR*e)

# ---------------------------- Ceiling --------------------------------------- #
def calcTWCeiling(densCeiling_to_densSL, Cd_0):
    return 1/(densCeiling_to_densSL )**0.6 *\
           ( 0.001 + 2*np.sqrt(Cd_0/(np.pi*9.8*0.85)))  

# ---------------------------- Takeoff --------------------------------------- #
def calcTWTakeoff(W_S, CL_max, runwayLength):
    return W_S/(1*CL_max* runwayLength/37.5)

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
	# import constants as plane
	import j481 as plane
	from Aerodynamics.calcCoeff import compentCDMethod
	from Weight.weight_refined import prelim_weight
	# from climb_constraints import calcTWClimb


	N = 50000
	W_S = np.linspace(10, 150, N)
	# w_0 = calcWeights((5000+200),15, 0.657)[0]	 # [0] <-- only use the first
	w_0, _ , plane = prelim_weight(plane.Sref , plane.thrust_req, plane)

	plane.CD0 = compentCDMethod(plane, plane.mach, plane.mu_cruise, plane.speed_fps, plane.density_cruise)

	T_W_takeoff = calcTWTakeoff(W_S, plane.CL['max']['takeoff'], plane.runway_length)
	T_W_cruise =  calcTWCruise(W_S,  plane.CD0['cruise'], plane.wing.aspect_ratio, plane.e['cruise'], plane.q_cruise)
	T_W_ceiling = np.ones(N)*calcTWCeiling(plane.density_ceiling/plane.density_SL, plane.CD0['cruise'])
	W_S_landing = calcWSLanding(plane.runway_length,plane.CL['max']['landing'])





	# ---------------------------------- Plotting ------------------------------- #


	ceiling, = plt.plot(W_S,T_W_ceiling , label='Ceiling')
	cruise, = plt.plot(W_S, T_W_cruise, label='Cruise')
	takeoff, = plt.plot(W_S, T_W_takeoff, label='Takeoff')
	landing, = plt.plot([W_S_landing]*2, [ 0, 1], label='Landing')


	T_W_climb = calcTWClimb(plane.CL['max'], plane.CD0,plane.k,plane.numEngines)

	lines = [ceiling, cruise, takeoff, landing]
	for key in T_W_climb.keys():

		lines.append(plt.plot(W_S, np.ones(np.shape(W_S))*T_W_climb[key],'--', label=key )[0])


	labels = [ x._label for x in lines]


	a = np.logical_and(T_W_cruise>=T_W_climb['Balked Climb OEI'], T_W_takeoff<=T_W_climb['Balked Climb OEI'])
	# b = np.logical_and(np.logical_not(a), W_S<=W_S_landing)
	b = np.logical_and(np.logical_not(a), T_W_takeoff< T_W_climb['Balked Climb OEI'])
	c = np.logical_and(T_W_takeoff>=T_W_climb['Balked Climb OEI'],  W_S<=W_S_landing)

	plt.fill_between(W_S,T_W_cruise,1,where=a     ,interpolate=True, color='b', alpha=0.5, edgecolor='none', linewidth=0.0)
	plt.fill_between(W_S,np.ones(np.shape(W_S))*T_W_climb['Balked Climb OEI'],1,where=b,interpolate=True, color='b', alpha=0.5, edgecolor='none', linewidth=0.0)
	plt.fill_between(W_S,T_W_takeoff,1,where=c,interpolate=True, color='b', alpha=0.5, edgecolor='none', linewidth=0.0)

	plt.axis((W_S[0], W_S[-1], 0, 0.5))


	plt.plot(63.7, 0.258, 'mo', label='PDR Design Point')
	design_point_str = str(63.7) + 'lb/ft^2, ' + str(0.26) 
	plt.annotate(design_point_str, xy=(63.7, 0.258), xytext=(63.7-29, 0.258+.01), weight = 'bold')

	plt.plot(w_0/plane.Sref, plane.thrust_req/w_0, 'ro', label='CDR Design Point')
	design_point_str = str(round(w_0/plane.Sref,1)) + 'lb/ft^2, ' + str(round(plane.thrust_req/w_0,2))
	plt.annotate(design_point_str, xy=(w_0/plane.Sref, plane.thrust_req/w_0), xytext=(w_0/plane.Sref-29, plane.thrust_req/w_0+.01), weight = 'bold')

	print w_0/plane.Sref, plane.thrust_req/w_0

	plt.legend(lines, labels)
	plt.legend(loc = 'upper right')

	plt.ylabel('T/W')
	plt.xlabel('W/S [$lb/ft^2$]')
	# plt.title('')
	plt.show()