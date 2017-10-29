#Calculate the stall velocity of the aircraft
import os,sys,inspect

sys.path.insert(1, os.path.join(sys.path[0], '..'))
import math
import numpy as np
import matplotlib.pyplot as plt
import constants
from Weight.weight_buildup import prelim_weight

def stallSpeed(Clmax, W, rho):
	# weight is input in lbf 
	Sref = constants.Sref

	Vstall = math.sqrt((2*W*4.44822)/(rho*Sref*Clmax))
	return Vstall*3.28084

if __name__=='__main__':
	import constants as consts 

	w_0, w_fuel = prelim_weight(consts.Sref/0.09203, consts.thrust_req)
	# print(w_0, w_fuel)
	weight_landing = w_0-w_fuel

	print("Landing Stall Speed (knts): ",  stallSpeed(consts.CL['max']['landing'],weight_landing, 1.225)*0.681818*0.868976)
	print("Cruise Stall Speed (knts): " ,   stallSpeed(consts.CL['max']['cruise'],w_0, consts.Density_Cruise)*0.681818*0.868976)
	print("Takeoff Stall Speed (knts): " ,   stallSpeed(consts.CL['max']['takeoff'],w_0, 1.225)*0.681818*0.868976)
