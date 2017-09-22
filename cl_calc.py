def cl_calc(wingloading):     #wingloading [W/S] [lb/f^2]
	rho = (5.87e-4)*32.174		#density at 40,000 ft [lb/f^3]
	V = 823			#cruise speed at 40,000 ft [ft/s]
	g = 32.174			#gravitational acceleration to convert to force
	C_L = wingloading*2*g/(rho*(V**2))
	return C_L
