def calcCL(wingloading):     #wingloading [W/S] [lb/f^2]
	rho = (5.87e-4)*32.174		#density at 40,000 ft [lb/f^3]
	V = 823			#cruise speed at 40,000 ft [ft/s]
	g = 32.174			#gravitational acceleration to convert to force
	C_L = wingloading*2*g/(rho*(V**2))
	return C_L

def calcCD(Cf, Swet, Sref, CL, e, AR):
	CD = Cf*Swet/Sref + CL**2/(3.141529*AR*e)
	return CD

def compentCDMethod(surfaces, consts):
	'''
	surfaces is a dictionary of surfaces. where each entry is another dictionary of the surface properties
	'''
	Cd_0 = 0
	for surface in surfaces.keys():
		Cf =  calcCf(surfaces[surface]['charLeng'], consts.v, consts.dens, consts.mu, consts.Density_Cruise, consts.machCruise)



		Cd += 1/consts.Sref*FF*surfaces[surface]['interfernceFactor']*surfaces[surface]['swet']


			


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
		


	#return
	return Cd_0, k, e

	return CD0


def calcCf(C, v, dens, mu, rho, M):
	Re = rho*v*C/mu

	return 0.455/(np.log10(Re)**2.58*(1+0.144*M^2)^0.65)

def calcFF(name, surface):

	if name is 'fueslage':
		f = surface['charLeng']/surface['diameter']
		FF = 1 + 60/f**3 + f/400
	elif name is 'nacelle':
		f = surface['charLeng']/surface['diameter']
		FF = 1 + 0.65/f
	else:
		FF = (1+ 0.6/f)




def calcFlagDrag(cf, c, S_flapped, S_slotted, defl, defl_slotted ):
	Cd = 1.7*(cf/c)^1.38 * (S_flapped/Sref)*sin(defl)^2
	Cd += 0.9*(cf/c)^1.38 * (S_slotted/Sref)*sin(defl_slotted)^2
	return Cd



if __name__ == '__main__':
	#Define w_0

	import constants as consts
	w_0 = calcWeights((5000+200),15, 0.657, M=0.85)[0]	 # [0] <-- only use the first 
	Cd_0, k = DragPolar(w_0, plot=True)[0:2] # [0:2] <-- only use the first two ouputs 
	print Cd_0

	# test for array inputs
	# w_0 = np.array([calcWeights((5000+200),15, 0.657, M=0.85)[0], calcWeights((5000+100),15, 0.657, M=0.85)[0]])	 # [0] <-- only use the first 
	# Cd_0, k = DragPolar(w_0, plot=False)[0:2] # [0:2] <-- only use the first two ouputs 
	# print Cd_0	
