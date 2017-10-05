import numpy as np 
import constants

def MAC(c_root,w_lambda):
	c_MAC = 2/3*c_root*(1+w_lambda+w_lambda**2)/(1+w_lambda)
	y_MAC = b/6*(1+2*w_lambda)/(1+w_lambda)

	return c_MAC, y_MAC

def hor_Sref(c_HT, c_MAC, Sref, L):
	S = c_HT*c_MAC*Sref/L
	return S

if __name == '__main__':

	c_MAC = MAC(constants.c_root, constants.w_lambda)
	