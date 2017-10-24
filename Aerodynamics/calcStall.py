#Calculate the stall velocity of the aircraft
import os,sys,inspect

sys.path.insert(1, os.path.join(sys.path[0], '..'))
import math
import numpy as np
import matplotlib.pyplot as plt
import constants
from Weight.weight_estimation import calcWeights

def stallSpeed(Clmax):
	w_0, w_empty, w_fuel, w_payload = calcWeights(constants.R, constants.L_D, constants.SFC)
	print(w_0, w_empty, w_fuel, w_payload)
	weight_landing = w_0-w_fuel
	g = -9.81
	#rho = constants.rho
	#assume sea level density
	rho = 1.225
	Sref = constants.Sref
	Clmax = Clmax
	Vstall = math.sqrt((2*weight_landing*g*(-1))/(rho*Sref*Clmax))
	return Vstall*3.28084

if __name__=='__main__':
	Vstall = stallSpeed(2.11)							#Landing with full flaps (30 deg) and 6 deg nose up pitch
	print("Stall Speed (ft/s): " + str(Vstall))