def cl_calc(wingloading):     #wingloading [W/S] [lb/f^2]
	rho = 0.00058727*32.174		#density at 40,000 ft [kg/m^3]
	V = 652.2			#cruise speed [m/s]
	g = 32.174			#gravity to convert to force
	C_L = wingloading*2*g/(rho*(V**2))
	return C_L
