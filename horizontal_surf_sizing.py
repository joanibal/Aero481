import numpy as np 
import constants

def MAC(c_root,w_lambda, b):
	c_MAC = 2.0/3.0*c_root*(1.0+w_lambda+w_lambda**2)/(1.0+w_lambda)
	y_MAC = b/6.0*(1.0+2.0*w_lambda)/(1.0+w_lambda)

	return c_MAC, y_MAC

def hor_Sref(c_HT, c_MAC, Sref, L):
	S = c_HT*c_MAC*Sref/L
	return S

if __name__ == '__main__':

	#MAC
	c_MAC, y_MAC = MAC(constants.c_root, constants.w_lambda, constants.b) #m
	print c_MAC, y_MAC #m

	#wing position
	d_np = constants.static_margin*c_MAC*3.28084 + constants.CG
	print d_np-constants.CG #ft

