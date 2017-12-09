

import numpy as np
import math

runLength = 4948   							# ft
alt = 53000       							# ft
R = 5200           							# nMi
machCruise = 0.85
SFC = 0.725      							# 1/hr
SFC_sealevel = 0.346                        # 1/hr
L_D = 15 									#used in weight_estimation
speed_kts = 566.7279

#W = MTOW*9.81                               # Lift equals weight
M = 0.85                                    # Cruise Mach numnber
T_C = -56.5                                 # Temperature (Celcius)
T = T_C + 273.15                            # Temperature (Kelvin)
p = 18822.69                                # Absolute Pressure (Pa)
gasConst = 287                                     # Gas Constant (J/kgK)
rho = p/(gasConst*T)                               # Air Density (kg/m^3)
# print rho
a = math.sqrt(1.4*gasConst*T)                      # Speed of Sound (m/s)
u = M*a                                     # Airspeed (m/s)
rho_imperial = rho*0.00194032               # Conversion from kg/m^3 to slugs/ft^3
u_imperial = u*3.28084                      # Conversion from m/s to ft/s
q = 0.5*rho_imperial*u_imperial**2          # Dynamic Pressure (imperial)

#print q, rho_imperial, u_imperial
#quit()

# print(str(q))
w_crew = 3.0*(180+60)       #lbs (crew weight + luggage)
w_payload = 8.0*(180+60) + w_crew    #lbs (passenger weight + luggage)

# G550 specs
# machCruise = 0.8
# SFC = 0.65 # 1/hr
# L_D = 18
# R = 6750 # nmi

numEngines = 2
engine_thrust = 7760 #lbs - sealevel


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

# ceiling = 60000     						# ft
T_Ceiling = 216.650  						# K
# mu = 2.995e-7*47.88026
mu_cruise = 1.422-7    #N s/m2

# T_SL
P_Ceiling = 11053.0  						# Pa
# P_SL

Density_Ceiling = 0.1164     				# kg/M^3
Density_SL  = 1.225       					# kg/M^3
Density_Cruise = 0.154                      # 53000 ft
a_Ceiling = 573.57          				# knots
cruise_steps = 1                            # number of altitude levels for cruise
# cruise_max_alt = alt+cruise_steps*2000.0

CL= {
    'max': {
    'takeoff': 2.0,
    'cruise':  1.3,
    'landing': 2.6,
    'balked landing': 2.6*0.85,
    },
    'cruise': 0.57
    }

# Empennage Constants
c_VT =  0.041
c_HT = 0.66

# Horizontal Stabilizer Properties
L_HT = 8.68								# m
c_root_HT = 2.0							# m
taper_HT = 0.35
span_h = 25.197                             # ft
t_root_h = 0.9251                           # ft
sweep_HT = 36 * 0.0174533                    # deg

# Canard Properties
L_c = 12.7 								# m
Sref_c = 6								# m^2
c_root_c = 1.35 								# m
taper_c = 0.25
Sref_c_actual = 130/10.7639                 # m^2
t_root_c = 0.837                            # ft
span_c = 26.06                              # ft
sweep_c = 31.0 * 0.0174533                  # rad
AR_c = span_c**2/Sref_c_actual

# Vertical Stabilizer Properties
c_root_VT = 4       						# m
taper_VT = 0.8							# vertical tail taper ratiop
sweep_VT = 0.628319							# radians (36 degrees)
L_VT = 6.35                                 # m
Arudder = 43.09                             # ft^2

# Wing Properties
#Sref = 127.59 								# m^2 (wing area)
#b = 33.89 									# m (span)
#c_root = 9.41 								# m
#w_lambda = 0.26 							# main wing taper ratio


# Fuselage Properties
fuse_length = 83.77*0.3048 					# m
Swet_fuse = 1975.14 #ft^2



# # A/C Properties
# CGpos = 63.97*0.3048						# m (This is used in SVT calculations)
# CG = 0.4*fuse_length 						# m
# static_margin = 0.15

# Wing Properties
# Sref = 950.0 * 0.09203 #m^2 (wing area)
S_wing = 865.5  # ft^2 Wing area
Sref = 950 #ft^2 (Referance area)

