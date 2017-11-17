def calcCL(wingloading):  # wingloading [W/S] [lb/f^2]
	rho = (5.87e-4) * 32.174  # density at 40,000 ft [lb/f^3]
	V = 823  # cruise speed at 40,000 ft [ft/s]
	g = 32.174  # gravitational acceleration to convert to force
	C_L = wingloading * 2 * g / (rho * (V**2))
	return C_L


def calcCD(Cf, Swet, Sref, CL, e, AR):
	CD = Cf * Swet / Sref + CL**2 / (3.141529 * AR * e)
	return CD


def compentCDMethod(consts):
	'''
	surfaces is a dictionary of surfaces. where each entry is another dictionary of the surface properties
	'''

	surfaces = consts.surfaces
	Cd_0 = 0
	for surface in surfaces.keys():

		Cf = calcCf(surfaces[surface] , consts.speed_kts * 0.51444448824222,
			consts.mu, consts.Density_Cruise, consts.machCruise, )

		FF = calcFF(surface, surfaces[surface], consts.machCruise)

		# print surface, Cf, FF, surfaces[surface]['interfernceFactor'], surfaces[surface]['swet']/ consts.Sref
		Cd_0 += surfaces[surface]['swet'] / consts.Sref * FF * Cf * surfaces[surface]['interfernceFactor'] 
		# print Cd_0

	# quit()
	# Missing Form Drag (da = drag area (D\q))
	empennage_upsweep = 6.08853 * 0.0174533														# rad
	da_fuse = 3.83 * empennage_upsweep**2.5 * np.pi * \
		(( surfaces['fuselage']['diameter'] / 2.0)**2)
	# regular wheel and tire, in tandem, and round strut (for nose, and two aft main gears)
	da_lg = (0.25 + 0.15 + 0.30) * (2 * 4.5 + 2.15)
	delC_d0_lg = (da_lg) / consts.Sref
	# 4.5 sq ft for main landing gear

	# engine windmilling effects
	da_engine_windmill = 0.3*2* np.pi *( surfaces['nacelle']['diameter'] / 2)**2
	CD_mis = (da_fuse + da_engine_windmill) / consts.Sref

	print Cd_0

	Cd_0 += CD_mis
	Cd_0 *= 1.035  # Account for Leak and Protuberance Drag

	Cf = calcCf(surfaces['wing'], consts.speed_kts * 0.51444448824222,
				consts.mu, consts.Density_Cruise, consts.machCruise, )

	# solving for the area of the flap
	c_flap_start = 0.9 * consts.c_root + consts.w_lambda * 0.1 * consts.c_root
	c_flap_end = 0.5 * consts.c_root + consts.w_lambda * 0.5 * consts.c_root
	S_flapped = consts.b / 2 * (c_flap_start + c_flap_end) / 2  # m^2

	# calc additional drag at landing and takeoff
	delC_d0_to = calcFlapDrag(
		0.25, S_flapped,  consts.S_wing / 10.7639,  15 * 0.0174533)
	delC_d0_lf = calcFlapDrag(
		0.25, S_flapped,  consts.S_wing / 10.7639,  40 * 0.0174533)


	kappa = 0.95
	sweep = consts.sweep
	thickness = consts.surfaces['wing']['t/c']  # Average
	cruiseCL = consts.CL['cruise']
	M = consts.M

	MDD = kappa / np.cos(sweep) - thickness / (np.cos(sweep)
												** 2) - cruiseCL / (10 * np.cos(sweep)**3)
	Mcrit = MDD - (0.1 / 80)**(1.0 / 3)

	if M > Mcrit:
		print("Valid")

	Cd_0_wave = 20 * (M - Mcrit)**4
	print Cd_0_wave
	Cd0 = {
		'takeoff': {'gear up': Cd_0 + delC_d0_to,
                    'gear down': Cd_0 + delC_d0_lg + delC_d0_to},
		'clean': Cd_0 + Cd_0_wave,
		'landing': {'gear up': Cd_0 + delC_d0_lf,
                    'gear down': Cd_0 + delC_d0_lf + delC_d0_lg}
	}

	e = {
		'takeoff': 0.75,
		'clean': 1.78 * (1 - 0.045 * consts.AR**0.68) - 0.64,
		'landing': 0.70
	}

	print Cd_0

	k = {}
	for key in e.keys():
		k[key] = 1 / (np.pi * consts.AR * e[key])

	#return
	return Cd0, k


