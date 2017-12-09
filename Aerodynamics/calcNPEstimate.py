# Estimate the position of the neutral point

import os,sys,inspect

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import numpy as np
import math

import constants
from Sizing.horizontal_surf_sizing import MAC, hor_Sref, hor_surf_prop
from Weight.cg_calculation import cg_location

# Tail parameters
ht_cMAC, ht_yMAC = MAC(constants.c_root, constants.w_lambda, constants.b)
St = hor_Sref(constants.c_HT, ht_cMAC, constants.S_wing*0.092903, constants.L_HT)
Sref_HT = (St*constants.L_HT-\
	constants.L_c*constants.Sref_c)/constants.L_HT	
_, AR_t = hor_surf_prop(Sref_HT, \
	constants.c_root_HT, constants.taper_HT)


def cl_a(AR, eta, sweep, M):
	cl_alpha = 2*math.pi*AR/(2+math.sqrt((AR/eta)**2*(1+math.tan(sweep)**2-M**2)+4))
	return cl_alpha

CL_alpha_canard = cl_a(constants.AR_c, 0.97, constants.sweep_c, constants.M)
CL_alpha_main_wing_0 = cl_a(constants.AR, 0.97, constants.sweep, constants.M)
CL_alpha_tail_0 = cl_a(AR_t, 0.97, constants.sweep, constants.M)

# Assuming wing is affected by downwash of canard
depsilon_dalpha_canard = 2*CL_alpha_canard/(math.pi*constants.AR_c)

# Corrected wing lift curve slope
CL_alpha_main_wing = CL_alpha_main_wing_0*(1 - depsilon_dalpha_canard)*0.9

# Calculate total wing (canard + main wing) lift curve slope
canard_fraction = constants.Sref_c_actual/constants.Sref 	# Percent of canard reference area w.r.t total Sref
CL_alpha_w = CL_alpha_canard*canard_fraction+CL_alpha_main_wing*(1-canard_fraction)

# Calculate total tail lift curve slope
depsilon_dalpha_wing  = 2*CL_alpha_w/(math.pi*constants.AR)
CL_alpha_tail = CL_alpha_tail_0*(1 - depsilon_dalpha_wing)*1	# Little interference with t-tail

# Fuselage contribution
w_f = constants.surfaces['fuselage']['diameter']
L_f = constants.surfaces['fuselage']['charLeng']
w_pos = 55.7175/L_f
#print('Wing Position: ' + str(w_pos))
k_f = 12.008*(w_pos)**4 - 20.018*(w_pos)**3 + 12.846*(w_pos)**2 - 1.9468*(w_pos) + 0.198
#print(k_f)
S_w = constants.surfaces['wing']['swet'] + constants.surfaces['canard']['swet']
MAC = constants.c_MAC

dcmfuselage_dCL = k_f*w_f**2*L_f/(S_w*MAC*CL_alpha_w)
cg_loc, cg = cg_location(constants)


