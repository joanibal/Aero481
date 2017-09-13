import numpy as np
import math

#human weights (project specs)
w_crew = 3*(180+60)		#lbs (crew weight + luggage)
w_payload = 8*(180+60)	#lbs (passenger weight + luggage)

#flight conditions (project specs)
M = 0.85 			#cruise mach
R = 5000 + 200		#nautical miles (range + divert extra)
LD = 16				#based on Roskam (L/D)
c = 0.5				#1/hrs, based on Roskam (TSFC)

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

print(V_kts)

#calculating cruise fuel fraction
ff5 = np.exp(-R/LD*c/V_kts)	#solving breguet equation

print(ff5)

#total fuel fraction
ff = ff1*ff2*ff3*ff4*ff5*ff6*ff7
print(ff)

#Roskam Equation constants
A = 1.02
C = -0.06

#solving for MTOW
w_0 = 80000		#lbs (weight guess)

tolerance = 0.1				#Adjust for acccuracy
converged = 0				#False

while (converged == 0):
	emptyWeightFraction = A*w_0**C
	fuelFraction = ff
	w_0new = (w_crew+w_payload)/(1-fuelFraction-emptyWeightFraction)
   
	if (abs(w_0new - w_0) <= tolerance):
   		converged = 1
	w_0 = w_0new
	
print(w_0)