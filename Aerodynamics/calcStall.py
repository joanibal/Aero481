#Calculate the stall velocity of the aircraft
import os,sys,inspect

sys.path.insert(1, os.path.join(sys.path[0], '..'))
import math
import numpy as np
import matplotlib.pyplot as plt
import constants
from Weight.weight_estimation import calcWeights

def stallSpeed(Clmax):
	w_0 = calcWeights(constants.R, constants.L_D, constants.SFC)[0]*0.453592
	g = -9.81
	rho = constants.rho
	Sref = constants.Sref
	Clmax = Clmax
	Vstall = math.sqrt((2*w_0*g*(-1))/(rho*Sref*Clmax))
	return Vstall*3.28084

if __name__=='__main__':
	Vstall = stallSpeed(1.6)
	print("Stall Speed (ft/s): " + str(Vstall))