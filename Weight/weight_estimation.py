import numpy as np

def regression():
	WTO = np.array([92500, 69600, 73000, 174200, 99600, 30800, 51000, 23500, 91000, 120152, 33500, 41000, 13870, 1268000, 987000])
	WE = np.array([50861, 43500, 36100, 102100, 54000, 18656, 30500, 14640, 48300, 70841, 24200, 20735, 8540, 610000, 485300])

	# (a_lin, b_lin)= np.polyfit(np.log10(WTO[:-3]),np.log10(WE[:-3]),1)
	(a_lin, b_lin)= np.polyfit(np.log10(WTO),np.log10(WE),1)

	c = a_lin-1
	a = 10**b_lin

	# print (a, c)

	# plt.plot(np.log10(WTO), np.log10(WE), 'o', label='Original data', markersize=10)
	# plt.plot(np.log10(WTO), a_lin*np.log10(WTO) + b_lin, 'r', label='Fitted line')
	# plt.legend()
	# plt.show()
	return a, c

def calcWeights(R,L_D, c , M=0.85):
	#human weights (project specs)
	w_crew = 3.0*(180+60)		#lbs (crew weight + luggage)
	w_payload = 8.0*(180+60)	#lbs (passenger weight + luggage)

	#fuel fractions (ROSKAM)
	ff1 = 0.99		#warmup
	ff2 = 0.995 	#taxi
	ff3 = 0.995	 	#TO
	ff4 = 0.98		#climb

	ff6 = 0.99 		#descent
	ff7 = 0.992		#landing


	#unit conversion
	a_sound = 574		#knots (speed of sound @40 K-ft)
	V_kts = M*a_sound	#knots = nm/hr (flight speed)


	#calculating cruise fuel fraction
	ff5 = np.exp(-R/L_D*c/V_kts)	#solving breguet equation

	#total fuel fraction
	ff = ff1*ff2*ff3*ff4*ff5*ff6*ff7


	#Raymer Equation constants
	(A, C) = regression()


	#solving for MTOW
	w_0 = 1e5	#lbs (weight guess)
	w = 1e5
	tolerance = 0.1				#Adjust for acccuracy
	converged = 0				#False



	fuelFraction = 1- ff

	for i in range(100):
		# w_0new = (w_crew+w_payload)/(1-fuelFraction-A*w_0**C)
		# w_0 += 0.1*(w_0new - w_0)
		# w_0 = w_0new

		f = w - fuelFraction*w - A*w**(C+1) - (w_crew+w_payload)
		df_dw =  1 - fuelFraction - A*(C+1)*w**C 

		delw = -f/df_dw
						

		if (abs(delw) <= tolerance):
			converged = 1
			return w_0, w_0*A*w_0**C, w_0*fuelFraction, w_crew + w_payload


		w += delw
		# print(i, w , delw, f,df_dw  )

		# plt.plot(w, f, 'o')

	raise Error('HiThere')


if __name__ == '__main__':
	# import matplotlib.pyplot as plt
	import os,sys,inspect

	sys.path.insert(1, os.path.join(sys.path[0], '..'))
	import constants

	import numpy as np


	w_0, w_empty, w_fuel, w_payload = calcWeights(constants.R,constants.L_D, constants.SFC, M=constants.machCruise)

	print(w_0, w_empty, w_fuel, w_payload )
	# plt.show()
