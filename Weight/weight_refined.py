import os,sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))

# import Sizing.horizontal_surf_sizing as hs
from Aerodynamics.calcCoeff import compentCDMethod
# import Sizing.Svt_calc
from Weight.weight_estimation import calcWeights
# import numpy as np
# # import matplotlib.pyplot as plt
# # import constants as plane
# # from Sizing.Svt_calc import *
# # from Sizing.horizontal_surf_sizing import *

# from Aerodynamics.avlLib import runAVL, changeSref
from Sizing.tailSizing import genTail
#------------------------------------------------------------------#

# # wing weight calculations
# Wwing_carichner = (0.00428*Sref_wing**0.48)*((plane.AR*plane.M**0.43)/(100*plane.tc)**0.76)*((MTOW*plane.N)**0.84*plane.w_lambda**0.14)/(np.cos(plane.lambda_half)**1.54)
# Wwing_raymer = 0.0051*((MTOW*plane.N)**0.557)*(Sref_wing**0.649)*(plane.AR**0.5)*(plane.tc**(-0.4))*((1+w_lambda)**0.1)*(math.cos(plane.sweep)**(-1))*(plane.wing_mounted_area**0.1)

# #horizontal tail calc
# gamma_horiz = ((w_0*plane.N)**0.813)*((S_HT*10.7639)**0.584)*((plane.span_h/plane.t_root_h)**0.033)*((plane.c_MAC/0.3048)/plane.L_HT)**0.28
# W_horiz = 0.0034*gamma_horiz**0.915

# #canard calc
# gamma_canard = ((w_0*plane.N)**0.813)*((plane.Sref_c_actual*10.7639)**0.584)*((plane.span_c/plane.t_root_c)**0.033)*((plane.c_MAC/0.3048)/plane.L_c)**0.28
# W_canard = 0.0034*gamma_canard**0.915

# #vertical tail
# gamma_vert = ((1+1)**0.5)*((w_0*plane.N)**0.363)*(S_VT**1.089)*(plane.M**0.601)*(plane.L_VT**(-0.726))*((1+plane.Arudder/S_VT)**0.217)*(plane.AR_VT**0.337)*((1+plane.taper_VT)**0.363)*(math.cos(plane.sweep_VT)**(-0.484))
# W_vert = 0.19*gamma_vert**1.014

# #fuselage
# W_fuselage = 10.43*(1.25**1.42)*((plane.q*10**(-2))**0.283)*((w_0*10**(-3))**0.95)*((plane.fuselage.length/8.8)**0.71)

#landing gear
# W_gear = 62.21*(MTOW*(10**(-3)))**0.84

#propulsion
# W_nacelle = 0.6724*1.017*(plane.nacelle_length**0.1)*(plane.nacelle_width**0.294)*(plane.N**0.119)*(weight_eng**0.611)*(plane.numEngines**0.984)*(plane.nacelle_wetted_area**0.224)	#cowl/duct
# W_bladder = 23.10*((fuelweight)*10**(-2))**0.758	#bladder cells
# W_bladdersupport = 7.91*((fuelweight)*10**(-2))**0.854	#bladder cells supports
# W_dumpdrain = 7.38*((fuelweight)*10**(-2))**0.458	#dump and drain
# W_cgcontrol = 28.38*((fuelweight)*10**(-2))**0.442	#cg control system

#engine controls
# w_engcontrol = plane.Keco*(plane.fuselage.length/0.3048*plane.numEngines)**0.792

#starting systems
# W_start_cp = 9.33*(plane.numEngines*w_eng*10**(-3))**1.078	#cartridge/pneumatic
# W_start_elec = 38.93*(plane.numEngines*w_eng*10**(-3))**0.918	#electrical

#surface controls
# W_surfcont = 56.01*(MTOW*plane.q*10**(-5))**0.576

#instruments
# W_flightind = plane.num_pilots*(15+0.032*(MTOW*10**(-3)))	#flight indicators
# W_engineind = plane.numEngines*(4.80+0.006*(MTOW*10**(-3)))	#engine indicators
# W_miscind = 0.15*(MTOW*10**(-3))	#misc indicators

#avionics
# w_avionics = 19.2+11+5+3.5+44+78.4+168.5+14+38.2+37+15.6

