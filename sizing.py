from constants import *
import numpy as np
import matplotlib.pyplot as plt
from calcDragPolar import DragPolar
from climb_constraints import *
#import C_d0 and K data
C_d0_clean, C_d0_takeoff_flaps_gear_down, C_d0_takeoff_flaps_gear_up, C_d0_landing_flaps_gear_down, C_d0_landing_flaps_gear_up, k_clean, k_takeoff, k_landing = DragPolar()

#sorting data into arrays for each stage
#order of climbs: TO, transition seg, 2nd seg, enroute, balked landing, balked landing (OEI)
#used in calculating T/W (uncorrected)
CL_max_array = np.array([1.8, 1.8, 1.8, 1.2, 2.0, 2.0*0.85]) #based on Roskam
C_d0_array = np.array([C_d0_takeoff_flaps_gear_up, C_d0_takeoff_flaps_gear_down, C_d0_takeoff_flaps_gear_up, C_d0_clean, C_d0_landing_flaps_gear_down, (C_d0_landing_flaps_gear_down+C_d0_takeoff_flaps_gear_down)/2])
ks_array = np.array([1.2, 1.15, 1.2, 1.25, 1.3, 1.5])
K_array = np.array([k_takeoff, k_takeoff, k_takeoff, k_clean, k_landing, k_landing])
G_array = np.array([0.012, 0.00, 0.024, 0.012, 0.032, 0.021])

#used in calculating T/W (corrected), 0-1 indicate condition active or not
thrust_mod_array = np.array([0, 0, 0, 1, 1, 1])
eng_mod_array = np.array([1, 1, 1, 1, 0, 1])
CTOL_mod_array = np.array([0, 0, 0, 0, 1, 1])

#preallocation
TW_array = np.empty([6,6])


TW_corrected_array = np.empty([6,1])
#calculating uncorrected climb
for i in range(0,6):
    TW = TWcalc(CL_max_array[i], C_d0_array[i], ks_array[i], K_array[i], G_array[i])
    # print TW
    TW_corrected = TWcorrection(thrust_mod_array[i], eng_mod_array[i], CTOL_mod_array[i], TW)
    # print TW_corrected
    # print TW, TW_corrected

    TW_array = np.append(TW_array,TW)
    # print(np.size(TW_corrected_array))
    TW_corrected_array[i] = TW_corrected
    # np.append(TW_corrected_array, TW_corrected)

# print TW_array

Cd_0 = 0.01597
Cd_0_climb = 0.01597
N = 100
W_S = np.linspace(0, 350, N)
CL_max = 2.5

# crusie 
T_W_cruise = 1.0/(0.2826**0.6)*(228.8*0.01597)/W_S + (W_S)*1/(228.8*np.pi)


# Ceiling 
T_W_ceiling = 1/(Density_Ceilng/Density_SL )**0.6 * ( 0.001 + 2*np.sqrt(Cd_0['cruise']/(np.pi*9.8*0.85)))  

# T_W = k**2/CL_max*Cd_0_climb + CL_max/(k**2 * np.pi * )
numEngines/(numEngines - 1)

#takeoff 
T_W_Takeoff = W_S/(1*CL_max* 4948/37.5)

plt.plot(W_S, np.ones(N)*T_W_ceiling, 'r--')
plt.plot(W_S, T_W_cruise, 'r--')
plt.plot(W_S, T_W_Takeoff, 'g--')
plt.show()
