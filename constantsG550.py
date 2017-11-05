import numpy as np
import math

#Basic Parameters (from student guide)
maxPax = 19
nAttendants = 1
nPilots = 2
nPax = 8
R = 6750									#n-mi
machCruise = 0.80
L_D = 18							
AR = 7.4									
maxTL = 0.83								#Ratio of maximum takeoff to landing weight
MTOW = 91000								#lbs
runLength = 6000							#Feet
Sref = 1140 * 0.09203                       #m^2
CL_max_takeoff = 1.8
CL_max_landing = 2.1
# speed_kts = 566.7279*0.8/0.85

alt = 40000       							# Estimated Cruise Altitude (ft)

Density_cruise = 0.3025273677;
# T_cruise = 216.65;
# a_cruise = (216.65*1.4*287)**(0.5)
# speed_kts = a_cruise*machCruise*1.94384

# print(speed_kts)
# print(566.7279*0.8/0.85)
speed_kts =562 * 0.868976


engine_thrust = 15385							#lbs
SFC = 0.6414       							# 1/hr
numEngines = 2
thrust_req = engine_thrust*numEngines
C_f = 0.0035 #Skin-friction coefficient based on equivalent skin-friction coefficients

Swet_rest = 5096.18 - 2*Sref/0.09203 #ft^2
Swet_fuse = 1731.70 #ft^2
w_payload = 6500	#lbs (passenger weight + luggage)


e = {'takeoff':{'gearUp':0.775,
                'geardown':0.775},
     'cruise':0.9,
     'landing':{'gearUp':0.725,
                'geardown':0.725}}

c_root = 18.48

S_HT = 244.87* 0.09203  # m^2
S_VT = 140.16* 0.09203  # m^2

Density_Ceiling = 0.17773
Density_SL  = 1.225
Density_Cruise = 0.316406

CL= {
    'max': {
    'takeoff': 2.0,
    'cruise':  0.75,
    'landing': 2.6,
    'balked landing': 1.99
    },
    'cruise': 0.51
    }

M = machCruise                                    # Cruise Mach numnber
T_C = -56.5                                 # Temperature (Celcius)
T = T_C + 273.15                            # Temperature (Kelvin)
p = 19677.3                                # Absolute Pressure (Pa)
gasConst = 287                                     # Gas Constant (J/kgK)
rho = p/(gasConst*T)                               # Air Density (kg/m^3)
a = math.sqrt(1.4*gasConst*T)                      # Speed of Sound (m/s)
u = M*a                                     # Airspeed (m/s)
rho_imperial = rho*0.00194032               # Conversion from kg/m^3 to slugs/ft^3
u_imperial = u*3.28084                      # Conversion from m/s to ft/s
q = 0.5*rho_imperial*u_imperial**2          # Dynamic Pressure (imperial)