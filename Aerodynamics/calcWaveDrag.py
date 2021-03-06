# Calculate wave drag using 3D Version of Korn Equation
import os,sys,inspect

sys.path.insert(1, os.path.join(sys.path[0], '..'))
import math
import numpy as np
import constants


kappa = 0.95
sweep = constants.sweep
#thickness = constants.surfaces['wing']['t/c']			#Average
thickness = 0.16
cruiseCL = constants.CL['cruise']
M = constants.M

MDD = kappa/math.cos(sweep)-thickness/(math.cos(sweep)**2)-cruiseCL/(10*math.cos(sweep)**3)
Mcrit = MDD-(0.1/80)**(1.0/3)

if M > Mcrit:
	CD_wave = 20*(M-Mcrit)**4
	print("Valid")
elif M < Mcrit:
	CD_wave = 0
	print("Invalid")
print("CD_wave: " + str(CD_wave))