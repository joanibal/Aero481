#Constants file for Gulfstream G650

#Basic Parameters (from student guide)
maxPax = 19
nAttendants = 1
nPilots = 2
nPax = 8
R = 6750									#n-mi
machCruise = 0.80
L_D = 18
max_Thrust = 15385							#lbs
AR = 7.4						
maxTL = 0.83								#Ratio of maximum takeoff to landing weight
MTOW = 91000								#lbs
runLength = 2770							#Feet
Sref = 1140
CL_max_takeoff = 1.8
CL_max_landing = 2.1

alt = 40000       							# Estimated Cruise Altitude (ft)
SFC = 0.65       							# 1/hr
numEngines = 2

e = {'takeoff':{'gearUp':0.775, 'geardown':0775}, 'cruise':0.835, 'landing':{'gearUp':0.725,'geardown':0.725}}

cd_0 = {'takeoff':{'gearUp':0.0400, 'geardown':0.0600}, 'cruise':0.0250, 'landing':{'gearUp':0.0850, 'geardown':0.1050}}

ceiling = 51000     						#ft
T_Ceiling = 216.650  						# K
# T_SL
P_Ceiling = 11053.0  						# Pa
# P_SL

Density_Ceilng = 0.178     					# kg/M^3
Density_SL  = 1.225       					# kg/M^3
a_Ceiling = 573.57          				# knots