#Calculate the stall velocity of the aircraft
import os,sys,inspect

sys.path.insert(1, os.path.join(sys.path[0], '..'))
import math
# import numpy as np
# import matplotlib.pyplot as plt
import j481
# from Weight.weight_buildup import prelim_weight

def stallSpeed(Clmax, W, rho):
	# weight is input in lbf
	Sref = j481.Sref
	# print Sref

	Vstall = math.sqrt((2*W)/(rho*Sref*Clmax))
	return Vstall

if __name__=='__main__':
	import j481

	# w_0, w_fuel = prelim_weight(consts.Sref*0.92, consts.thrust_req, consts)
	w_0 = 55774.0
	w_fuel = 17298.0

	print(w_0, w_fuel)
	weight_landing = 0.77*w_0

	print("Landing Stall Speed (kts): ",  stallSpeed(j481.CL['max']['landing'],weight_landing, j481.density_SL)*0.592484) #last factor converts ft/s to knots
	print("Cruise Stall Speed (kts): " ,   stallSpeed(j481.CL['max']['cruise'],w_0, j481.density_cruise)*0.592484)
	print("Takeoff Stall Speed (kts): " ,   stallSpeed(j481.CL['max']['takeoff'],w_0, j481.density_SL)*0.592484)