#electrical system
# w_elec = 1162.66*((w_bladder+w_bladdersupport+w_dumpdrain+w_cgcontrol)*w_avionics*10**(-3))**0.506

#furnishings
# w_flightdeck = 54.99*plane.num_pilots	#flight deck seats
# w_passseats = 32.03*plane.num_passengers	#passenger seats
# w_lav = 3.90*(plane.num_passengers**1.33)	#lavatories
# w_food = 5.68*(plane.num_passengers**1.12)	#food
# w_oxygen = 7*(plane.num_pilots+plane.num_passengers+plane.num_attendants)**0.702	#oxygen
# w_windows = 109.33*(plane.num_passengers*(1+plane.cabinpressure)*10**(-2))**0.505	#windows
# w_baggage = 0.0646*plane.num_passengers**1.456	#baggage
# w_ac = 469.30*((45.83*60*(plane.num_pilots+plane.num_attendants+plane.num_passengers)*10**(-4))**0.419)	#air conditioning
# w_miscfurnish = 0.771*(w_0*10**(-3))	#misc

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
		CL = 2.0*w_cruise_i/(rho*(V*1.68781)**2.0*Sref)
		# print rho, Sref, w_cruise_i


		# print('start')
		# L_D = CL/(CD0 + runAVL(CL=CL ,geo_file='./Aerodynamics/J481T.avl'))
		L_D = CL/(CD0 + CL/(CD0 + K*CL**2))
		# print CL, L_D, CL/(CD0 + K*CL**2)

		# print('L_D', L_D, CL/(CD0 + K*CL**2))
		# print(CL/(CD0 + K*CL**2))

		# print CL, CD0, K, L_D
		ff_cruise_step = np.exp(-(R/n)*c/(V*L_D))
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
	plane.wing.update(area=plane.Sref*plane.wing_area_ratio)

	# idk why but == works better of string comparison
	if plane.name=='j481':
		plane.canard.update(area=plane.Sref*plane.canard_area_ratio)
		plane.tail_vert, plane.tail_horz = genTail(plane.wing, plane.dist_to_surface ,  canard=plane.canard)
		plane.canard.weight = 7.5*plane.canard.area

	elif plane.name == 'g550':
    		plane.tail_vert, plane.tail_horz = genTail(plane.wing, plane.dist_to_surface)
	else:
    		raise ValueError('plane name "%s" not recognized' % plane.name)



	plane.CD0 = compentCDMethod(plane);

	# CD0 = plane.C_f*(plane.Swet_rest + 2.0*Sref_wing)/Sref_wing


	# # engine weight calculations (lbs)
	w_eng_dry = 0.521*(T0)**0.9
	w_eng_oil = 0.082*(T0)**0.65
	w_eng_rev = 0.034*(T0)	
	# w_eng_control = 0.26*(T0)**0.5
	# w_eng_start = 9.33*(w_eng_dry/1000.0)**1.078
	w_eng = w_eng_dry + w_eng_oil + w_eng_rev
	w_nacelle = 0.6724*1.017*(plane.nacelle.length**0.1)*(plane.nacelle.diameter**0.294)\
				*(plane.load_factor**0.119)*(w_eng**0.611)*(plane.numEngines**0.984)\
				*(plane.nacelle.wetted_area**0.224)	#cowl/duct
	w_engcontrol = plane.Keco*(plane.fuselage.length/0.3048*plane.numEngines)**0.792
	
	#starting systems
	w_start_cp = 9.33*(plane.numEngines*w_eng*10**(-3))**1.078	#cartridge/pneumatic
	w_start_elec = 38.93*(plane.numEngines*w_eng*10**(-3))**0.918	#electrical

	w_eng_total = w_eng*plane.numEngines + plane.nacelle.comp*w_nacelle + w_engcontrol + w_start_cp + w_start_elec
	# print w_eng, w_nacelle, w_engcontrol, w_start_cp, w_start_elec
	# print 'engine', w_eng_total

	# to prevent redoing calculations and preserve the first guess
	try:
		plane.wing.weight
	except:
		# do the calculation for the weight of the interior
		plane.wing.weight= 7.5*plane.wing.area
		plane.tail_horz.weight = 4.0*plane.tail_horz.area
		plane.tail_vert.weight = 4.0*plane.tail_vert.area
		

		plane.fuselage.weight = 3.5*plane.fuselage.wetted_area
		# w_fuse = 2.5*plane.Swet_fuse


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
		# print w_flightdeck, w_passseats, w_lav, w_food, w_oxygen, w_windows, w_baggage, w_ac
		plane.fuselage.interior_weight = w_flightdeck + w_passseats +  2.0*w_lav + w_food + w_oxygen + w_windows + w_baggage + w_ac
		# print 'interior', w_interior


		#iterating for MTOW	
		w_0, _, _, w_crew_payload = calcWeights(plane.range, plane.LD_ratio, plane.SFC, plane.mach, plane.payload)


	# quit()

	tolerance = 1.0
	converged = 0

	while True:
	# for i in range(1000):
		# CL = calcCL(w_0/Sref_wing)
		
		Wwing_carichner = (0.00428*wing.area**0.48)*((wing.aspect_ratio*plane.mach**0.43)\
						/ (100 * plane.wing.thickness_chord)**0.76) * ((w_0 * plane.N)**0.84 *\
						 plane.wing.taper**0.14)/(np.cos(np.rad2deg(plane.wing.sweep/2))**1.54)
		# print 'carichner', Wwing_carichner
		Wwing_raymer = 0.0051*((w_0*plane.N)**0.557)*(wing.area**0.649)\
					   *(plane.wing.aspect_ratio**0.5)*(plane.wing.thickness_chord**(-0.4))\
					   *((1+plane.taper)**0.1)*(np.cos(plane.sweep)**(-1))\
					   *(plane.wing_mounted_area**0.1)
		# print 'raymer', Wwing_raymer
		plane.wing.weight = wing_comp * (Wwing_raymer + Wwing_carichner) / 2.0

		Wwing_carichner = (0.00428 * wing.area**0.48) * ((wing.aspect_ratio * plane.mach**0.43)
                                                   / (100 * plane.thickness_chord)**0.76) * ((w_0 * plane.N)**0.84 *
                                                                                             plane.w_lambda**0.14) / (np.cos(np.rad2deg(plane.wing.sweep / 2))**1.54)
		# print 'carichner', Wwing_carichner
		Wwing_raymer = 0.0051 * ((w_0 * plane.N)**0.557) * (Sref_wing**0.649) * (plane.AR**0.5) * (plane.tc **
                                                                                             (-0.4)) * ((1 + plane.w_lambda)**0.1) * (np.cos(plane.sweep)**(-1)) * (plane.wing_mounted_area**0.1)
		# print 'raymer', Wwing_raymer
		plane.wing.weight = wing_comp * (Wwing_raymer + Wwing_carichner) / 2.0

		
		Wcanard_carichner = (0.00428*plane.wing.sref**0.48)*((plane.wing.aspect_ratio*plane.M**0.43)/(100*plane.tc)**0.76)*((w_0*plane.N)**0.84*plane.w_lambda**0.14)/(np.cos(plane.sweep_half)**1.54)
		# print 'carichner', Wcanard_carichner
		Wcanard_raymer = 0.0051*((w_0*plane.N)**0.557)*(Sref_wing**0.649)*(plane.AR**0.5)*(plane.tc**(-0.4))*((1+plane.w_lambda)**0.1)*(np.cos(plane.sweep)**(-1))*(plane.wing_mounted_area**0.1)
		# print 'raymer', Wwing_raymer
		w_wing = canard_comp*(Wcanard_raymer + Wcanard_carichner)/2.0
		# w_canard = Wcanard_carichner

		# print 'wing', w_wing

		gamma_horiz = ((w_0*plane.N)**0.813)*((S_HT*10.7639)**0.584)*((plane.span_h/plane.t_root_h)**0.033)*((plane.c_MAC/0.3048)/(plane.L_HT/0.3048))**0.28
		w_HT = tail_comp*0.0034*gamma_horiz**0.915
		# print 'HT', w_HT

		try:
			gamma_canard = ((w_0*plane.N)**0.813)*((plane.Sref_c_actual*10.7639)**0.584)*((plane.span_c/plane.t_root_c)**0.033)*((plane.c_MAC/0.3048)/(plane.L_c/0.3048))**0.28
			w_c = tail_comp*0.0034*gamma_canard**0.915
			# print 'c', w_c

		except:
			w_c = 0

		gamma_vert = ((1+1)**0.5)*((w_0*plane.N)**0.363)*((S_VT*10.7639)**1.089)*(plane.M**0.601)*((plane.L_VT/0.3048)**(-0.726))*((1+plane.Arudder/S_VT)**0.217)*(AR_VT**0.337)*((1+plane.taper_VT)**0.363)*(np.cos(plane.sweep_VT)**(-0.484))
		w_VT = tail_comp*0.19*gamma_vert**1.014
		# print 'VT', w_VT

		w_fuse = fuselage.comp*10.43*(1.25**1.42)*((plane.q*10**(-2))**0.283)*((w_0*10**(-3))**0.95)*((plane.fuselage.length/0.3048/8.8)**0.71)
		# print 'fuse', w_fuse

		w_surfcont = 56.01*(w_0*plane.q*10**(-5))**0.576
		# print w_surfcont

		# CD0 = plane.C_f*(plane.Swet_rest + 2.0*Sref_wing)/Sref_wing


		




		# print(plane.C_f*(plane.Swet_rest + 2.0*Sref_wing)/Sref_wing, compentCDMethod(plane)[0]['clean'])
		# CL = np.sqrt(CD0*np.pi*plane.AR*plane.e['cruise'])
		# CD = CD0 + CL**2/(np.pi*plane.AR*plane.e['cruise'])
		# ff = fuel_fraction(plane.SFC, CD, plane.R, plane.speed_kts, CL)
		# w_f = ff*w_0
		ff_step = fuel_fraction_update(plane.SFC, plane.SFC_sealevel, Sref_wing, T0, w_0, CD0, plane.alt, plane.speed_kts, plane.R, K['clean'], plane.cruise_steps)
		w_f = ff_step*w_0


		w_bladder = 23.10*((w_f/plane.jetA_density)*10**(-2))**0.758	#bladder cells
		w_bladdersupport = 7.91*((w_f/plane.jetA_density)*10**(-2))**0.854	#bladder cells supports
		w_dumpdrain = 7.38*((w_f/plane.jetA_density)*10**(-2))**0.458	#dump and drain
		w_cgcontrol = 28.38*((w_f/plane.jetA_density)*10**(-2))**0.442	#cg control system

		w_fuelcontrol = w_bladder + w_bladdersupport + w_dumpdrain + w_cgcontrol

		w_flightind = plane.num_pilots*(15+0.032*(w_0*10**(-3)))	#flight indicators
		w_engineind = plane.numEngines*(4.80+0.006*(w_0*10**(-3)))	#engine indicators
		w_miscind = 0.15*(w_0*10**(-3))	#misc indicators
		# print w_flightind, w_engineind, w_miscind
		w_indicators = w_flightind + w_engineind + w_miscind
		# print 'indicators', w_indicators

		w_landing_gear = gear_comp*62.21*(w_0*(10**(-3)))**0.84
		# w_landing_gear = w_0*0.043 #lb
		w_nose_gear = w_landing_gear*0.15 #lb
		w_main_gear = 0.85*w_landing_gear/2.0 #lb
		# w_xtra = 0.17*w_0 #lb
		w_miscfurnish = 0.771*(w_0*10**(-3))	#misc
		w_elec_transport = 1162.66*((w_fuelcontrol*w_avionics)*10**(-3))**0.506 # transport
		w_elec_fight = 426.17*((w_fuelcontrol*w_avionics)*10**(-3))**0.51 # fighter
		w_elec = (w_elec_transport + w_elec_fight)/2.0
		# w_elec = 12.57*(w_fuelcontrol*w_avionics)**(0.51) #raymer GA
		# print 'landing gear', w_landing_gear
		# print 'misc furnishings', w_miscfurnish
		# print 'w_avionics', w_avionics
		# print 'fuel control', w_fuelcontrol
		# print 'electron`ics', w_elec

		w_0new = w_eng_total + w_avionics + w_interior + w_wing + w_HT +\
				w_c + w_VT + w_fuse + w_surfcont + w_f + w_fuelcontrol +\
				w_indicators + w_landing_gear + w_miscfurnish + w_elec
		# print w_eng_total, w_avionics, w_interior, w_wing, w_HT, w_c, w_VT, w_fuse, w_surfcont, w_f, w_fuelcontrol, w_indicators, w_landing_gear, w_miscfurnish, w_elec

		#convergence check
		if abs(w_0new - w_0) <= tolerance:
			w_breakdown = {'engine_total':w_eng_total,
							'avionics':w_avionics,
							'interior':w_interior,
							'wing':w_wing,
							'HT':w_HT,
							'canard':w_c,
							'VT':w_VT,
							'fuselage':w_fuse,
							'surface_control':w_surfcont,
							'fuel_control':w_fuelcontrol,
							'indicators':w_indicators,
							'nose_gear':w_nose_gear,
							'main_gear':w_main_gear,
							'misc':w_miscfurnish,
							'electronics':w_elec 
							}
			return w_0, plane
				
		w_0 += 1.00*(w_0new - w_0)
		# w_0 += 0.5*(w_0new - w_0)
		# print 'w_0', w_0
	
	# print('CL ', CL, 'CD0', CD0, ' w_0/Sref_wing ',  w_0/Sref_wing)
	# print w_nose_gear, 2*w_main_gear, w_xtra
	# print w_fuse+w_xtra



	# print w_breakdown
	# print plane.AR, 'carichner', Wwing_carichner, 'raymer', Wwing_raymer ,w_0, w_f

	return w_0, w_f, w_breakdown

