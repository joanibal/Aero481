
import numpy as np

runLength = 4948   							# ft
alt = 40000       							# ft
R = 5200           							# nMi
machCruise = 0.85
SFC = 0.657        							# 1/hr
L_D = 15 									#used in weight_estimation

# G550 specs
# machCruise = 0.8
# SFC = 0.65 # 1/hr
# L_D = 18
# R = 6750 # nmi

numEngines = 2
engine_thrust = 16096.3201 #lbs


e = {'takeoff':{'gearUp':0.775,
                'geardown':0775},
     'cruise':0.835,
     'landing':{'gearUp':0.725,
                'geardown':0.725}}

Cd_0 = {'takeoff':{'gearUp':0.0400,
                'geardown':0.0600},
     'cruise':0.0250,
     'landing':{'gearUp':0.0850,
                'geardown':0.1050}}


# runLength_Denver =
# density_denver =
# density_ceiling =

ceiling = 51000     						# ft
T_Ceiling = 216.650  						# K
# T_SL
P_Ceiling = 11053.0  						# Pa
# P_SL

Density_Ceilng = 0.178     					# kg/M^3
Density_SL  = 1.225       					# kg/M^3
a_Ceiling = 573.57          				# knots

CL_max = np.array([1.8, 1.8, 1.8, 1.2, 2.1, 2.0*0.85]) #based on Roskam
CL_cruise = 0.6657

# Empennage Constants
c_VT =  0.041
c_HT = 1

# Horizontal Stabilizer Properties
L_HT = 14.25 								# m
c_root_HT = 3.5 							# m
taper_HT = 0.41

# Canard Properties
L_c = 16 									# m
Sref_c = 20	 								# m^2
c_root_c = 3.5 								# m
taper_c = 0.25

<<<<<<< HEAD
# Vertical Stabilizer Properties
c_root_VT = 14.5*0.3048						# m
taper_VT = 0.75								# vertical tail taper ratiop
sweep_VT = 0.628319							# radians (36 degrees)

# Wing Properties
Sref = 127.59 								# m^2 (wing area)
b = 33.89 									# m (span)
c_root = 9.41 								# m
w_lambda = 0.26 							# main wing taper ratio

# Fuselage Properties
fuse_length = 105.2*0.3048 					# m
Swet_fuse = 2389.0744993*0.092903 			# m^2

# A/C Properties
CGpos = 63.97*0.3048						# m (This is used in SVT calculations)
CG = 0.4*fuse_length 						# m
static_margin = 0.15
=======
# Wing Properties
Sref = 127.59 #m^2 (wing area)
b = 33.89 #m (span)
c_root = 9.41 #m
w_lambda = 0.26 #(taper ratio
#Fuselage Properties
fuse_length = 105.2 #ft
Swet_fuse = 2389.0744993 #ft^2

#A/C Properties
CG = 0.6*fuse_length #ft
static_margin = 0.15
>>>>>>> e765a24a21dfc9b278eea3a68365db55073268b8

# Properties exclusing wings
Swet_rest = 368 #m^2
C_f = 0.0045 #Skin-friction coefficient based on equivalent skin-friction coefficients
