import numpy as np
import matplotlib.pyplot as plt

def regression():
	WTO = np.array([92500, 69600, 73000, 174200, 99600, 30800, 51000, 23500, 91000, 120152, 33500, 41000, 13870, 1268000, 987000])
	WE = np.array([50861, 43500, 36100, 102100, 54000, 18656, 30500, 14640, 48300, 70841, 24200, 20735, 8540, 610000, 485300])

	(a_lin, b_lin)= np.polyfit(np.log10(WTO[:-3]),np.log10(WE[:-3]),1)
	# (a_lin, b_lin)= np.polyfit(np.log10(WTO),np.log10(WE),1)

	c = a_lin-1
	a = 10**b_lin

	# print (a, c)

	# data, = plt.plot(np.log10(WTO[:-3]), np.log10(WE[:-3]), 'bo', label='Original Data', markersize=10)
	# regLine, = plt.plot(np.log10(WTO[:-3]), a_lin*np.log10(WTO[:-3]) + b_lin, 'b-', label='Fitted line')

	# dseign, = plt.plot(np.log10(94965), np.log10(53502), 'ro', label='Design Point', markersize=10)
	# design_point_str = '94965 lb MTWO, 53502 lb EW'
	# plt.annotate(design_point_str, xy=(np.log10(94965), np.log10(53502)), xytext=(np.log10(94965)-0.47, np.log10(53502)), weight = 'bold')


	# plt.legend()
	# plt.xlabel('$Log_{10}$ MTOW', size='large')
	# plt.ylabel('$Log_{10}$ Empyty Weight', size='large')
	# plt.show()
	return a, c

def calcWeights(R,L_D, c , M, w_payload ):
	#human weights (project specs)
	# w_crew = 3.0*(180+60)		#lbs (crew weight + luggage)
	# w_payload = 8.0*(180+60)	#lbs (passenger weight + luggage)

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

		f = w - fuelFraction*w - A*w**(C+1) - (w_payload)
		df_dw =  1 - fuelFraction - A*(C+1)*w**C 

		delw = -f/df_dw
						

		if (abs(delw) <= tolerance):
			converged = 1
			return w, w*A*w**C, w*fuelFraction, w_payload


		w += delw
		# print(i, w , delw, f,df_dw  )

		# plt.plot(w, f, 'o')

	raise Error('HiThere')


if __name__ == '__main__':
	import matplotlib.pyplot as plt
	import os,sys,inspect

	sys.path.insert(1, os.path.join(sys.path[0], '..'))
	import constants

	import numpy as np


	print(constants.R, constants.L_D, constants.SFC)
	w_0, w_empty, w_fuel, w_payload = calcWeights(constants.R, constants.L_D, constants.SFC, constants.M, constants.w_payload)

	print(w_0, w_empty, w_fuel, w_payload )
	# plt.show()
