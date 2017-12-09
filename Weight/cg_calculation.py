import os,sys,inspect

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from weight_refined import *

def cg_location(plane):
	w_0, w_f, plane = prelim_weight(plane.Sref, plane.thrust_req, plane)

	propulsion = plane.w_breakdown['engine_total']*plane.cg_locations['propulsion'] 
	avionics = plane.w_breakdown['avionics']*plane.cg_additional['avionics'] 
	interior = plane.w_breakdown['interior']*plane.cg_locations['fuselage']
	wing = plane.w_breakdown['wing']*plane.cg_locations['wing']
	HT = plane.w_breakdown['HT']*plane.cg_locations['HT']
	canard = plane.w_breakdown['canard']*plane.cg_locations['canard']
	VT = plane.w_breakdown['VT']*plane.cg_locations['VT']
	fuselage = plane.w_breakdown['fuselage']*plane.cg_locations['fuselage']
	surf_cont = plane.w_breakdown['surface_control']*plane.cg_additional['surface_control']
	fuel_cont = plane.w_breakdown['fuel_control']*plane.cg_additional['fuel_control']
	indicators = plane.w_breakdown['indicators']*plane.cg_additional['instruments']
	nose_gear = plane.w_breakdown['nose_gear']*plane.cg_locations['nose_gear']
	main_gear = plane.w_breakdown['main_gear']*plane.cg_locations['main_gear']
	misc = plane.w_breakdown['misc']*plane.cg_additional['furnishings']
	electronics = plane.w_breakdown['electronics']*plane.cg_additional['electronics']

	MtimesL = propulsion + avionics + interior + wing + HT + canard + VT + fuselage + surf_cont + fuel_cont + indicators + nose_gear + main_gear + misc + electronics
	M = sum(plane.w_breakdown.values())

	return MtimesL/M, M

if __name__ == '__main__':
	import j481
	import numpy as np

	cg_loc, weight = cg_location(j481)
	print str(weight)+' lbs at '+str(cg_loc)+' ft from nose'