# Calculate Aircraft Trim Drag

# Python packages
import os,sys,inspect
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import math
import numpy as np
import matplotlib.pyplot as plt

# AERO 481 Packages
import constants
from Sizing.horizontal_surf_sizing import MAC, hor_Sref, hor_surf_prop

# AVL Geometry Information (NEEDS TO BE UPDATED WITH CORRECT VALUES)
x_w = 54.709747						# Main wing NP (ft)
x_tNP = 103.913994					# Horizontal Tail NP (ft)
x_cg = 52.55						# Aircraft CG (ft) - PDR Report number

x = x_tNP-x_w						# Dist. between Tail NP and Main wing NP (ft)
x_t = x_tNP-x_cg					# Dist. between Tail NP and Aircraft CG (ft)

C_Mact = -0.3057					# Aircraft CM minus Tail & Canard (sectional)
C_LW = 0.58							# Aircraft Cruise CL

x_cNP = 14.731684					# Canard NP (ft)
l = x_w-x_cNP						# Dist. between Canard NP and Main wing NP (ft)
l_c = x_cg-x_cNP					# Dist. between Canard NP and Aircraft CG (ft)


# Imported from Constants.py, horizontal_surf_sizing.py
Sref = constants.Sref
wMAC = constants.c_MAC
ht_cMAC, ht_yMAC = MAC(constants.c_root, constants.w_lambda, constants.b)
St = hor_Sref(constants.c_HT, ht_cMAC, constants.Sref, constants.L_HT)
V_HT = constants.c_HT

"""# Calculate fuselage + main wing pitching moment contributions
K_f = 0.0375						# Contribution factor
W_f = 8.8							# Max fuselage width
l_f = 101.2							# Fuselage length
alpha_fuse = 0.01					# Fuselage AoA
CM_fuse = (K_f*W_f**2*l_f*alpha_fuse)/(wMAC*Sref)
print("Fuselage CM: " + str(CM_fuse))"""


# Calculate tail trim drag coefficients
# Origin degined from nose of aircraft
C_Lt = (C_LW*(x_w/Sref)+C_Mact)*(x/(x-x_w))*(1/V_HT)		# Tail lift coefficient				
Sref_HT = (St*constants.L_HT-\
	constants.L_c*constants.Sref_c)/constants.L_HT			# Tail Sref
_, AR_t = hor_surf_prop(Sref_HT, \
	constants.c_root_HT, constants.taper_HT)				# Tail AR
e_t = 1.78*(1-0.045*AR_t**0.68)-0.64						# Tail Oswald efficiency
CD_trim_tail = ((C_Lt**2)/(math.pi*e_t*AR_t))*(St/Sref)		# Tail trim drag
print("Horizontal Trail Trim Drag (C_D):" + str(CD_trim_tail))

#Calculate canard trim drag coefficients
Sref_c = constants.Sref_c*10.7639								# Canard sref (ft^2)
AR_c = (constants.span_c)**2/Sref_c								# Canard AR
C_Lc = (C_LW*(x_w/Sref)+C_Mact)*(l/(l-x_w))*(Sref/Sref_c)		# Canard lift coefficient
e_c = 1.78*(1-0.045*AR_c**0.68)-0.64							# Canard Oswald efficiency
CD_tim_canard = ((C_Lc**2)/(math.pi*e_c*AR_c))*(Sref_c/Sref)	# Canard trim drag
print("Canard Trim Drag (C_D):" + str(CD_tim_canard))