if __name__ == '__main__':

	# import numpy as np 
	# import constants as plane
	# import constantsG550
	import j481

	w_0, w_f, w_other = prelim_weight(j481.Sref, j481.thrust_req, j481)
	quit()


	# CD = calcCD(plane.C_f, plane.Swet_rest*10.7639 + 2.0*plane.Sref, plane.Sref,  plane.CL['cruise'], plane.e['cruise'], plane.AR )
	# ff = fuel_fraction(plane.SFC, CD, plane.R, plane.speed_kts, plane.CL['cruise'])
	# print ff
	# changeSref(plane, plane.S_wing, plane.Sref_c*10.7639)
	# # changeCSref(plane, constants.Sref_c*10.7639)

	# # print constants.S_wing, constants.Sref_c

	# w_0, w_f, w_other = prelim_weight(plane.S_wing, plane.thrust_req, plane)

	# print 'J481: w_0',w_0 , 'w_f', w_f, 'empty', w_0-w_f-constants.w_payload

	# print 'fuselage:', w_other['fuselage']+w_other['interior']+w_other['indicators']+w_other['misc']+w_other['electronics']+w_other['avionics']
	# print 'wing:', w_other['wing']+w_other['surface_control']+w_other['fuel_control']
	# print 'HT:', w_other['HT']
	# print 'VT:', w_other['VT']
	# print 'canard:', w_other['canard']
	# print 'landing gears', w_other['main_gear'], w_other['nose_gear']
	# print 'engine(x2):', w_other['engine_total']

	# w_0, w_f, _ = prelim_weight(constantsG550.Sref*10.7639, constantsG550.thrust_req, constantsG550)

	# print 'G550: w_0',w_0 , 'w_f', w_f

	# n = 10.0
	# Sref_wing = plane.S_wing
	# T0 = plane.thrust_req
	# w_0, _, _, w_crew_payload = Weight.weight_estimation.calcWeights(plane.R,plane.L_D, plane.SFC, plane.machCruise, plane.w_payload)
	# CD0 = plane.C_f*(plane.Swet_rest + 2.0*Sref_wing)/Sref_wing
	# CL = np.sqrt(CD0*np.pi*plane.AR*plane.e['cruise'])
	# # print 'CL original '+str(CL)
	# CD = CD0 + CL**2/(np.pi*plane.AR*plane.e['cruise'])
	# ff = fuel_fraction(plane.SFC, CD, plane.R, plane.speed_kts, CL)
	# # ff_step = fuel_fraction_update(plane.SFC, plane.SFC_sealevel, Sref_wing, T0, w_0, CD0, plane.alt, plane.ceiling, plane.speed_kts, plane.rho_imperial, plane.R, 1.0/(np.pi*plane.AR*plane.e['cruise']), n)
	# print 'originial '+str(ff)
	# print 'stepped '+str(ff_step)
	
