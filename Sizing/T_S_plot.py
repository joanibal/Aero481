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


itermax = 100
T_guess = 4400
S = np.linspace(400, 350, 10)
T = np.empty(len(S))
w_0 = calcWeights((5000+200),15, 0.657)[0]	 # [0] <-- only use the first 


CD0, k = DragPolar(w_0)[0:2] # [0:2] <-- only use the first two ouputs 




contraints = {
		'Ceilling': 'ceilling',
		'Cruise': 'cruise',
		'Lanidng': 'lanidng',
		'Climb':['takeoff climb', 'trans seg climb', '2nd seg climb', 'enroute climb', 'balked climb AEO', 'balked climb OEI'],
		'Takeoff': 'takeoff',
}

thrustCon = {
		'Ceilling': np.ones(len(S))*T_guess,
		'Cruise': np.ones(len(S))*T_guess,
		'Lanidng': np.ones(len(S))*T_guess,
		'Climb':{'takeoff climb': np.ones(len(S))*T_guess,
				'trans seg climb':  np.ones(len(S))*T_guess,
				'2nd seg climb':  np.ones(len(S))*T_guess,
				'enroute climb': np.ones(len(S))*T_guess,
				'balked climb AEO': np.ones(len(S))*T_guess,
				'balked climb OEI': np.ones(len(S))*T_guess},
		'Takeoff': np.ones(len(S))*T_guess
			}


tolerance = 0.1
T_upper = 36000
T_lower = 0 


for i in range(len(S)):
	for flightCond in contraints.keys():
		notconverged = True


		if flightCond == 'Climb':
			for climbCond in contraints[flightCond]:
				for j in range(itermax):
					W = prelim_weight(S[i] , thrustCon['Climb'][climbCond][i])
					# W_S = W/S[i]

					CD0, k = DragPolar(W)[0:2] # [0:2] <-- only use the first two ouputs 

					T_W_climb = calcTWClimb(consts.CL['max'], CD0, k, consts.numEngines)[climbCond]

					T_climb_new = T_W_climb*W
					print(flightCond + " " + climbCond + " " +  str(i) + " " + str(np.abs(T_climb_new - thrustCon['Climb'][climbCond][i])))
					if np.abs(T_climb_new - thrustCon['Climb'][climbCond][i]) <= tolerance:
						notconverged = False
						break

					thrustCon['Climb'][climbCond][i] = T_climb_new

				if notconverged:
					raise ValueError(flightCond + ' ' + climbCond + ' didnt converge')

		elif flightCond == 'Ceilng':
			for j in range(itermax):
				W = prelim_weight(S[i] , thrustCon[flightCond][i])
				W_S = W/S[i]

				CD0, k = DragPolar(W)[0:2] # [0:2] <-- only use the first two ouputs 

				T_W_climb = calcTWCeilng(desCeilng_to_densSL, CDO['cruise'])

				T_climb_new = T_W_climb*W
				print(flightCond + " " +   str(i) + " " + str(np.abs(T_climb_new - thrustCon[flightCond][i])))
				if np.abs(T_climb_new - thrustCon[flightCond][i]) <= tolerance:
					notconverged = False
					break

				thrustCon[flightCond][i] = T_climb_new

			if notconverged:
				raise ValueError(flightCond + ' didnt converge')


		elif flightCond == 'Cruise':
			for j in range(itermax):
				W = prelim_weight(S[i] , thrustCon[flightCond][i])
				W_S = W/S[i]


				T_W_climb = calcTWCruise(W_S)

				T_climb_new = T_W_climb*W
				print(flightCond + " " +   str(i) + " " + str(np.abs(T_climb_new - thrustCon[flightCond][i])))
				if np.abs(T_climb_new - thrustCon[flightCond][i]) <= tolerance:
					notconverged = False
					break

				thrustCon[flightCond][i] = T_climb_new

			if notconverged:
				raise ValueError(flightCond + ' didnt converge')


		elif flightCond == 'Takeoff':
			for j in range(itermax):
				W = prelim_weight(S[i] , thrustCon[flightCond][i])
				W_S = W/S[i]


				T_W_climb = calcTWTakeoff(W_S, consts.CL['max']['cruise'])

				T_climb_new = T_W_climb*W
				print(flightCond + " " +   str(i) + " " + str(np.abs(T_climb_new - thrustCon[flightCond][i])))
				if np.abs(T_climb_new - thrustCon[flightCond][i]) <= tolerance:
					notconverged = False
					break

				thrustCon[flightCond][i] = T_climb_new

			if notconverged:
				raise ValueError(flightCond + ' didnt converge')




		elif flightCond == 'Landing':
			for j in range(itermax):
				thrustCon[flightCond][i] = (T_upper + T_lower)/2

				W = prelim_weight(S[i] , thrustCon[flightCond][i])
				W_S = W/S[i]

				diff_W_S = W_S - W_S_landing;
				# binary search
				
				print(str(i) + " " + str((diff_W_S)))

				if np.abs(diff_W_S) <= tolerance:
						notconverged = False
						break


				elif diff_W_S > 0:
						T_upper = thrustCon[flightCond][i]
				else:
						T_lower = thrustCon[flightCond][i]


			if notconverged:
				raise ValueError(flightCond + ' didnt converge')







# pdb.set_trace()


plt.plot(S, thrustCon['Cruise'])
plt.plot(S, thrustCon['Ceilling'])
plt.plot(S, thrustCon['Lanidng'])
plt.plot(S, thrustCon['Takeoff'])
for climbCond in contraints['Climb']:
	plt.plot(S, thrustCon['Climb'][climbCond])


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








