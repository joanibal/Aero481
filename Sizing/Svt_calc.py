import os,sys,inspect

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import constants
import numpy as np
from Sizing.horizontal_surf_sizing import MAC

def cMAC(c_root_VT, taper_VT, b):
	c_MAC, _ = MAC(c_root_VT, taper_VT, b)
	return c_MAC

def calcL_VT(c_MAC, sweep_VT, fuse_length, CGpos, c_root_VT):
	x = c_MAC*np.tan(sweep_VT)
	L_VT = (fuse_length-CGpos)-c_root_VT+x
	return L_VT

def calcS_VT(L_VT, c_VT, b, Sref):
	S_VT = c_VT*b*Sref/L_VT
	return S_VT

def calcTipChord(c_VT, taper_VT):
	c_tip_VT = c_VT*taper_VT
	return c_tip_VT

def calcb_VT(S_VT, c_root_VT, c_tip_VT):
	b_VT = 2*S_VT/(c_root_VT+c_tip_VT)
	return b_VT

def calcAR_VT(b_VT, S_VT):
	AR_VT = b_VT**2/S_VT
	return AR_VT

def calcyMAC(c_root_VT, taper_VT, b):
	_, y_MAC = MAC(c_root_VT, taper_VT, b_VT)
	return y_MAC

if __name__ == '__main__':

	# Calculate Chord Mac
	c_MAC = cMAC(constants.c_root_VT, constants.taper_VT, 0) 			
	print("Chord MAC: " + str(c_MAC) + " m")							

	# Calculate Vertical Tail Moment Arm
	L_VT = calcL_VT(c_MAC, constants.sweep_VT, constants.fuse_length, constants.CGpos, constants.c_root_VT)
	print("VT Arm Length: " + str(L_VT) + " m")

	# Calculate Vertical Tail Reference Area
	S_VT = calcS_VT(L_VT, constants.c_VT, constants.b, constants.Sref)
	print("VT Sref: " + str(S_VT) + " m^2")

	# Calculate Tip Chord Length
	c_tip_VT = calcTipChord(constants.c_VT, constants.taper_VT)
	print("VT Tip Chord: " + str(c_tip_VT) + " m")

	# Calculate Vertical Tail Span
	b_VT = calcb_VT(S_VT, constants.c_root_VT, c_tip_VT)
	print("VT Span: " + str(b_VT) + " m")

	# Calculate Horizontal Tail Aspect Ratio
	AR_VT = calcAR_VT(b_VT, S_VT)
	print("BT Aspect Ratio:" + str(AR_VT))

	# Calculate yMAC
	y_MAC = calcyMAC(constants.c_root_VT, constants.taper_VT, b_VT)
	print("y MAC: " + str(y_MAC) + " m")