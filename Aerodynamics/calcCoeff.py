import os,sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))


from AircraftClass.classes import surface, Object

import numpy as np


def calcCL(wingloading):  # wingloading [W/S] [lb/f^2]
	rho = (5.87e-4) * 32.174  # density at 40,000 ft [lb/f^3]
	V = 823  # cruise speed at 40,000 ft [ft/s]
	g = 32.174  # gravitational acceleration to convert to force
	C_L = wingloading * 2 * g / (rho * (V**2))
	return C_L


def calcCD(Cf, Swet, Sref, CL, e, AR):
	CD = Cf * Swet / Sref + CL**2 / (3.141529 * AR * e)
	return CD


def compentCDMethod(plane,M, mu, v, rho, full=True):
	'''
	plane is a module that diffines the aircraft

	full is used for recursion -> no need to bother with it
	'''


	CD_0 = 0
	for name, part in vars(plane).iteritems():
		if (type(part) == surface or type(part) ==Object):
			# print name, ": ", part


			Cf = calcCf(part.MAC_c, part.finish, part.frac_laminar,  v, mu, rho, M)
			FF = calcFF(name, part, M)

			# print FF , Cf 
			CD_0 += part.wetted_area / plane.Sref * FF * Cf * part.interfernce_factor 




	if not(full):
		return CD_0

	# Missing Form Drag (DA = drag area (D\q))
	DA_fuse = 3.83 * (plane.fuselage.empennage_upsweep* 0.0174533)**2.5 * np.pi * \
		(( plane.fuselage.diameter/ 2.0)**2)

	# regular wheel and tire, in tandem, and round strut (for nose, and two aft main gears)
	DA_lg = ((0.25 + 0.15)*1.59*2 + 0.15*1.23)*2 + ( (0.25 + 0.15)*0.52*2 + 0.15*1) 
	delCD0_lg = (DA_lg) / plane.Sref


	CD_mis = (DA_fuse) / plane.Sref



	# engine windmilling effects
	# DA_engine_windmill = 0.3*2* np.pi *( surfaces['nacelle']['diameter'] / 2)**2


	CD_0 += CD_mis
	CD_0 *= 1.035  # Account for Leak and Protuberance Drag


	if plane.name == 'j481':
		flapped_surfaces = [plane.wing, plane.canard]
	else:
		flapped_surfaces = [plane.wing]

	delCD_0_to = 0.0
	delCD_0_lf = 0.0
	for surf in flapped_surfaces:
		# # solving for the area of the flap
		c_flap_start = surf.chord_root + surf.flap_position[0]*(surf.taper - 1) * surf.chord_root 
		c_flap_end = surf.chord_root + surf.flap_position[1]*(surf.taper - 1) * surf.chord_root 
		S_flapped = surf.span*(surf.flap_position[1]- surf.flap_position[0]) * (c_flap_start + c_flap_end) / 2  

		# # calc additional drag at landing and takeoff
		delCD_0_to += calcFlapDrag(
			0.25, S_flapped,  surf.area ,  np.deg2rad(surf.flap_deflection['takeoff']))
		delCD_0_lf += calcFlapDrag(
			0.25, S_flapped,  surf.area ,  np.deg2rad(surf.flap_deflection['landing']))


	kappa = 0.95 # technology factor which assumes supercrtical airfoils


	MDD = kappa / np.cos(np.deg2rad(plane.wing.sweep)) - plane.wing.thickness_chord / (np.cos(np.deg2rad(plane.wing.sweep))
												** 2) - plane.CL['cruise'] / (10. * np.cos(np.deg2rad(plane.wing.sweep))**3)
	Mcrit = MDD - (0.1 / 80)**(1.0 / 3)

	
	if M > Mcrit:
		
		CD_0_wave = 20 * (M - Mcrit)**4
	else:
		CD_0_wave = 0.0



	# values at sea level to calculate CD_0 at takeoff and landing
	# plane = plane.copy()
	v_sea_level = 200.  # ft/s
	mu_sea_level = 3.737e-7  # lb s/ft2
	mach_sea_level = v * 0.514444 / 340
	rho_sea_level = 0.0023769   # slug/ft^3
	CD_0_sea_level = compentCDMethod(plane, mach_sea_level, mu_sea_level, v_sea_level, rho_sea_level , full=False)

	CD_0_dict = {
		'takeoff': {'gear up': CD_0_sea_level + delCD_0_to,
                    'gear down': CD_0_sea_level + delCD0_lg + delCD_0_to},
		'cruise': CD_0 + CD_0_wave,
		'landing': {'gear up': CD_0_sea_level + delCD_0_lf,
                    'gear down': CD_0_sea_level + delCD_0_lf + delCD0_lg}
	}


	# print CD_mis, DA_fuse, delCD0_lg
	# print CD_0_sea_level
	# print 'CD_mis', CD_mis
	# print 'delCD0_lg', delCD0_lg
	# print 'delCD0_lf', delCD_0_lf
	# print 'delCD0_to', delCD_0_to
	# print 'leak and pro', (CD_0/1.035)* 0.035
	# print 'CD_0_wave', CD_0_wave
	# print '--------------------------------'

	return CD_0_dict


