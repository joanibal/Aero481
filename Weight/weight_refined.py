import os,sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))

# import Sizing.horizontal_surf_sizing as hs
from Aerodynamics.calcCoeff import compentCDMethod
# import Sizing.Svt_calc
from Weight.weight_estimation import calcWeights
import numpy as np
# # import matplotlib.pyplot as plt
# # import constants as plane
# # from Sizing.Svt_calc import *
# # from Sizing.horizontal_surf_sizing import *

# from Aerodynamics.avlLib import runAVL, changeSref
from Sizing.tailSizing import genTail


from AircraftClass.classes import surface, Object

#------------------------------------------------------------------#

#----------------------------------------------------#
def fuel_fraction(c, CD, R, speed, CL):
	ff1 = 0.99		#warmup
	ff2 = 0.995 	#taxi
	ff3 = 0.995	 	#TO
	ff4 = 0.98		#climb

	ff6 = 0.99 		#descent
	ff7 = 0.992		#landing
	
	cruiseFrac = np.exp(R*c*CD/(speed*CL))
	ff5 = 1/cruiseFrac
	ff = ff1*ff2*ff3*ff4*ff5*ff6*ff7
	# print cruiseFrac, ff5, ff, 1-ff
	return 1-ff

def fuel_fraction_update(c, c_sealevel, Sref, T, w_0, CD0, alt_cruise, V, R, K, n):
	
	ff_startup = 1.0-c_sealevel*(15.0/60.0)*(T*0.05/w_0)	#startup/warmup/taxi
	w_startup = ff_startup*w_0
	# print 'startup '+str(ff_startup)
	
	ff_TO = 1.0-c_sealevel*(1/60.0)*(T/w_startup)
	w_takeoff = ff_TO*w_startup
	# print 'TO '+str(ff_TO)
	
	ff_climb = 0.98 #historical
	w_climb = ff_climb*w_takeoff
	# print 'climb '+str(ff_climb)

	w_cruise_i = w_climb
	alt_cruise_i = alt_cruise
	temp = -56.46 + 273.15 #K - approximately constant for altitude range

	for i in range(int(n)):
		p = 22.65 * np.exp(1.73 - .000157*(alt_cruise_i*0.3048)) #kPa
		# print 'pressure '+str(p)
		rho_metric = p*1000.0/(287.058*temp)
		rho = rho_metric*0.00194032

		# V constant because a = sqrt(gamma*R*T) -> T is approx. constant
		CL = np.sqrt(CD0/K)* 0.707
		# selecting CL for cruise altitude and starting cruise climb from there
		# CL = 2*w_0/(rho*(V*1.68781)**2*Sref)
		# print rho, Sref, w_cruise_i
		# print CL, rho

		# print('start')
		# L_D = CL/(CD0 + runAVL(CL=CL ,geo_file='./Aerodynamics/j481.avl'))
		L_D = CL/(CD0 + K*CL**2)
		# print CL, L_D, CD0, CL/(CD0 + K*CL**2)

		# print('L_D', L_D, CL/(CD0 + K*CL**2))
		# print(CL/(CD0 + K*CL**2))

		# print R , n, c ,V , L_D
		ff_cruise_step = np.exp(-(R)*c/(V*L_D))
		# print 'cruise_step '+str(ff_cruise_step)

		# used in next iteration
		w_cruise_i = ff_cruise_step*w_cruise_i
		# print 'altitude '+str(alt_cruise_i), 'CL step '+str(CL), 'weight '+str(w_cruise_i)
		# print 'w_cruise_step '+str(w_cruise_i)
		# print i, alt_cruise_i, R, n, R/n, rho
		
		alt_cruise_i += 2000.0 			#steps determined by ATC

	ff_cruise = w_cruise_i/w_climb
	# print 'cruise '+str(ff_cruise)

	ff_descent = 0.99 #historical
	ff_landing = 0.992 #historical

	ff = ff_startup*ff_TO*ff_climb*ff_cruise*ff_descent*ff_landing

	return 1-ff


