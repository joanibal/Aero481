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
from Weight.fuel_weight_curves import fuel_weight
from TWconstraints import calcTWCeiling, calcTWClimb, calcTWCruise, calcTWTakeoff, calcWSLanding

# =================== Calculations ================================= #
# for i in range(6)


itermax = 1000
T_guess = 4400

S = np.linspace(1300, 2000, 10)

# S = np.linspace(400, 751, 10)
W_S_landing = calcWSLanding(consts.runLength,consts.CL['max']['landing'])



contraints = {
		'Ceiling': 'ceiling',
		'Cruise': 'cruise',
		'Landing': 'landing',
		'Climb':['takeoff climb', 'trans seg climb', '2nd seg climb', 'enroute climb', 'balked climb AEO', 'balked climb OEI'],
		'Takeoff': 'takeoff',
}

thrustCon = {
		'Ceiling': np.ones(len(S))*T_guess,
		'Cruise': np.ones(len(S))*T_guess,
		'Landing': np.ones(len(S))*T_guess,
		'Climb':{'takeoff climb': np.ones(len(S))*T_guess,
				'trans seg climb':  np.ones(len(S))*T_guess,
				'2nd seg climb':  np.ones(len(S))*T_guess,
				'enroute climb': np.ones(len(S))*T_guess,
				'balked climb AEO': np.ones(len(S))*T_guess,
				'balked climb OEI': np.ones(len(S))*T_guess},
		'Takeoff': np.ones(len(S))*T_guess
			}


tolerance = 0.1


for i in range(len(S)):
	for flightCond in contraints.keys():
		notconverged = True
		T_upper = 1e3
		T_lower = 0



		if flightCond == 'Climb':
			for climbCond in contraints[flightCond]:
				for j in range(itermax):
					W = prelim_weight(S[i] , thrustCon['Climb'][climbCond][i])[0]
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

		elif flightCond == 'Ceiling':
			for j in range(itermax):
				W = prelim_weight(S[i] , thrustCon[flightCond][i])[0]
				W_S = W/S[i]

				CD0, k = DragPolar(W)[0:2] # [0:2] <-- only use the first two ouputs

				T_W = calcTWCeiling(consts.Density_Ceiling/consts.Density_SL , CD0['clean'])

				T_new = T_W*W
				print(flightCond + " " +   str(i) + " " + str(np.abs(T_new - thrustCon[flightCond][i])))
				if np.abs(T_new - thrustCon[flightCond][i]) <= tolerance:
					notconverged = False
					break

				thrustCon[flightCond][i] = T_new

			if notconverged:
				raise ValueError(flightCond + ' didnt converge')


		elif flightCond == 'Cruise':
			for j in range(itermax):
				W = prelim_weight(S[i] , thrustCon[flightCond][i])[0]
				W_S = W/S[i]

				CD0 = DragPolar(W)[0] # [0:2] <-- only use the first two ouputs

				T_W = calcTWCruise(W_S, CD0['clean'], consts.AR, consts.e['cruise'], consts.q)

				T_new = T_W*W
				print(flightCond + " " +   str(i) + " " + str(np.abs(T_new - thrustCon[flightCond][i])))
				if np.abs(T_new - thrustCon[flightCond][i]) <= tolerance:
					notconverged = False
					break

				thrustCon[flightCond][i] = T_new

			if notconverged:
				raise ValueError(flightCond + ' didnt converge')


		elif flightCond == 'Takeoff':
			for j in range(itermax):
				W = prelim_weight(S[i] , thrustCon[flightCond][i])[0]
				W_S = W/S[i]

				T_W = calcTWTakeoff(W_S, consts.CL['max']['takeoff'], consts.runLength)

				T_new = T_W*W
				print(flightCond + " " +   str(i) + " " + str(np.abs(T_new - thrustCon[flightCond][i])))
				if np.abs(T_new - thrustCon[flightCond][i]) <= tolerance:
					notconverged = False
					break

				thrustCon[flightCond][i] = T_new

			if notconverged:
				raise ValueError(flightCond + ' didnt converge')




		#elif flightCond == 'Landing':
			#for j in range(itermax):
				#thrustCon[flightCond][i] = (T_upper + T_lower)/2

				#W = prelim_weight(S[i] , thrustCon[flightCond][i])[0]
				#W_S = W/S[i]
				#diff_W_S = W_S - W_S_landing;
				# binary search

				#print(str(i) + " " + str((diff_W_S)))

				#if np.abs(diff_W_S) <= tolerance:
					#	notconverged = False
						#break


			#	elif diff_W_S > 0:
				#		T_upper = thrustCon[flightCond][i]
				#else:
					#	T_lower = thrustCon[flightCond][i]


			#if notconverged:
				#raise ValueError(flightCond + ' didnt converge')







# pdb.set_trace()

X, Y, fuel_curves = fuel_weight(S, np.linspace(0, T_guess*20, 10))
# print fuel_curves
# X, Y = np.meshgrid(np.linspace(4000, 30000, 20), np.linspace(750, 1400, 20))
CS = plt.contour(X, Y, fuel_curves, 20,linestyles='dashed', alpha=0.5, label='Fuel Burn')

plt.clabel(CS, CS.levels[0::2])
# cbar = plt.colorbar(CS)
# cbar.ax.set_ylabel('Fuel Weight [lbs]')
# plt.show()


ceiling, = plt.plot(S, thrustCon['Ceiling'], label='Ceiling',linewidth=3.0)
takeoff, = plt.plot(S, thrustCon['Takeoff'], label='Takeoff',linewidth=3.0)
cruise, = plt.plot(S, thrustCon['Cruise'], label='Cruise',linewidth=3.0)
landing, = plt.plot(S, thrustCon['Landing'], label='Landing',linewidth=3.0)

lines = [ceiling, cruise, takeoff, landing]
# lines = [ceiling, cruise, takeoff]

for climbCond in contraints['Climb']:
	lines.append(plt.plot(S, thrustCon['Climb'][climbCond], '--', label=climbCond,  linewidth=3.0)[0])

labels = [ x._label for x in lines]

plt.legend(lines, labels)
plt.legend(loc = 'upper right')

plt.ylabel('Thrust [lbs]')
plt.xlabel('S [ft^2]')
plt.title('Thrust vs S and Fuel Burn')
# plt.axis((S[0], S[-1], 0, T_guess*3))

plt.show()
