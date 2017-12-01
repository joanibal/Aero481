import os,sys,inspect

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import constants
import numpy as np
from Sizing.horizontal_surf_sizing import MAC

# Calculate the control surface position and span

def calcControlSurface(Croot, b, taperRatio, chordRatio, spanRatio, endSpanPosition, controlSurface):
	# Define constants
	Croot_main = Croot
	b_main = b
	lambda_main = taperRatio
	mac_main = Croot_main*2/3*((1 + lambda_main + lambda_main**2)/(1 + lambda_main))
	csName = str(controlSurface)


	# Use 25% Control Surface Chord to Wing Chord Ratio
	chordRatio = chordRatio

	# Calculate the mean aerodynamic chord of the Control Surface
	mac_cs = chordRatio*mac_main

	# Find the start and end chord lengths
	Croot_cs = mac_cs*3/2*((1 + lambda_main + lambda_main**2)/(1 + lambda_main))
	Ctip_cs = Croot_cs*lambda_main
	print(csName + " MAC: " + str(mac_cs) + "m")
	print(csName + " MAC%: "+ str(chordRatio*100)+"%")
	print(csName + " Root Chord:" + str(Croot_cs) + "m") 
	print(csName + " Root Chord Percentage:" + str((Croot_cs/mac_main)*100) + "%")
	print(csName + " Tip Chord:" + str(Ctip_cs) + "m")
	print(csName + " Tip Chord Percentage:" + str((Ctip_cs/mac_main)*100)+ "%")

	# Calculate Control Surface position
	spanRatio = spanRatio
	b_cs = spanRatio*b_main
	pos_cs = b_cs
	endSpan = endSpanPosition*b_main
	broot_cs = endSpan - pos_cs
	btip_cs = broot_cs + pos_cs
	print(csName + " Start Span Position: " + str(broot_cs) + "m")
	print(csName + " Start Span Percentage: " + str((broot_cs/b_main)*100) + "%")
	print(csName + " End Span Position: " + str(btip_cs) + "m")
	print(csName + " End Span Percentage: " + str((btip_cs/b_main)*100) + "%")
	print("")

	return

if __name__ == '__main__':
	#Calculate Results
	# Solve for Main Wing Parameters
	# calcControlSurface(Croot, b, taperRatio, chordRatio, spanRatio, endSpanPosition, controlSurface)
	calcControlSurface(constants.c_root, constants.b, 0.26, 0.08, 0.80, 0.90, "Slat")
	calcControlSurface(constants.c_root, constants.b, 0.26, 0.25, 0.35, 0.50, "Flap")
	calcControlSurface(constants.c_root, constants.b, 0.26, 0.25, 0.40, 0.90, "Aileron")
	calcControlSurface(constants.c_root_HT, 7.68, 0.41, 0.40, 0.95, 1.00, "Elevator")