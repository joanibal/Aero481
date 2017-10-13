# from Weight.weight_estimation import calcWeights
# from Aerodynamics.calcDragPolar import DragPolar





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

# def TWcorrection(TW):
    	
# 	TW
# 	#used in calculating T/W (corrected), 0-1 indicate condition active or not

# 	# C_d0_array = np.array([C_d0_takeoff_flaps_gear_up, C_d0_takeoff_flaps_gear_down, C_d0_takeoff_flaps_gear_up, C_d0_clean, C_d0_landing_flaps_gear_down, (C_d0_landing_flaps_gear_down+C_d0_takeoff_flaps_gear_down)/2])

# 	max_cont_thrust = np.array([0, 0, 0, 1, 1, 1])
# 	OEI = np.array([1, 1, 1, 1, 0, 1])
# 	landing = np.array([0, 0, 0, 0, 1, 1])

# 	TW['']
# 	thrust_coeff = np.array([1, 1, 1,  1/0.94, 1/0.94, 1/0.94])
# 	OEI = np.array([1 , 1, 1, 1, 1/(constants.numEngines/(constants.numEngines -1)) , 1])*constants.numEngines/(constants.numEngines -1)
# 	#correction conditions
# 	#modifier for max continuous thrust
# 	if max_cont_thrust == 1:	# 1 - true
# 		thrust_coeff = 1/0.94
# 	else:						#else - max cont. thrust false
# 		thrust_coeff = 1

# 	#modifier for OEI
# 	if OEI == 1: 		# 1 - true
# 		eng_coeff = constants.numEngines/(constants.numEngines -1)
# 	else:				# else - OEI false
# 		eng_coeff = 1		

# 	#modifier for landing
# 	if landing == 1: 	# 1 - true
# 		CTOL_coeff = 0.65 	#estimate (high estimate, from notes)
# 	else:				# else - landing false
# 		CTOL_coeff = 1

# 	#adjusted T/W
# 	TW_corrected = 1/0.80 * thrust_coeff * eng_coeff * CTOL_coeff * TW

# 	return TW_corrected

# if __name__ == '__main__':
# 	#import C_d0 and K data
# 	C_d0_clean, C_d0_takeoff_flaps_gear_down, C_d0_takeoff_flaps_gear_up, C_d0_landing_flaps_gear_down, C_d0_landing_flaps_gear_up, k_clean, k_takeoff, k_landing = DragPolar()

# 	#sorting data into arrays for each stage
# 	#order of climbs: TO, transition seg, 2nd seg, enroute, balked landing, balked landing (OEI)
# 	#used in calculating T/W (uncorrected)
# 	CL_max_array = constants.CL_max
# 	C_d0_array = np.array([C_d0_takeoff_flaps_gear_up, C_d0_takeoff_flaps_gear_down, C_d0_takeoff_flaps_gear_up, C_d0_clean, C_d0_landing_flaps_gear_down, (C_d0_landing_flaps_gear_down+C_d0_takeoff_flaps_gear_down)/2])
# 	ks_array = np.array([1.2, 1.15, 1.2, 1.25, 1.3, 1.5])
# 	K_array = np.array([k_takeoff, k_takeoff, k_takeoff, k_clean, k_landing, k_landing])
# 	G_array = np.array([0.012, 0.00, 0.024, 0.012, 0.032, 0.021])

# 	#used in calculating T/W (corrected), 0-1 indicate condition active or not
# 	thrust_mod_array = np.array([0, 0, 0, 1, 1, 1])
# 	eng_mod_array = np.array([1, 1, 1, 1, 0, 1])
# 	CTOL_mod_array = np.array([0, 0, 0, 0, 1, 1])

# 	#preallocation
# 	TW_array = np.array([])
# 	TW_corrected_array = np.array([])

# 	#calculating uncorrected climb
# 	for i in range(0,6):
# 	TW = calcTWClimb(CL_max_array[i], C_d0_array[i], ks_array[i], K_array[i], G_array[i])
# 	# print TW
# 	TW_corrected = TWcorrection(thrust_mod_array[i], eng_mod_array[i], CTOL_mod_array[i], TW)
# 	# print TW_corrected
# 	# print TW, TW_corrected

# 	TW_array = np.append(TW_array,TW)
# 	TW_corrected_array = np.append(TW_corrected_array, TW_corrected)

# 	# print TW_array
# 	# print TW_corrected_array
# 	# print C_d0_array










