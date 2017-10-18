def calcCL(wingloading):     #wingloading [W/S] [lb/f^2]
	rho = (5.87e-4)*32.174		#density at 40,000 ft [lb/f^3]
	V = 823			#cruise speed at 40,000 ft [ft/s]
	g = 32.174			#gravitational acceleration to convert to force
	C_L = wingloading*2*g/(rho*(V**2))
	return C_L

def calcCD(Cf, Swet, Sref, CL, e, AR):
	CD = Cf*Swet/Sref + CL**2/(3.141529*AR*e)
	return CD
