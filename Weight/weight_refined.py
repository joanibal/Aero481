import os,sys,inspect

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import Sizing.horizontal_surf_sizing
from Aerodynamics.calcCoeff import *
import Sizing.Svt_calc
import Weight.weight_estimation
import numpy as np
import matplotlib.pyplot as plt
import constants as consts

# wing weight calculations
Wt_carichner = (0.00428*consts.Sref_wing**0.48)*((consts.AR*consts.M**0.43)/(100*consts.tc)**0.76)*((MTOW*consts.N)**0.84*consts.w_lambda**0.14)/(np.cos(consts.lambda_half)**1.54)

#horizontal tail calc
gamma_tail = ((MTOW*consts.N)**0.813)*(consts.S_HT**0.584)*((consts.span_h/consts.t_root_h)**0.033)*()

#canard calc

#vertical tail

#fuselage

#landing gear
W_gear = 62.21*(MTOW*(10**(-3)))**0.84

#propulsion
	#cowl/duct
W_bladder = 23.10*((fuelweight)*10**(-2))**0.758	#bladder cells
W_bladdersupport = 7.91*((fuelweight)*10**(-2))**0.854	#bladder cells supports
W_dumpdrain = 7.38*((fuelweight)*10**(-2))**0.458	#dump and drain
W_cgcontrol = 28.38*((fuelweight)*10**(-2))**0.442	#cg control system

#engine controls
W_engcontrol = consts.Keco*(consts.fuse_length/0.3048*consts.numEngines)**0.792

#starting systems
W_start_cp = 9.33*(numEngines*weight_eng*10**(-3))**1.078	#cartridge/pneumatic
W_start_elec = 38.93*(numEngines*weight_eng*10**(-3))**0.918	#electrical

#surface controls

#instruments
W_flightind = Npil*(15+0.032*(MTOW*10**(-3)))	#flight indicators
W_engineind = numEngines*(4.80+0.006*(MTOW*10**(-3)))	#engine indicators
W_miscind = 0.15*(MTOW*10**(-3))	#misc indicators

#electrical system

#furnishings
W_flightdeck = 54.99*Npil	#flight deck seats
W_passseats = 32.03*Npass	#passenger seats
W_lav = 3.90*(Npass**1.33)	#lavatories
W_food = 5.68*(Npass**1.12)	#food
W_oxygen = 7*(Npil+Npass+Natt)**0.702	#oxygen
	#windows
W_baggage = 0.0646*Npass**1.456	#baggage
W_miscfurnish = 0.771*(MTOW*10**(-3))	#misc
	#air conditioning

#avionics
