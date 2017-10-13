# ================== Standard Packages ============================= #
import numpy as np
import matplotlib.pyplot as plt
import os,sys,inspect
import sizing
import pdb
from Weight.weight_buildup import prelim_weight

sys.path.insert(1, os.path.join(sys.path[0], '..'))


# ==================== 481  Packages =============================== #

from climb_constraints import *
from constants import *
from Aerodynamics.calcDragPolar import DragPolar

# =================== Calculations ================================= #
# for i in range(6)



T_guess = 4400
S = np.linspace(100, 350, 10)
T = np.empty(len(S))
T_ceiling = np.empty(len(S))
T_ceiling = np.empty(len(S))

for i in range(len(S)):
	S_0 = S[i]
	T[i] = T_guess
	T_ceiling[i] = T_guess
	T_ceiling[i] = T_guess
	tolerance = 0.1
	converged = True

	while converged :
		W = prelim_weight(S_0 , T[i])
		W_S = W/S_0
		T_W_cruise = 1.0/(0.2826**0.6)*(228.8*0.01597)/W_S + (W_S)*1/(228.8*np.pi)

		T_new = T_W_cruise*W
		print(str(i) + " " + str(np.abs(T_new - T[i])))
		if np.abs(T_new - T[i]) <= tolerance:
			converged = False
	
		T[i] = T_new

	converged = True
	while converged :

		W = prelim_weight(S_0 , T_ceiling[i])
		W_S = W/S_0
		T_W_ceiling = 1/(Density_Ceilng/Density_SL )**0.6 * ( 0.001 + 2*np.sqrt(Cd_0['cruise']/(np.pi*9.8*0.85)))  

		T_ceilng_new = T_W_ceiling*W
		print(str(i) + " " + str(np.abs(T_ceilng_new - T_ceiling[i])))
		if np.abs(T_ceilng_new - T_ceiling[i]) <= tolerance:
			converged = False

		T_ceiling[i] = T_ceilng_new

	while converged :
    
		W = prelim_weight(S_0 , T_ceiling[i])
		W_S = W/S_0
		T_W_ceiling = 1/(Density_Ceilng/Density_SL )**0.6 * ( 0.001 + 2*np.sqrt(Cd_0['cruise']/(np.pi*9.8*0.85)))  

		T_ceilng_new = T_W_ceiling*W
		print(str(i) + " " + str(np.abs(T_ceilng_new - T_ceiling[i])))
		if np.abs(T_ceilng_new - T_ceiling[i]) <= tolerance:
			converged = False

		T_ceiling[i] = T_ceilng_new	
# pdb.set_trace()


print(T)
print(T_Ceiling)

plt.plot(S, T)
plt.plot(S, T_ceiling)
plt.show()







# A = []

# for i in range(0,6):
# 	A.append(plt.plot(W_S, np.ones(np.shape(W_S))*TW_corrected_array[i],'--', label=('Climb '+str(i+1))))

# landing, = plt.plot([W_S_landing, W_S_landing], [ 0, 1], label='Landing')

# a = np.logical_and(T_W_cruise>=TW_corrected_array[5], T_W_Takeoff<=TW_corrected_array[5])
# b = np.logical_and(np.logical_not(a), T_W_Takeoff<=TW_corrected_array[5])
# c = np.logical_and(T_W_Takeoff>=TW_corrected_array[5], W_S<=W_S_landing)

# plt.fill_between(W_S,T_W_cruise,1,where=a     ,interpolate=True, color='b')
# plt.fill_between(W_S,np.ones(np.shape(W_S))*TW_corrected_array[5],1,where=b,interpolate=True, color='b')
# plt.fill_between(W_S,T_W_Takeoff,1,where=c,interpolate=True, color='b')


# # pdb.set_trace()
# plt.axis((W_S[0], W_S[-1], 0, 1))	


# plt.legend([ceiling, cruise, takeoff, landing, A[0][0], A[1][0], A[2][0], A[3][0], A[4][0], A[5][0]],\
#            [ceiling._label, cruise._label, takeoff._label, landing._label, A[0][0]._label, A[1][0]._label, A[2][0]._label, A[3][0]._label, A[4][0]._label, A[5][0]] )

# # plt.legend(handles=[ceiling, cruise, takeoff, landing, A[0][0], A[1][0], A[2][0], A[3][0], A[4][0], A[5][0]])
# plt.legend(loc = 'upper right')

# plt.ylabel('T/W')
# plt.xlabel('W/S')
# # plt.title('')
# plt.show()