def calcCf(C, finish, fracLaminar,  v, mu, rho, M):

	# Reynolds number breakdown

	skinRoughness = {					# all units of ft
				'camPaint': 3.3e-5,		
				'smoothPaint': 2.08e-5,
				'producitonSM': 1.33e-5,
				'polishedSM': 0.50e-5,
				'smoothComp': 0.17e-5
			}

	# print surface, surface['charLeng']


	# print rho , v
	k = skinRoughness[finish]

	Re = rho * v * C / mu

	
	Re_cutoff_turb = 44.62 * (C / k)**1.053 * M**1.16
	Re_cutoff_laminar = 32.21 * (C / k)**1.053

	# print Re, Re_cutoff_turb < Re, Re_cutoff_laminar < Re
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
	# print Cf, Re, surface['charLeng']
	return Cf



def calcFF(name, part, M):
	if name == 'fuselage':
		f = part.MAC_c/ part.diameter
		FF = 1 + 60 / f**3 + f / 400.
	elif name == 'propulsion':
		f = part.MAC_c/ part.diameter
		FF = 1 + 0.65 / f
	else:
		FF = (1 + 0.6 / part.Xmaxt * part.thickness_chord + 100 *
		      part.thickness_chord**4) * (1.34 * M**0.18 * np.cos(np.deg2rad(part.sweep))**0.28)

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

	sys.path.insert(1, os.path.join(sys.path[0], '..'))
	import numpy as np
	import j481
	# w_0 = calcWeights((5000+200),15, 0.657, M=0.85)[0]	 # [0] <-- only use the first
	# CD_0, k = DragPolar(w_0, plot=True)[0:2] # [0:2] <-- only use the first two ouputs
	# print CD_0
	plot = True
	k = j481.k

	CD_0 = compentCDMethod(j481, j481.mach, j481.mu_cruise, j481.speed_fps, j481.density_cruise)

	if plot:
				#Need to upDAte with appropriate CL limits

			CL_range_clean = np.linspace(-0.8, j481.CL['max']['cruise'], 100)
			CL_range_landing = np.linspace(0.2, j481.CL['max']['landing'], 100)
			CL_range_takeoff = np.linspace(-0.1, j481.CL['max']['takeoff'], 100)

			CD_clean = CD_0['cruise'] + k['cruise'] * CL_range_clean**2
			CD_takeoff_flaps_gear_down = CD_0['takeoff']['gear down'] + \
				k['takeoff'] * CL_range_takeoff**2
			CD_takeoff_flaps_gear_up = CD_0['takeoff']['gear up'] + \
				k['takeoff'] * CL_range_takeoff**2
			CD_landing_flaps_gear_down = CD_0['landing']['gear down'] + \
				k['landing'] * CL_range_landing**2
			CD_landing_flaps_gear_up = CD_0['landing']['gear up'] + \
				k['landing'] * CL_range_landing**2

			cruise, = plt.plot(CD_clean, CL_range_clean, linewidth=2,
			                   label='Cruise', color='forestgreen')
			takegearup, = plt.plot(CD_takeoff_flaps_gear_up, CL_range_takeoff,
			                       linewidth=2, label='Takeoff Gear Up', color='orangered')
			takegeardownd, = plt.plot(CD_takeoff_flaps_gear_down, CL_range_takeoff,
			                          linewidth=2, label='Takeoff Gear Down', color='DArkred')
			landgearup, = plt.plot(CD_landing_flaps_gear_down, CL_range_landing,
			                       linewidth=2, label='Landing Gear Up', color='skyblue')
			landgeardown, = plt.plot(CD_landing_flaps_gear_up, CL_range_landing,
			                         linewidth=2, label='Landing Gear Down', color='DArkblue')
			plt.ylabel('$C_L$', weight='bold', size='x-large')
			plt.xlabel('$C_D$', weight='bold', size='x-large')

			lines = [cruise,	takegearup,	takegeardownd,	landgearup,	landgeardown]
			labels = [x._label for x in lines]

			plt.legend(lines, labels)
			plt.legend(loc='lower right')

			plt.show()
