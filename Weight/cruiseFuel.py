import os,sys,inspect
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from constants import *
import numpy as np

def cruiseFuel(c, S):  # S must be in [m^2]
    CD = C_f*(Swet_rest + 2.0*S)/S + CL_cruise/(np.pi*AR*e['cruise'])
    cruiseFrac = np.exp(R*c*CD/(speed_kts*CL_cruise))
    return cruiseFrac

def fuel_fraction(c,S):
	ff1 = 0.99		#warmup
	ff2 = 0.995 	#taxi
	ff3 = 0.995	 	#TO
	ff4 = 0.98		#climb

	ff6 = 0.99 		#descent
	ff7 = 0.992		#landing

	cruiseFrac = cruiseFuel(c,S)
	ff5 = 1/cruiseFrac
	ff = ff1*ff2*ff3*ff4*ff5*ff6*ff7
	return 1-ff

if __name__ == '__main__':
	ff = fuel_fraction(SFC, Sref)
	print ff