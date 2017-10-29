

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
runLength = 2770							#Feet
Sref = 1140 * 0.09203                       #m^2
CL_max_takeoff = 1.8
CL_max_landing = 2.1
# speed_kts = 566.7279*0.8/0.85

alt = 40000       							# Estimated Cruise Altitude (ft)

# Density_cruise = 0.3025273677;
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