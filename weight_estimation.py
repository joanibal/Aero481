import numpy as np
from regression import regression
import matplotlib.pyplot as plt
# import math

#human weights (project specs)
w_crew = 3.0*(180+60)		#lbs (crew weight + luggage)
w_payload = 8.0*(180+60)	#lbs (passenger weight + luggage)

#flight conditions (project specs)
M = 0.85 			#cruise mach
R = 5000 + 200		#nautical miles (range + divert extra)
LD = 8				#based on Roskam (L/D)
c = 0.75				#1/hrs, based on Roskam (TSFC)

# LD = 18				#based on Roskam (L/D)
# c = 0.35				#1/hrs, based on Roskam (TSFC)

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
ff5 = np.exp(-R/LD*c/V_kts)	#solving breguet equation

# print(ff5)

#total fuel fraction
ff = ff1*ff2*ff3*ff4*ff5*ff6*ff7
print(ff)

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
for i in range(200):
	# i += 1
	emptyWeightFraction = A*w_0**C
	fuelFraction = ff
	w_0new = (w_crew+w_payload)/(1-fuelFraction-emptyWeightFraction)
   
			

	if (abs(w_0new - w_0) <= tolerance):
   		converged = 1
	w_0 += 0.1*(w_0new - w_0)
	# w_0 = w_0new
	# print(w_0)
	

	#converged = 1
	# plt.plot(i, w_0, 'o')


# plt.show()
	
print(w_0)
print(w_0*fuelFraction)
# print(w_0*emptyWeightFraction)
# print(w_crew + w_payload)