import numpy as np

runLength = 4948   # ft
alt = 40000       # ft
R = 5200           # nMi
machCruise = 0.85
SFC = 0.657        # 1/hr
L_D = 15 			#used in weight_estimation

numEngines = 2


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

ceiling = 51000     # ft
T_Ceiling = 216.650  # K
# T_SL
P_Ceiling = 11053.0  # Pa
# P_SL

Density_Ceilng = 0.178     # kg/M^3
Density_SL  = 1.225       # kg/M^3
a_Ceiling = 573.57          # knots



CL_max = np.array([1.8, 1.8, 1.8, 1.2, 2.1, 2.0*0.85]) #based on Roskam
