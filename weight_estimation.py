import numpy as np
from regression import regression
import matplotlib.pyplot as plt
# import math

def calcWeights(R,L_D, c , M=0.85):
	#human weights (project specs)
	w_crew = 3.0*(180+60)		#lbs (crew weight + luggage)
	w_payload = 8.0*(180+60)	#lbs (passenger weight + luggage)
	# w_payload = 35000	#lbs (passenger weight + luggage)
	# w_payload += 1000
	# print(w_payload + w_crew)
	#flight conditions (project specs)
	# M = 0.85 			#cruise mach
	# R = 5000 + 200		#nautical miles (range + divert extra)
	# L_D = 8				#based on Roskam (L/D)
	# c = 0.75				#1/hrs, based on Roskam (TSFC)

	# L_D = 18				#based on Roskam (L/D)
	# c = 0.35				#1/hrs, based on Roskam (TSFC)

	#fuel fractions (ROSKAM)
	ff1 = 0.99		#warmup
	ff2 = 0.995 	#taxi
	ff3 = 0.995	 	#TO
	ff4 = 0.98		#climb

	ff6 = 0.99 		#descent
	ff7 = 0.992		#landing

	# ff_loiter = 0.97

	#unit conversion
	a_sound = 574		#knots (speed of sound @40 K-ft)
	V_kts = M*a_sound	#knots = nm/hr (flight speed)


	#calculating cruise fuel fraction
	ff5 = np.exp(-R/L_D*c/V_kts)	#solving breguet equation

	# print(ff5)

	#total fuel fraction
	ff = ff1*ff2*ff3*ff4*ff5*ff6*ff7
	# ff = ff1*ff2*ff3*ff4*ff5*ff6*ff7
	# print(ff)

	#Raymer Equation constants
	# A = 1.02
	# C = -0.06 
	(A, C) = regression()
	# A = 1.10
	# C = -0.06


	#solving for MTOW
	w_0 = 1e6	#lbs (weight guess)

	tolerance = 0.1				#Adjust for acccuracy
	converged = 0				#False

	# i=0
	# while (converged == 0):
	fuelFraction = 1- ff

	for i in range(100):
		# i += 1
		emptyWeightFraction = A*w_0**C
		w_0new = (w_crew+w_payload)/(1-fuelFraction-emptyWeightFraction)
	
				

		if (abs(w_0new - w_0) <= tolerance):
			converged = 1
			break
		w_0 += 0.1*(w_0new - w_0)
		# w_0 = w_0new
		# print(w_0)
		

		# converged = 1
		plt.plot(i, w_0, 'o')


		
	#print('w_0', w_0)
	#print('w_f', w_0*fuelFraction)
	return w_0, w_0*emptyWeightFraction, w_0*fuelFraction, w_crew + w_payload
	# print(w_0*emptyWeightFraction)
	# print(w_crew + w_payload)


if __name__ == '__main__':
    		#flight conditions (project specs)
	# M = 0.85 			#cruise mach
	# R = 5000 + 200		#nautical miles (range + divert extra)
	# L_D = 8				#based on Roskam (L/D)
	# c = 0.75				#1/hrs, based on Roskam (TSFC)

	# w_0, w_empty, w_fuel, w_payload = calcWeights((5000+300),15, 0.657, M=0.85)
	# print('w_0      ', '      w_empty      ', ' w_fuel      ', 'w_payload  ' )

	# print(w_0, w_empty, w_fuel, w_payload )
	w_0, w_empty, w_fuel, w_payload = calcWeights((5000+200),15, 0.657, M=0.85)

	# w_0, w_empty, w_fuel, w_payload = calcWeights((6750),18, 0.657, M=0.80) #for G650 comparison
	# print(w_0, w_empty, w_fuel, w_payload )
	# w_0, w_empty, w_fuel, w_payload = calcWeights((5000+100),15, 0.657, M=0.85)

	print(w_0, w_empty, w_fuel, w_payload )
	# w_0, w_empty, w_fuel, w_payload = calcWeights((5000+200),16, 0.8, M=0.85)
	# w_0, w_empty, w_fuel, w_payload = calcWeights(1620,16, 0.5, M=0.82) # 737
	

	# print(w_0, w_empty, w_fuel, w_payload )
	# plt.show()

	# calcWeights((5000+200),8, 0.75, M=0.85)
	