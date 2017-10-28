
import numpy as np
import math

runLength = 4948   							# ft
alt = 40000       							# ft
R = 5200           							# nMi
machCruise = 0.85
SFC = 0.657        							# 1/hr
L_D = 15 									#used in weight_estimation
speed_kts = 566.7279

#W = MTOW*9.81                               # Lift equals weight
M = 0.85                                    # Cruise Mach numnber
T_C = -56.5                                 # Temperature (Celcius)
T = T_C + 273.15                            # Temperature (Kelvin)
p = 18822.69                                # Absolute Pressure (Pa)
gasConst = 287                                     # Gas Constant (J/kgK)
rho = p/(gasConst*T)                               # Air Density (kg/m^3)
a = math.sqrt(1.4*gasConst*T)                      # Speed of Sound (m/s)
u = M*a                                     # Airspeed (m/s)
rho_imperial = rho*0.00194032               # Conversion from kg/m^3 to slugs/ft^3
u_imperial = u*3.28084                      # Conversion from m/s to ft/s
q = 0.5*rho_imperial*u_imperial**2          # Dynamic Pressure (imperial)

# print(str(q))

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

# Cd_0 = {'takeoff':{'gearUp':0.0400,
#                 'geardown':0.0600},
#      'cruise':0.0250,
#      'landing':{'gearUp':0.0850,
#                 'geardown':0.1050}}


# runLength_Denver =
# density_denver =
# density_ceiling =

ceiling = 51000     						# ft
T_Ceiling = 216.650  						# K
# T_SL
P_Ceiling = 11053.0  						# Pa
# P_SL

Density_Ceiling = 0.178     					# kg/M^3
Density_SL  = 1.225       					# kg/M^3
a_Ceiling = 573.57          				# knots


CL= {
    'max': {
    'takeoff': 2.6,
    'cruise':  1.2,
    'landing': 3.0,
    'balked landing': 3.0*0.85,
    },
    'cruise': 0.5
    }

# Empennage Constants
c_VT =  0.041
c_HT = 0.66

# Horizontal Stabilizer Properties
L_HT = 13.25								# m
c_root_HT = 2.35 							# m
taper_HT = 0.41

# Canard Properties
L_c = 16 									# m
Sref_c = 2	 								# m^2
c_root_c = 2 								# m
taper_c = 0.25

# Vertical Stabilizer Properties
c_root_VT = 3.5       						# m
taper_VT = 0.75								# vertical tail taper ratiop
sweep_VT = 0.628319							# radians (36 degrees)
L_VT = 9.75

# Wing Properties
#Sref = 127.59 								# m^2 (wing area)
#b = 33.89 									# m (span)
#c_root = 9.41 								# m
#w_lambda = 0.26 							# main wing taper ratio


# Fuselage Properties
fuse_length = 105.2*0.3048 					# m
Swet_fuse = 2389.0744993 #ft^2

# # A/C Properties
# CGpos = 63.97*0.3048						# m (This is used in SVT calculations)
# CG = 0.4*fuse_length 						# m
# static_margin = 0.15

# Wing Properties
Sref = 950.0 * 0.09203 #m^2 (wing area)
b = 33.89 #m (span)
c_root = 4.95 #m
w_lambda = 0.26 #(taper ratio
c_MAC = 2.0/3.0*c_root*(1.0+w_lambda+w_lambda**2)/(1.0+w_lambda)
y_MAC = b/6.0*(1.0+2.0*w_lambda)/(1.0+w_lambda)
AR = 9

print c_MAC, y_MAC

# Properties exclusing wings
Swet_rest = 368 #m^2
C_f = 0.0045 #Skin-friction coefficient based on equivalent skin-friction coefficients

v_landingstall = 228.9 #ft/s

# design point
thrust_req = 16550 #lbs

#landing gear
wheels_nose = 2
wheels_main = 4
nose_x = 180.0*0.0254           #m (from datum at nose)
main_x = 20.7249521             #m (from datum at nose)

# A/C mass properties (datum at nose)
np_location = 20.09     #m
cg_fwd = 19.0             #m (chosen because forward cg can be modified based on fuel placement)
cg_aft = 19.60          #empty CG location
cg_h = 2.2964764        #m

