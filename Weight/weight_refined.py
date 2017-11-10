import os,sys,inspect

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import Sizing.horizontal_surf_sizing as hs
from Aerodynamics.calcCoeff import *
import Sizing.Svt_calc
import Weight.weight_estimation
import numpy as np
import matplotlib.pyplot as plt
import constants as consts

# wing weight calculations
Wwing_carichner = (0.00428*Sref_wing**0.48)*((consts.AR*consts.M**0.43)/(100*consts.tc)**0.76)*((MTOW*consts.N)**0.84*consts.w_lambda**0.14)/(np.cos(consts.lambda_half)**1.54)
Wwing_raymer = 0.0051*((MTOW*consts.N)**0.557)*(Sref_wing**0.649)*(consts.AR**0.5)*(consts.tc**(-0.4))*((1+w_lambda)**0.1)*(math.cos(consts.sweep)**(-1))*(consts.wing_mounted_area**0.1)

#horizontal tail calc
gamma_horiz = ((MTOW*consts.N)**0.813)*((hs.S_HT*10.7639)**0.584)*((consts.span_h/consts.t_root_h)**0.033)*((consts.c_MAC/0.3048)/consts.L_HT)**0.28
W_horiz = 0.0034*gamma_horiz**0.915

#canard calc
gamma_canard = ((MTOW*consts.N)**0.813)*((consts.Sref_c_actual*10.7639)**0.584)*((consts.span_c/consts.t_root_c)**0.033)*((consts.c_MAC/0.3048)/consts.L_c)**0.28
W_horiz = 0.0034*gamma_canard**0.915

#vertical tail
gamma_vert = ((1+1)**0.5)*((MTOW*consts.N)**0.363)*(hs.S_VT**1.089)*(consts.M**0.601)*(hs.L_VT**(-0.726))*((1+consts.Arudder/hs.S_VT)**0.217)*(AR_VT**0.337)*((1+taper_VT)**0.363)*(math.cos(sweep_VT)**(-0.484))
W_vert = 0.19*gamma_vert**1.014

#fuselage
W_fuselage = 10.43*(1.25**1.42)*((consts.q*10**(-2))**0.283)*((MTOW*10**(-3))**0.95)*((consts.fuse_length/8.8)**0.71)

#landing gear
W_gear = 62.21*(MTOW*(10**(-3)))**0.84

#propulsion
W_nacelle = 0.6724*1.017*(consts.nacelle_length**0.1)*(consts.nacelle_width**0.294)*(consts.N**0.119)*(weight_eng**0.611)*(consts.numEngines**0.984)*(consts.nacelle_wettedarea**0.224)	#cowl/duct
W_bladder = 23.10*((fuelweight)*10**(-2))**0.758	#bladder cells
W_bladdersupport = 7.91*((fuelweight)*10**(-2))**0.854	#bladder cells supports
W_dumpdrain = 7.38*((fuelweight)*10**(-2))**0.458	#dump and drain
W_cgcontrol = 28.38*((fuelweight)*10**(-2))**0.442	#cg control system

#engine controls
W_engcontrol = consts.Keco*(consts.fuse_length/0.3048*consts.numEngines)**0.792

#starting systems
W_start_cp = 9.33*(consts.numEngines*weight_eng*10**(-3))**1.078	#cartridge/pneumatic
W_start_elec = 38.93*(consts.numEngines*weight_eng*10**(-3))**0.918	#electrical

#surface controls
W_surfcont = 56.01*(MTOW*consts.q*10**(-5))**0.576

#instruments
W_flightind = consts.Npil*(15+0.032*(MTOW*10**(-3)))	#flight indicators
W_engineind = consts.numEngines*(4.80+0.006*(MTOW*10**(-3)))	#engine indicators
W_miscind = 0.15*(MTOW*10**(-3))	#misc indicators

#avionics
W_avionics = 19.2+11+5+3.5+44+78.4+168.5+14+38.2+37+15.6

#electrical system
W_elec = 1162.66*((W_bladder+W_bladdersupport+W_dumpdrain+W_cgcontrol)*W_avionics*10**(-3))**0.506

#furnishings
W_flightdeck = 54.99*consts.Npil	#flight deck seats
W_passseats = 32.03*consts.Npass	#passenger seats
W_lav = 3.90*(consts.Npass**1.33)	#lavatories
W_food = 5.68*(consts.Npass**1.12)	#food
W_oxygen = 7*(consts.Npil+consts.Npass+consts.Natt)**0.702	#oxygen
W_windows = 109.33*(consts.Npass*(1+cabinpressure)*10**(-2))**0.505	#windows
W_baggage = 0.0646*consts.Npass**1.456	#baggage
W_miscfurnish = 0.771*(MTOW*10**(-3))	#misc
W_ac = 469.30*((45.83*60*(consts.Npil+consts.Natt+consts.Npass)*10**(-4))**0.419)	#air conditioning