def calcCf(surface, v, mu, rho, M):
    # every varible must be in SI!!!

	# Reynolds number breakdown
	# Cruise conditions (40k ft)

	skinRoughness = {
				'camPaint': 3.3e-5,
				'smoothPaint': 2.08e-5,
				'producitonSM': 1.33e-5,
				'polishedSM': 0.50e-5,
				'smoothComp': 0.17e-5
			}

	# print surface, surface['charLeng']


	C = surface['charLeng']
	fracLaminar = surface['fracLaminar']
	k = skinRoughness[surface['finish']]

	Re = rho * v * C / mu
	Re_cutoff_turb = 44.62 * (C / k)**1.053 * M**1.16
	Re_cutoff_laminar = 32.21 * (C / k)**1.053

	if Re_cutoff_turb < Re:
		Re_turb = Re_cutoff_turb
	else:
		Re_turb = Re

	if Re_cutoff_laminar < Re:
		Re_laminar = Re_cutoff_laminar
	else:
		Re_laminar = Re

	Cf = 0.455 / (np.log10(Re)**2.58 * (1 + 0.144 * M**2)**0.65) * (1 - fracLaminar) + \
            1.328 / np.sqrt(Re_laminar) * fracLaminar

	return Cf



def calcFF(name, surface, M):
	if name is 'fuselage':
		f = surface['charLeng'] / surface['diameter']
		FF = 1 + 60 / f**3 + f / 400
	elif name is 'nacelle':
		f = surface['charLeng'] / surface['diameter']
		FF = 1 + 0.65 / f
	else:
		FF = (1 + 0.6 / surface['Xmaxt/c'] * surface['t/c'] + 100 *
		      surface['t/c']**4) * (1.34 * M**0.18 * np.cos(surface['sweep'])**0.28)
		# print (1.34 * M**0.18 * np.cos(surface['sweep'])**0.28), 1.34 * M**0.18, np.cos(surface['sweep'])**0.28

	return FF


def calcFlapDrag(cf_c,  S_flapped, Sref,  defl):
	Cd = 0.9 * (cf_c)**1.38 * (S_flapped / Sref) * np.sin(defl)**2
	return Cd


if __name__ == '__main__':
	#Define w_0
	#calculate Cd0 using the component build up method
	import matplotlib.pyplot as plt
	import os
	import sys
	import inspect

	sys.path.insert(1, os.path.join(sys.path[0], '..'))
	import numpy as np
	import constants as consts
	# w_0 = calcWeights((5000+200),15, 0.657, M=0.85)[0]	 # [0] <-- only use the first
	# Cd_0, k = DragPolar(w_0, plot=True)[0:2] # [0:2] <-- only use the first two ouputs
	# print Cd_0
	plot = True

	Cd_0, k = compentCDMethod(consts)
	if plot:
				#Need to update with appropriate CL limits
			import constants as consts

			CL_range_clean = np.linspace(-0.8, consts.CL['max']['cruise'], 100)
			CL_range_landing = np.linspace(0.2, consts.CL['max']['landing'], 100)
			CL_range_takeoff = np.linspace(-0.1, consts.CL['max']['takeoff'], 100)

			CD_clean = Cd_0['clean'] + k['clean'] * CL_range_clean**2
			CD_takeoff_flaps_gear_down = Cd_0['takeoff']['gear down'] + \
				k['takeoff'] * CL_range_takeoff**2
			CD_takeoff_flaps_gear_up = Cd_0['takeoff']['gear up'] + \
				k['takeoff'] * CL_range_takeoff**2
			CD_landing_flaps_gear_down = Cd_0['landing']['gear down'] + \
				k['landing'] * CL_range_landing**2
			CD_landing_flaps_gear_up = Cd_0['landing']['gear up'] + \
				k['landing'] * CL_range_landing**2

			cruise, = plt.plot(CD_clean, CL_range_clean, linewidth=2,
			                   label='Cruise', color='forestgreen')
			takegearup, = plt.plot(CD_takeoff_flaps_gear_up, CL_range_takeoff,
			                       linewidth=2, label='Takeoff Gear Up', color='orangered')
			takegeardownd, = plt.plot(CD_takeoff_flaps_gear_down, CL_range_takeoff,
			                          linewidth=2, label='Takeoff Gear Down', color='darkred')
			landgearup, = plt.plot(CD_landing_flaps_gear_down, CL_range_landing,
			                       linewidth=2, label='Landing Gear Up', color='skyblue')
			landgeardown, = plt.plot(CD_landing_flaps_gear_up, CL_range_landing,
			                         linewidth=2, label='Landing Gear Down', color='darkblue')
			plt.ylabel('$C_L$', weight='bold', size='x-large')
			plt.xlabel('$C_D$', weight='bold', size='x-large')

			lines = [cruise,	takegearup,	takegeardownd,	landgearup,	landgeardown]
			labels = [x._label for x in lines]

			plt.legend(lines, labels)
			plt.legend(loc='lower right')

			plt.show()
