# ================== Standard Packages ============================= #
import numpy as np
import matplotlib.pyplot as plt
import os,sys,inspect
import pdb
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import shelve
# ==================== 481  Packages =============================== #

import constants as consts
from Aerodynamics.calcDragPolar import DragPolar
from Weight.weight_refined import prelim_weight
from Weight.weight_estimation import calcWeights
from Weight.fuel_weight_curves import fuel_weight
from TWconstraints import calcTWCeiling, calcTWClimb, calcTWCruise, calcTWTakeoff, calcWSLanding
from Aerodynamics.avlLib import changeSref
# =================== Calculations ================================= #
# for i in range(6)


itermax = 1000
T_guess = 4400

S = np.linspace(1000, 1200, 5)



contraints = {
		'Ceiling': 'ceiling',
		'Cruise': 'cruise',
		'Landing': 'landing',
		'Climb':['Takeoff Climb', 'Trans. Seg. Climb', '2nd Seg. Climb', 'Enroute Climb', 'Balked Climb AEO', 'Balked Climb OEI'],
		'Takeoff': 'Takeoff',
}




# my_shelf = shelve.open('/tmp/shelve4.out')
# for key in my_shelf:
#     globals()[key]=my_shelf[key]
# my_shelf.close()


thrustCon = {
		'Ceiling': np.ones(len(S))*T_guess,
		'Cruise': np.ones(len(S))*T_guess,
		'Landing': np.ones(len(S))*T_guess,
		'Climb':{'Takeoff Climb': np.ones(len(S))*T_guess,
				'Trans. Seg. Climb':  np.ones(len(S))*T_guess,
				'2nd Seg. Climb':  np.ones(len(S))*T_guess,
				'Enroute Climb': np.ones(len(S))*T_guess,
				'Balked Climb AEO': np.ones(len(S))*T_guess,
				'Balked Climb OEI': np.ones(len(S))*T_guess},
		'Takeoff': np.ones(len(S))*T_guess
			}


Sref_landing = S;



tolerance = 10.0


W_S_landing = calcWSLanding(consts.runLength,consts.CL['max']['landing'])

T = np.linspace(0,40000, len(S))
for i in range(len(T)):
	# Sref_landing[i] = Sref_landing[i -1]
	print Sref_landing[i], Sref_landing[i -1]
	for j in range(itermax):

		changeSref(consts, Sref_landing[i])

		W_new = prelim_weight(Sref_landing[i] , T[i], consts)[0]
		# W_S = W/Sref_landing[i]
		# S_new = T_W*W
		print("Landing " +   str(i) + " " + str(np.abs(W_new - W_S_landing*Sref_landing[i])))
		if np.abs(W_new - W_S_landing*Sref_landing[i]) <= tolerance:
			notconverged = False
			break


		Sref_landing[i] = W_new/W_S_landing

	if notconverged:
		raise ValueError(flightCond + ' didnt converge')

for i in range(len(S)):
	# print('i', i)
	# S[i] = S[i-1]
	for flightCond in contraints.keys():
		notconverged = True
		T_upper = 1e12
		T_lower = 0

		# print('flightCond', flightCond)


		if flightCond == 'Climb':
			for climbCond in contraints[flightCond]:
				for j in range(itermax):
					changeSref(consts, S[i])
					W = prelim_weight(S[i] , thrustCon['Climb'][climbCond][i], consts)[0]
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

		# elif flightCond == 'Ceiling':
		# 	for j in range(itermax):
		# 		changeSref(consts, S[i])
		# 		W = prelim_weight(S[i] , thrustCon[flightCond][i], consts)[0]
		# 		W_S = W/S[i]

		# 		CD0, k = DragPolar(W)[0:2] # [0:2] <-- only use the first two ouputs

		# 		T_W = calcTWCeiling(consts.Density_Ceiling/consts.Density_SL , CD0['clean'])

		# 		T_new = T_W*W
		# 		print(flightCond + " " +   str(i) + " " + str(np.abs(T_new - thrustCon[flightCond][i])))
		# 		if np.abs(T_new - thrustCon[flightCond][i]) <= tolerance:
		# 			notconverged = False
		# 			break

		# 		thrustCon[flightCond][i] = T_new

		# 	if notconverged:
		# 		raise ValueError(flightCond + ' didnt converge')


		# elif flightCond == 'Cruise':
		# 	for j in range(itermax):
		# 		changeSref(consts, S[i])

		# 		W = prelim_weight(S[i] , thrustCon[flightCond][i], consts)[0]
		# 		W_S = W/S[i]

		# 		CD0 = DragPolar(W)[0] # [0:2] <-- only use the first two ouputs

		# 		T_W = calcTWCruise(W_S, CD0['clean'], consts.AR, consts.e['cruise'], consts.q)

		# 		T_new = T_W*W
		# 		print(flightCond + " " +   str(i) + " " + str(np.abs(T_new - thrustCon[flightCond][i])))
		# 		if np.abs(T_new - thrustCon[flightCond][i]) <= tolerance:
		# 			notconverged = False
		# 			break

		# 		thrustCon[flightCond][i] = T_new

		# 	if notconverged:
		# 		raise ValueError(flightCond + ' didnt converge')


		# elif flightCond == 'Takeoff':
		# 	for j in range(itermax):
		# 		changeSref(consts, S[i])
		# 		W = prelim_weight(S[i] , thrustCon[flightCond][i], consts)[0]
		# 		W_S = W/S[i]

		# 		T_W = calcTWTakeoff(W_S, consts.CL['max']['takeoff'], consts.runLength)

		# 		T_new = T_W*W
		# 		print(flightCond + " " +   str(i) + " " + str(np.abs(T_new - thrustCon[flightCond][i])))
		# 		if np.abs(T_new - thrustCon[flightCond][i]) <= tolerance:
		# 			notconverged = False
		# 			break

		# 		thrustCon[flightCond][i] = T_new

		# 	if notconverged:
		# 		raise ValueError(flightCond + ' didnt converge')