b = (46.23310*2 )/3.28084#m (span)
c_root = 15.56581025 /3.28084#m
w_lambda = 0.26 #(taper ratio
c_MAC = 2.0/3.0*c_root*(1.0+w_lambda+w_lambda**2)/(1.0+w_lambda)
# print(c_MAC)
y_MAC = b/6.0*(1.0+2.0*w_lambda)/(1.0+w_lambda)
AR = 9
tc = 0.12
sweep = 36*0.0174533
wing_mounted_area = 132.8011*2      #ft
nacelle_length = 12.5               #ft
inlet_area = 8.73                   #ft^2
nacelle_wettedarea = 315.789/2      #ft
cabinpressure = 11.8                #psi


# print c_MAC, y_MAC

# Properties exclusing wings
Swet_rest = 307.1091*10.7639 #ft^2
C_f = 0.0030 #Skin-friction coefficient based on equivalent skin-friction coefficients

v_landingstall = 143.977436581 #ft/s

# design point
thrust_req = engine_thrust*numEngines #lbs

#landing gear
wheels_nose = 2
wheels_main = 4
nose_x = 180.0*0.0254           #m (from datum at nose)
main_x = 20.7249521             #m (from datum at nose)

# A/C mass properties (datum at nose)
np_location = 16.66     #m
cg_fwd = 15             #m (chosen because forward cg can be modified based on fuel placement)
cg_aft = 16.07          #empty CG location
cg_h = 2.50        #m

N = 4.5
sweep_half = math.atan((0.5*b*math.tan(sweep)-0.25*c_root + 0.25*w_lambda*c_root)/(0.5*b))
Keco = 0.686
Npil = 2  #number of pilots
Npass = 8  #number of passengers
Natt = 1  #number of attendants

jetA_density = 6.71 #lb/gal

# Rkva = 50
# La = fuse_length
# Ngen = numEngines

surfaces = {
            'fuselage':{
                        'charLeng':101.17, #ft
                        'diameter':8.8,  # ft
                        'interfernceFactor': 1.0,
                        'swet':2323.66 ,#ft^2
                        'sweep': 0  ,# rad
                        'fracLaminar': 0.1,
                        'finish': 'smoothPaint'
                    },
            'wing':{
                        'charLeng':3.17, #ft
                        't/c':0.093,
                        'Xmaxt/c':.4,
                        'interfernceFactor': 1.0,
                        'swet': 1333 ,#ft^2
                        'sweep': sweep  ,# rad
                        'fracLaminar': 0.35,
                        'finish': 'polishedSM'
                        },
            'vTail':{
                        'charLeng':11.407, #ft
                        't/c':0.093,
                        'Xmaxt/c':.4,
                        'interfernceFactor': 1.0,
                        'swet': 252.18 ,#ft^2
                        'sweep': sweep_VT  ,# rad
                        'fracLaminar': 0.35,
                        'finish': 'smoothPaint'
                    },
            'hTail':{
                        'charLeng':11.407,
                        't/c':0.093,
                        'Xmaxt/c':.4,
                        'interfernceFactor': 1.0,
                        'swet': 216.24 ,#ft^2
                        'sweep': sweep_HT  ,# rad
                        'fracLaminar': 0.35,
                        'finish': 'polishedSM'
                    },
            'canard':{
                        'charLeng':11.407,
                        't/c':0.093,
                        'Xmaxt/c':.4,
                        'interfernceFactor': 1.0,
                        'swet': 267.4, #ft^2.
                        'sweep': sweep_c  ,# rad
                        'fracLaminar': 0.35,
                        'finish': 'polishedSM'

                        },
            'nacelle':{
                        'charLeng':12.5,
                        'diameter':4.83,
                        'interfernceFactor': 1.0,
                        'swet': 215.58, #ft^2,
                        'sweep': 0,
                        'fracLaminar': 0.1,
                        'finish': 'smoothPaint'
                        }

            }

# cg locations referenced from tip of nose
cg_locations = {'wing':60.0,                
                'HT':105.0117,
                'canard':13.5491,
                'VT':93.7585,
                'fuselage':40.48,
                'main_gear':54.4441,
                'nose_gear':13.4351,
                'propulsion':70.4627}

