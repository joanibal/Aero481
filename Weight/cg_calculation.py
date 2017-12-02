import os,sys,inspect

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from weight_refined import *

def cg_location(consts):
	w_0, w_f, w_other = prelim_weight(consts.S_wing, consts.thrust_req, consts)

	propulsion = w_other['engine_total']*consts.cg_locations['propulsion'] 
	avionics = w_other['avionics']*consts.cg_additional['avionics'] 
	interior = w_other['interior']*consts.cg_locations['fuselage']
	wing = w_other['wing']*consts.cg_locations['wing']
	HT = w_other['HT']*consts.cg_locations['HT']
	canard = w_other['canard']*consts.cg_locations['canard']
	VT = w_other['VT']*consts.cg_locations['VT']
	fuselage = w_other['fuselage']*consts.cg_locations['fuselage']
	surf_cont = w_other['surface_control']*consts.cg_additional['surface_control']
	fuel_cont = w_other['fuel_control']*consts.cg_additional['fuel_control']
	indicators = w_other['indicators']*consts.cg_additional['instruments']
	nose_gear = w_other['nose_gear']*consts.cg_locations['nose_gear']
	main_gear = w_other['main_gear']*consts.cg_locations['main_gear']
	misc = w_other['misc']*consts.cg_additional['furnishings']
	electronics = w_other['electronics']*consts.cg_additional['electronics']

	MtimesL = propulsion + avionics + interior + wing + HT + canard + VT + fuselage + surf_cont + fuel_cont + indicators + nose_gear + main_gear + misc + electronics
	M = sum(w_other.values())

	return MtimesL/M, M

if __name__ == '__main__':
	import constants as consts
	import numpy as np

	cg_loc, weight = cg_location(consts)
	print str(weight)+' lbs at '+str(cg_loc)+' ft from nose'