X, Y, fuel_curves = fuel_weight(S, np.linspace(0, T_guess*20, 10), consts)

filename='/tmp/shelve4.out'
my_shelf = shelve.open(filename,'n') # 'n' for new

for key in dir():
    try:
        my_shelf[key] = globals()[key]
    except TypeError:
        #
        # __builtins__, my_shelf, and imported modules can not be shelved.
        #
        print('ERROR shelving: {0}'.format(key))
my_shelf.close()


# quit()
CS = plt.contour(X, Y, fuel_curves, 20,linestyles='dashed', alpha=0.5, label='Fuel Burn', colors='black')
# CS = plt.contourf(X, Y, fuel_curves, 50, alpha=0.5)

plt.clabel(CS, CS.levels, fmt= '%8.0f')
# cbar = plt.colorbar(CS)
# cbar.ax.set_ylabel('Fuel Weight [lbs]')
# plt.show()


ceiling, = plt.plot(S, thrustCon['Ceiling'], label='Ceiling',linewidth=3.0)
takeoff, = plt.plot(S, thrustCon['Takeoff'], label='Takeoff',linewidth=3.0)

cruise, = plt.plot(S, thrustCon['Cruise'], label='Cruise',linewidth=3.0)
# landing, = plt.plot(S, thrustCon['Landing'], label='Landing',linewidth=3.0)
landing, = plt.plot(Sref_landing, T, label='Landing',linewidth=3.0)
print(T)
print(Sref_landing)
lines = [ceiling, cruise, takeoff, landing]

for climbCond in contraints['Climb']:
	lines.append(plt.plot(S, thrustCon['Climb'][climbCond], '--', label=climbCond,  linewidth=3.0)[0])

labels = [ x._label for x in lines]

# # a = np.logical_and(90000 >=thrustCon['Takeoff'],90000 >= thrustCon['Climb']['Balked Climb OEI'])
# plt.fill_between(S,thrustCon['Takeoff'],90000, where=thrustCon['Takeoff'] > thrustCon['Climb']['Balked Climb OEI'], interpolate=True, color='b', alpha=0.5, edgecolor='none')
# plt.fill_between(S,thrustCon['Climb']['Balked Climb OEI'],90000, where=thrustCon['Takeoff'] < thrustCon['Climb']['Balked Climb OEI'], interpolate=True, color='b', alpha=0.5, edgecolor='none')






# for i in range(len(Sref_landing)):

# 	flightCond = 'Climb'
# 	climbCond = 'Balked Climb OEI'
# 	for j in range(itermax):
# 		W = prelim_weight(Sref_landing[i] , thrustCon['Climb'][climbCond][i], consts)[0]
# 		# W_S = W/S[i]

# 		CD0, k = DragPolar(W)[0:2] # [0:2] <-- only use the first two ouputs

# 		T_W_climb = calcTWClimb(consts.CL['max'], CD0, k, consts.numEngines)[climbCond]

# 		T_climb_new = T_W_climb*W
# 		print(flightCond + " " + climbCond + " " +  str(i) + " " + str(np.abs(T_climb_new - thrustCon['Climb'][climbCond][i])))
# 		if np.abs(T_climb_new - thrustCon['Climb'][climbCond][i]) <= tolerance:
# 			notconverged = False
# 			break

# 		thrustCon['Climb'][climbCond][i] = T_climb_new

# 	if notconverged:
# 		raise ValueError(flightCond + ' ' + climbCond + ' didnt converge')


# print 'done' 





plt.fill_between(Sref_landing, T,thrustCon['Climb']['Balked Climb OEI'], where=T > thrustCon['Climb']['Balked Climb OEI'], interpolate=True, color='b', alpha=0.5, edgecolor='none')

plt.plot([consts.Sref], [consts.thrust_req], 'ro', label='Design Point')
# plt.plot([1080], [consts.thrust_req], 'ro', label='da design pnt')
design_point_str = str(int(consts.Sref)) + ' ft^2, ' + str(consts.thrust_req) + ' lbs'
plt.annotate(design_point_str, xy=(consts.Sref, consts.thrust_req), xytext=(consts.Sref+10, consts.thrust_req+100), weight = 'bold')

plt.legend(lines, labels)
plt.legend(loc = 'upper left')

plt.ylabel('Thrust [lbs]')
plt.xlabel('S [$ft^2$]')
# plt.title('Thrust vs S and Fuel Burn')
plt.axis((S[0], S[-1], 0, 30000))

plt.show()