def prelim_weight(Sref, T0, plane):
    	'''
	#Sref in ft^2, T0 in lbs
	'''

	# if plane.name === 

	# update plane with new Sizing info
	plane.thrust = T0



	plane.Sref = Sref
	# plane.wing.update(area=plane.Sref*plane.wing_area_ratio)

	# idk why but == works better of string comparison
	if plane.name=='j481':
		plane.wing.update(area=plane.Sref*plane.wing_area_ratio)

		plane.canard.update(area=plane.Sref*plane.canard_area_ratio)
		plane.tail_vert, plane.tail_horz = genTail(plane.wing, plane.dist_to_surface ,  canard=plane.canard)
		# plane.canard.weight = 7.5*plane.canard.area




		plane.canard.comp = 1
		plane.wing.comp = 0.8
		plane.tail_horz.comp = 0.75
		plane.tail_vert.comp = 0.75
		plane.fuselage.comp = 0.75
		plane.propulsion.comp = 1.0
		gear_comp = 0.92
		
		plane.CD0 = compentCDMethod(plane, plane.mach, plane.mu_cruise, plane.speed_fps, plane.density_cruise)


	elif plane.name == 'g550':
		# plane.tail_vert = plane.tail_vert
		# plane.tail_horz = plane.tail_horz
		plane.wing.update(area=plane.Sref )

		plane.tail_vert, plane.tail_horz = genTail(plane.wing, plane.dist_to_surface)

		plane.CD0 = compentCDMethod(
			plane, plane.mach, plane.mu_cruise, plane.speed_fps, plane.density_cruise)

		plane.wing.comp = 1.0
		plane.tail_horz.comp = 1.0
		plane.tail_vert.comp = 1.0
		plane.fuselage.comp = 1.0
		plane.propulsion.comp = 1.0
		gear_comp = 1.0
	else:
    		raise ValueError('plane name "%s" not recognized' % plane.name)


	# plane.CD0 = compentCDMethod(plane, plane.mach, plane.mu_cruise, plane.speed_fps, plane.density_cruise)
	# print .003*(plane.fuselage.wetted_area + 2.2*plane.Sref)/plane.Sref, plane.CD0['cruise']


	# print plane.CD0

	# # engine weight calculations (lbs)
	w_eng_dry = 0.521*(T0)**0.9
	w_eng_oil = 0.082*(T0)**0.65
	w_eng_rev = 0.034*(T0)	
	# w_eng_control = 0.26*(T0)**0.5
	# w_eng_start = 9.33*(w_eng_dry/1000.0)**1.078
	w_eng = w_eng_dry + w_eng_oil + w_eng_rev
	w_nacelle = 0.6724*1.017*(plane.propulsion.length**0.1)*(plane.propulsion.diameter**0.294)\
				*(plane.load_factor**0.119)*(w_eng**0.611)*(plane.numEngines**0.984)\
				*(plane.propulsion.wetted_area**0.224)	#cowl/duct
	w_engcontrol = plane.Keco*(plane.fuselage.length*plane.numEngines)**0.792
	
	#starting systems
	w_start_cp = 9.33*(plane.numEngines*w_eng*10**(-3))**1.078	#cartridge/pneumatic
	w_start_elec = 38.93*(plane.numEngines*w_eng*10**(-3))**0.918	#electrical

	# w_eng_total = w_eng*plane.numEngines + plane.propulsion.comp*w_nacelle + w_engcontrol + w_start_cp + w_start_elec
	plane.propulsion.weight = w_eng*plane.numEngines + plane.propulsion.comp*w_nacelle + w_engcontrol + w_start_cp + w_start_elec
	# print w_eng, w_nacelle, w_engcontrol, w_start_cp, w_start_elec
	# print 'engine', w_eng_total

	# to prevent redoing calculations and preserve the first guess
	w_avionics = 19.2+11+5+3.5+8.4+44+78.4+168.5+14+38.2+37+15.6
	# print 'avionics', w_avionics

	w_flightdeck = 54.99*plane.num_pilots	#flight deck seats
	w_passseats = 32.03*plane.num_passengers	#passenger seats
	w_lav = 3.90*(plane.num_passengers**1.33)	#lavatories
	w_food = 5.68*(plane.num_passengers**1.12)	#food
	w_oxygen = 7*(plane.num_pilots+plane.num_passengers+plane.num_attendants)**0.702	#oxygen
	w_windows = 109.33*(plane.num_passengers*(1+plane.fuselage.cabinpressure)*10**(-2))**0.505	#windows
	w_baggage = 0.0646*plane.num_passengers**1.456	#baggage
	w_ac = 469.30*((45.83*60*(plane.num_pilots+plane.num_attendants+plane.num_passengers)*10**(-4))**0.419)	#air conditioning
	w_interior = w_flightdeck + w_passseats + 2.0 * w_lav + \
		w_food + w_oxygen + w_windows + w_baggage + w_ac

	try:
		w_0 = plane.MTOW
		# print('smart')
	except:
		# print plane.range_nMi, plane.LD_ratio, plane.SFC, plane.mach, plane.weight_payload
		# w_0 = calcWeights(plane.range_nMi, plane.LD_ratio, plane.SFC, plane.mach, plane.weight_payload)[0]
		w_0 = 66000


	# print w_0
	# quit()

	tolerance = 10.0
	converged = 0



	while True:
	# for i in range(1000):

		sweep_halfchord = np.arctan((0.5 *plane.wing.span *np.tan(np.deg2rad(plane.wing.sweep)) -0.25 *plane.wing.chord_root + 0.25 *plane.wing.taper*plane.wing.chord_root) /(0.5 *plane.wing.span))
		Wwing_carichner = (0.00428 * plane.wing.area**0.48) * ((plane.wing.aspect_ratio * plane.mach**0.43)
                         / (100 * plane.wing.thickness_chord)**0.76) * ((w_0 * plane.load_factor)**0.84 *
                         plane.wing.taper**0.14) / (np.cos(sweep_halfchord)**1.54)
		Wwing_raymer = 0.0051 * ((w_0 * plane.load_factor)**0.557) * (plane.wing.area**0.649)\
                    * (plane.wing.aspect_ratio**0.5) * (plane.wing.thickness_chord**(-0.4))\
                    * ((1 + plane.wing.taper)**0.1) * (np.cos(np.deg2rad(plane.wing.sweep))**(-1))\
                    * (plane.wing.mounted_area**0.1)
		plane.wing.weight = plane.wing.comp * (Wwing_raymer + Wwing_carichner) / 2.0


		plane.tail_horz.weight = plane.tail_horz.comp * 0.0034 *( ((w_0 * plane.load_factor)**0.813) * ((plane.tail_horz.area )**0.584) * (
			(plane.tail_horz.span / (plane.tail_horz.chord_root*plane.tail_horz.thickness_chord))**0.033) * ((plane.tail_horz.MAC_c ) / (plane.dist_to_surface[0] ))**0.28 ) **0.915

		if plane.name=='j481':
    			plane.canard.weight = plane.canard.comp * 0.0034 *( ((w_0 * plane.load_factor)**0.813) * ((plane.canard.area )**0.584) * (\
				(plane.canard.span / (plane.canard.chord_root * plane.canard.thickness_chord))**0.033) * ((plane.canard.MAC_c ) / ((plane.wing.coords[0, 0] - plane.canard.coords[0, 0]) ))**0.28 )**0.915



		plane.tail_vert.weight = plane.tail_vert.comp * 0.19 *( ((1 + 1)**0.5) * ((w_0 * plane.load_factor)**0.363) * ((plane.tail_vert.area )**1.089) * (plane.mach**0.601) * ((plane.dist_to_surface[1] )**(-0.726)) * (
			(1 + 0.3)**0.217) * (plane.tail_vert.aspect_ratio**0.337) * ((1 + plane.tail_vert.taper)**0.363) * (np.cos(np.deg2rad(plane.tail_vert.sweep))**(-0.484)) )**1.014


		plane.fuselage.weight=plane.fuselage.comp * 10.43 * (1.25**1.42) * ((plane.q_cruise * 10**(-2))**0.283) * (
			(w_0 * 10**(-3))**0.95) * ((plane.fuselage.length / 8.8)**0.71)

		w_control_surfaces = 56.01*(w_0*plane.q_cruise*10**(-5))**0.576

		
		ff_step = fuel_fraction_update(plane.SFC, plane.SFC_sealevel, plane.Sref, T0, w_0, plane.CD0['cruise'] , plane.altitude, plane.speed_kts, plane.range_nMi, plane.k['cruise'], plane.cruise_steps)
		w_fuel = ff_step*w_0


		w_bladder = 23.10*((w_fuel/plane.jetA_density)*10**(-2))**0.758	#bladder cells
		w_bladdersupport = 7.91*((w_fuel/plane.jetA_density)*10**(-2))**0.854	#bladder cells supports
		w_dumpdrain = 7.38*((w_fuel/plane.jetA_density)*10**(-2))**0.458	#dump and drain
		w_cgcontrol = 28.38*((w_fuel/plane.jetA_density)*10**(-2))**0.442	#cg control system

		w_fuelcontrol = w_bladder + w_bladdersupport + w_dumpdrain + w_cgcontrol

		w_flightind = plane.num_pilots*(15+0.032*(w_0*10**(-3)))	#flight indicators
		w_engineind = plane.numEngines*(4.80+0.006*(w_0*10**(-3)))	#engine indicators
		w_miscind = 0.15*(w_0*10**(-3))	#misc indicators
		# print w_flightind, w_engineind, w_miscind
		w_indicators = w_flightind + w_engineind + w_miscind

		w_landing_gear = gear_comp*62.21*(w_0*(10**(-3)))**0.84
		w_nose_gear = w_landing_gear*0.15 #lb
		w_main_gear = 0.85*w_landing_gear/2.0 #lb

		w_miscfurnish = 0.771*(w_0*10**(-3))	#misc
		w_elec_transport = 1162.66*((w_fuelcontrol*w_avionics)*10**(-3))**0.506 # transport
		w_elec_fight = 426.17*((w_fuelcontrol*w_avionics)*10**(-3))**0.51 # fighter
		w_elec = (w_elec_transport + w_elec_fight)/2.0

		
		w_0new = 0.
		for name, part in vars(plane).iteritems():
    			if (type(part) == surface or type(part)==Object ):
    				# if i ==0:
						# print name, part.weight
    				w_0new += part.weight

		wight_main_comp = w_0new
		# add the misc. things 
		w_0new += w_avionics + w_interior + w_control_surfaces +\
				 w_fuel + w_fuelcontrol + w_indicators + w_landing_gear +\
				 w_miscfurnish  + w_elec

		#convergence check
		if plane.name =='j481':
			canard_weight = plane.canard.weight
		else:
			canard_weight = 0.0

		w_breakdown = {'engine_total':plane.propulsion.weight,
						'avionics':w_avionics,
						'interior':w_interior,
						'wing':plane.wing.weight,
						'HT': plane.tail_horz.weight,
						'canard':canard_weight,
						'VT': plane.tail_vert.weight,
						'fuselage': plane.fuselage.weight,
						'surface_control':w_control_surfaces,
						'fuel_control':w_fuelcontrol,
						'indicators':w_indicators,
						'nose_gear':w_nose_gear,
						'main_gear':w_main_gear,
						'misc':w_miscfurnish,
						'fuel': w_fuel,
						'electronics':w_elec 
						}
		if abs(w_0new - w_0) <= tolerance:
		# if True:
			plane.MTOW = w_0

			# for key in w_breakdown.keys():
			# 	print key, w_breakdown[key]

			# print 'fuselage:', w_breakdown['fuselage']+w_breakdown['interior']+w_breakdown['indicators']+w_breakdown['misc']+w_breakdown['electronics']+w_breakdown['avionics']
			# print 'wing:', w_breakdown['wing']+w_breakdown['surface_control']+w_breakdown['fuel_control']
			# print 'HT:', w_breakdown['HT']
			# print 'VT:', w_breakdown['VT']
			# print 'canard:', w_breakdown['canard']
			# print 'landing gears', w_breakdown['main_gear'], w_breakdown['nose_gear']
			# print 'engine(x2):', w_breakdown['engine_total']
		
			return w_0, w_fuel, plane

		w_0 += 1.0*(w_0new - w_0)


	return w_0, w_fuel, plane

if __name__ == '__main__':


	import j481
	import g550

	w_0, w_f, plane = prelim_weight(j481.Sref, j481.thrust_req, j481)
	print 'j481:',w_0, w_f

	w_0, w_f, plane = prelim_weight(g550.Sref, g550.thrust_req, g550)
	print 'g550:', w_0, w_f	



