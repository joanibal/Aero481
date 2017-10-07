import os,sys,inspect

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from climb_constraints import *
from constants import *

from Aerodynamics.calcDragPolar import DragPolar

import numpy as np
import matplotlib.pyplot as plt
from Aerodynamics.calcDragPolar import DragPolar
#import C_d0 and K data
C_d0_clean, C_d0_takeoff_flaps_gear_down, C_d0_takeoff_flaps_gear_up, C_d0_landing_flaps_gear_down, C_d0_landing_flaps_gear_up, k_clean, k_takeoff, k_landing = DragPolar()

#sorting data into arrays for each stage
#order of climbs: TO, transition seg, 2nd seg, enroute, balked landing, balked landing (OEI)
#used in calculating T/W (uncorrected)
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
    TW = TWcalc(CL_max[i], C_d0_array[i], ks_array[i], K_array[i], G_array[i])
    # print TW
    TW_corrected = TWcorrection(thrust_mod_array[i], eng_mod_array[i], CTOL_mod_array[i], TW)
    # print TW_corrected
    # print TW, TW_corrected

    TW_array = np.append(TW_array,TW)
    # print(np.size(TW_corrected_array))
    TW_corrected_array[i] = TW_corrected
    # np.append(TW_corrected_array, TW_corrected)

# print TW_array

# Cd_0 = 0.01597
# Cd_0_climb = 0.01597
N = 10000
W_S = np.linspace(0, 350, N)
# CL_max = 2.5

# crusie 
T_W_cruise = 1.0/(0.2826**0.6)*(228.8*0.01597)/W_S + (W_S)*1/(228.8*np.pi)


# Ceiling 
T_W_ceiling = 1/(Density_Ceilng/Density_SL )**0.6 * ( 0.001 + 2*np.sqrt(Cd_0['cruise']/(np.pi*9.8*0.85)))  

# T_W = k**2/CL_max*Cd_0_climb + CL_max/(k**2 * np.pi * )
numEngines/(numEngines - 1)

#takeoff 
T_W_Takeoff = W_S/(1*CL_max[0]* 4948/37.5)


# landing
W_S_landing = (runLength/1.6 - 00)*CL_max[4]*1/80.0 
print W_S_landing







ceiling, = plt.plot(W_S, np.ones(N)*T_W_ceiling, label='Ceiling')
cruise, = plt.plot(W_S, T_W_cruise, label='Cruise')
takeoff, = plt.plot(W_S, T_W_Takeoff, label='Takeoff')
A = []

for i in range(0,6):
	A.append(plt.plot(W_S, np.ones(np.shape(W_S))*TW_corrected_array[i],'--', label=('Climb '+str(i+1))))

landing, = plt.plot([W_S_landing, W_S_landing], [ 0, 1], label='Landing')

a = np.logical_and(T_W_cruise>=TW_corrected_array[5], T_W_Takeoff<=TW_corrected_array[5])
b = np.logical_and(np.logical_not(a), T_W_Takeoff<=TW_corrected_array[5])
c = np.logical_and(T_W_Takeoff>=TW_corrected_array[5], W_S<=W_S_landing)

plt.fill_between(W_S,T_W_cruise,1,where=a     ,interpolate=True, color='b')
plt.fill_between(W_S,np.ones(np.shape(W_S))*TW_corrected_array[5],1,where=b,interpolate=True, color='b')
plt.fill_between(W_S,T_W_Takeoff,1,where=c,interpolate=True, color='b')

plt.axis((W_S[0], W_S[-1], 0, 1))	

plt.legend(handles=[ceiling, cruise, takeoff, landing, A[0][0], A[1][0], A[2][0], A[3][0], A[4][0], A[5][0]])
plt.legend(loc = 'upper right')

plt.ylabel('T/W')
plt.xlabel('W/S')
# plt.title('')
plt.show()