cg_additional = {'fuel_control':cg_locations['wing'],
                'start_systems':cg_locations['propulsion'],
                'surface_control':cg_locations['wing'],
                'instruments':cg_locations['fuselage'],
                'furnishings':cg_locations['fuselage'],
                'avionics':cg_locations['fuselage'],
                'electronics':cg_locations['fuselage']}




            
# [[  5.          10.9592      39.8333      58.13695556]
#  [  0.           2.           3.          46.23310502]
#  [ -2.16535     -2.16535     -2.16535     -2.75591   ]
#  [ 61.          51.21        13.6482944    3.54855654]
#  [  5.           5.           0.           0.        ]
#  [  2.           2.           9.           9.        ]
# #  [  3.           3.          -2.          -2.        ]]
# print np.tan(sweep)*(b/2*3.28084 - 3)
# print np.tan(sweep), (b/2*3.28084 - 3)


Xle = np.array([  5.0 ,    10.9592  ,  39.8333  , 39.8333 + np.tan(sweep)*(b/2*3.28084 - 3) ])
Yle = np.array([0,       2,        3,    b/2*3.28084])
Zle = np.array([-2.16535, -2.16535, -2.16535,   -2.75591])
C =   np.array([61,  51.21,  c_root*3.28084, c_root*3.28084*w_lambda])
incAng = np.array([5, 5, 2, 0 ])
Nspan = np.array([3, 3, 9, 9])
Sspace = np.array([3, 3, -2, -2])
AFILE = np.array(['naca0008.dat', 'naca0008.dat', 'sc20612-il.dat', 'sc20612-il.dat'])

wing= (np.vstack((Xle, Yle, Zle, C, incAng, Nspan, Sspace))).T
# print 'consts'
# print wing.T
# quit()
# print 39.8333 + c_root/4
# #    
# Xle = np.array([5,       10.9592,  39.27,   69.91948])
# Yle = np.array([0,       2,        3,    b/2])
# print b/2
# Zle = np.array([-2.16535, -2.16535, -2.16535,   -2.75591])
# C =   np.array([61,  51.21,  c_root*3.28084,   c_root*3.28084*w_lambda])
# incAng = np.array([5, 5, 0, 0 ])
# Nspan = np.array([2, 2, 9, 9])
# Sspace = np.array([3, 3, 3, 3])
# AFILE = np.array(['naca0008.dat', 'naca0008.dat', 'sc20612-il.dat', 'sc20612-il.dat'])

# wing= np.vstack((Xle, Yle, Zle, C, incAng, Nspan, Sspace)).T




# Xle = np.array([41.8333,   75.4948])
# Yle = np.array([     0,    46.0302])
# Zle = np.array([ -2.16535,   -2.75591])
# C =   np.array([ 15.0591,   4.22244])
# incAng = np.array([0, 0 ])
# Nspan = np.array([60, 60])
# Sspace = np.array([3, 3])
# AFILE = np.array(['sc20612-il.dat', 'sc20612-il.dat'])

# wing= np.vstack((Xle, Yle, Zle, C, incAng, Nspan, Sspace)).T



# [[  8.98        13.26634767]
#  [  0.          13.03      ]
#  [ -0.75        -0.75      ]
#  [  4.429134     1.1072835 ]
#  [  2.           2.        ]
#  [  6.           6.        ]
#  [  3.           3.        ]]




Xle_c = np.array([8.98, 13.2663])
Yle_c = np.array([0.0, 13.03])
Zle_c = np.array([-.75, -0.75])
C_c = np.array([  4.429134   ,  1.1072835 ])
incAng_c = np.array([2, 2])
Nspan_c = np.array([6, 6])
Sspace_c = np.array([3, 3])
AFILE_c = np.array(['sc20612-il.dat', 'sc20612-il.dat'])

canard= np.vstack((Xle_c, Yle_c, Zle_c,  C_c, incAng_c, Nspan_c, Sspace_c)).T

cg = [51.44619, 0, 0]
