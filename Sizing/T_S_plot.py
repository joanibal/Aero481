# ================== Standard Packages ============================= #
import numpy as np
import matplotlib.pyplot as plt
import os,sys,inspect
import pdb
sys.path.insert(1, os.path.join(sys.path[0], '..'))


# ==================== 481  Packages =============================== #

from climb_constraints import *
import constants as consts
from Aerodynamics.calcDragPolar import DragPolar
from Weight.weight_buildup import prelim_weight
from Weight.weight_estimation import calcWeights

from TWconstraints import calcTWCeilng, calcTWClimb, calcTWCruise, calcTWTakeoff, calcWSLanding

# =================== Calculations ================================= #
# for i in range(6)



T_guess = 4400
S = np.linspace(1000, 1400, 10)
T = np.empty(len(S))
w_0 = calcWeights((5000+200),15, 0.657)[0]	 # [0] <-- only use the first 
CD0, k = DragPolar(w_0)[0:2] # [0:2] <-- only use the first two ouputs 


T_ceiling = np.empty(len(S))
T_ceiling = np.empty(len(S))
T_climb1 = np.empty([len(S)])
T_climb2 = np.empty([len(S)])
T_climb3 = np.empty([len(S)])
T_climb4 = np.empty([len(S)])
T_climb5 = np.empty([len(S)])
T_climb6 = np.empty([len(S)])
T_takeoff = np.empty([len(S)])
T_landing = np.empty([len(S)])

