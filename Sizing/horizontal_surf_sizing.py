import os,sys,inspect

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import numpy as np 
import constants

def MAC(c_root,w_lambda, b):
	c_MAC = 2.0/3.0*c_root*(1.0+w_lambda+w_lambda**2)/(1.0+w_lambda)
	y_MAC = b/6.0*(1.0+2.0*w_lambda)/(1.0+w_lambda)
	return c_MAC, y_MAC

def hor_Sref(c_HT, c_MAC, Sref, L):
	S = c_HT*c_MAC*Sref/L
	return S

def hor_surf_prop(Sref,root_chord, taper):
	b = 2*Sref/(root_chord*(1.0+taper))
	AR = b**2.0/Sref
	return b, AR

if __name__ == '__main__':

	#MAC
	c_MAC, y_MAC = MAC(constants.c_root, constants.w_lambda, constants.b) #m
	print c_MAC, y_MAC #m

	#wing position
	d_np = constants.static_margin*c_MAC*3.28084 + constants.CG
	print d_np-constants.CG #ft

	#horizontal stabilizer calculations
	S_total = hor_Sref(constants.c_HT, c_MAC, constants.Sref, constants.L_HT)
	print S_total*constants.L_HT

	#HT calculations
	Sref_HT = (S_total*constants.L_HT-constants.L_c*constants.Sref_c)/constants.L_HT
	print Sref_HT #m^2

	b_HT, AR_HT = hor_surf_prop(Sref_HT, constants.c_root_HT, constants.taper_HT)
	print b_HT, AR_HT #m

	_ , y_MAC_HT = MAC(constants.c_root_HT, constants.taper_HT, b_HT)
	print y_MAC_HT #m

	#canard calculations
	b_c, AR_c = hor_surf_prop(constants.Sref_c, constants.c_root_c, constants.taper_c)
	print b_c, AR_c #m

	_ , y_MAC_c = MAC(constants.c_root_c, constants.taper_c, b_c)
	print y_MAC_c #m