for i in range(len(S)):
	# for i in 9:
	# i = 9
	S_0 = S[i]
	T[i] = T_guess
	T_ceiling[i] = T_guess
	T_climb1[i] = T_guess

	T_climb2[i] = T_guess
	T_climb3[i] = T_guess
	T_climb4[i] = T_guess
	T_climb5[i] = T_guess
	T_climb6[i] = T_guess
	T_takeoff[i] = T_guess
	# T_landing[i] = T_guess




	tolerance = 0.1


	notconverged = True

	while notconverged :
		W = prelim_weight(S_0 , T[i])
		W_S = W/S_0
		T_W_cruise = calcTWCruise(W_S)

		T_new = T_W_cruise*W
		print(str(i) + " " + str(np.abs(T_new - T[i])))
		if np.abs(T_new - T[i]) <= tolerance:
			notconverged = False
	
		T[i] = T_new

	notconverged = True
	while notconverged :

		W = prelim_weight(S_0 , T_ceiling[i])
		W_S = W/S_0
		T_W_ceiling = calcTWCeilng(consts.Density_Ceilng/consts.Density_SL, CD0['clean'])

		T_ceiling_new = T_W_ceiling*W
		print(str(i) + " " + str(np.abs(T_ceiling_new - T_ceiling[i])))
		if np.abs(T_ceiling_new - T_ceiling[i]) <= tolerance:
			notconverged = False

		T_ceiling[i] = T_ceiling_new


	notconverged = True
	while notconverged :

		W = prelim_weight(S_0 , T_climb1[i])
		W_S = W/S_0
		T_W_climb1 = calcTWClimb(consts.CL['max'], CD0, k, consts.numEngines)['takeoff climb']

		T_climb1_new = T_W_climb1*W
		print(str(i) + " " + str(np.abs(T_climb1_new - T_climb1[i])))
		if np.abs(T_climb1_new - T_climb1[i]) <= tolerance:
			notconverged = False

		T_climb1[i] = T_climb1_new


	notconverged = True
	while notconverged :

		W = prelim_weight(S_0 , T_climb2[i])
		W_S = W/S_0
		T_W_climb2 = calcTWClimb(consts.CL['max'], CD0, k, consts.numEngines)['trans seg climb']

		T_climb2_new = T_W_climb2*W
		print(str(i) + " " + str(np.abs(T_climb2_new - T_climb2[i])))
		if np.abs(T_climb2_new - T_climb2[i]) <= tolerance:
			notconverged = False

		T_climb2[i] = T_climb2_new

	notconverged = True
	while notconverged :

		W = prelim_weight(S_0 , T_climb3[i])
		W_S = W/S_0
		T_W_climb3 = calcTWClimb(consts.CL['max'], CD0, k, consts.numEngines)['2nd seg climb']

		T_climb3_new = T_W_climb3*W
		print(str(i) + " " + str(np.abs(T_climb3_new - T_climb3[i])))
		if np.abs(T_climb3_new - T_climb3[i]) <= tolerance:
			notconverged = False

		T_climb3[i] = T_climb3_new

	notconverged = True
	while notconverged :

		W = prelim_weight(S_0 , T_climb4[i])
		W_S = W/S_0
		T_W_climb4 = calcTWClimb(consts.CL['max'], CD0, k, consts.numEngines)['enroute climb']

		T_climb4_new = T_W_climb4*W
		print(str(i) + " " + str(np.abs(T_climb4_new - T_climb4[i])))
		if np.abs(T_climb4_new - T_climb4[i]) <= tolerance:
			notconverged = False

		T_climb4[i] = T_climb4_new

	notconverged = True
	while notconverged :

		W = prelim_weight(S_0 , T_climb5[i])
		W_S = W/S_0
		T_W_climb5 = calcTWClimb(consts.CL['max'], CD0, k, consts.numEngines)['balked climb AEO']

		T_climb5_new = T_W_climb5*W
		print(str(i) + " " + str(np.abs(T_climb5_new - T_climb5[i])))
		if np.abs(T_climb5_new - T_climb5[i]) <= tolerance:
			notconverged = False

		T_climb5[i] = T_climb5_new

	notconverged = True
	while notconverged :

		W = prelim_weight(S_0 , T_climb6[i])
		W_S = W/S_0
		T_W_climb6 = calcTWClimb(consts.CL['max'], CD0, k, consts.numEngines)['balked climb OEI']

		T_climb6_new = T_W_climb6*W
		print(str(i) + " " + str(np.abs(T_climb6_new - T_climb6[i])))
		if np.abs(T_climb6_new - T_climb6[i]) <= tolerance:
			notconverged = False

		T_climb6[i] = T_climb6_new


	notconverged = True
	while notconverged :

		W = prelim_weight(S_0 , T_takeoff[i])
		W_S = W/S_0
		T_W_takeoff = calcTWTakeoff(W_S, consts.CL['max']['takeoff'])

		T_takeoff_new = T_W_takeoff*W
		print(str(i) + " " + str(np.abs(T_takeoff_new - T_takeoff[i])))
		if np.abs(T_takeoff_new - T_takeoff[i]) <= tolerance:
			notconverged = False

		T_takeoff[i] = T_takeoff_new


	notconverged = True
	T_upper = 36000
	T_lower = 0 
	W_S_landing = calcWSLanding(consts.runLength, consts.CL['max']['takeoff'])

	while notconverged :

		T_landing[i] = (T_upper + T_lower)/2

		W = prelim_weight(S_0 , T_landing[i])
		W_S = W/S_0

		diff_W_S = W_S - W_S_landing;
		# binary search
		
		print(str(i) + " " + str((diff_W_S)))

		if np.abs(diff_W_S) <= tolerance:
    			break
		elif diff_W_S > 0:
    			T_upper = T_landing[i]
		else:
    			T_lower = T_landing[i]
    					 
    			
		# print(str(i) + " " + str(np.abs(T_landing_new - T_landing[i])))
		# if np.abs(calcWSLanding(runLength, CL_max): - T_landing[i]) 
		# 	notconverged = False

		# T_landing[i] = T_landing_new






# pdb.set_trace()


print(T)
print(T_landing)

plt.plot(S, T)
plt.plot(S, T_ceiling)
plt.plot(S, T_climb1)
plt.plot(S, T_climb2)
plt.plot(S, T_climb3)
plt.plot(S, T_climb4)
plt.plot(S, T_climb5)
plt.plot(S, T_climb6)
plt.plot(S, T_takeoff)
plt.plot(S, T_landing)

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








