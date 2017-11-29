from __future__ import division

from openmdao.api import IndepVarComp, Component, Problem, Group
from openmdao.api import ScipyOptimizer, ExecComp, SqliteRecorder
#from openmdao.drivers.pyoptsparse_driver import pyOptSparseDriver
from openmdao.drivers.latinhypercube_driver import OptimizedLatinHypercubeDriver

from scipy.optimize import *
#from sympy import Symbol, nsolve
import numpy as np
import matplotlib.pyplot as plt

from time import localtime, strftime, time
from xfoil_lib import xfoilAlt, getDataXfoil

from Input import AC
import pyAVL



class aeroAnalysis(Component):
	"""
	OpenMDAO component for aerodynamic analysis via AVL
	- Uses the current iteration of the aircraft: in_aircraft
	- Modifies in_aircraft, outputs a new out_aircraft
	- ^ All of the same AC class (AC.wing, AC.tail, etc.)

	Inputs
	-------
	Aircraft_Class:	class
					in_aircraft class


	Outputs
	-------
	Aircraft_Class:	class
					out_aircraft class
	SM			: 	float
					Static margin			
	"""   

	def __init__(self ):
		super(aeroAnalysis,self).__init__()

		# Input instance of aircraft - before modification
		self.add_param('in_aircraft',val=AC, desc='Input Aircraft Class')

		# Output instance of aircaft - after modification
		self.add_output('out_aircraft',val=AC, desc='Output Aircraft Class')

		# Other outputs to be used in top_level group (e.g. constraints)
		self.add_output('SM', val = 0.0, desc = 'static margin')

	def solve_nonlinear(self,params,unknowns,resids):
		# Used passed in instance of aircraft
		AC = params['in_aircraft']

		# print('================  Current Results ===================')
		# print('\n')
		# print("Chord Values", AC.wing.chord_vals)
		# print("Chord Cubic Terms", AC.wing.chord)
		# print("Wingspan", AC.wing.b_wing)
		# print("Boom Length", AC.boom_len)
		# print("Sweep Cubic Terms", AC.wing.sweep)
		# print("Sweep Values", AC.wing.sweep_vals)
		# print("Horiz. Tail Chord Values", AC.tail.htail_chord_vals)
		# print("Horiz. Tail  Chord Cubic Terms", AC.tail.htail_chord)
	
		# Call aero analysis to get CL, CD, CM and NP - Add to class
		AC.alpha, AC.CL, AC.CD, AC.CM, AC.NP, AC.sec_CL, AC.sec_Yle, sec_Chord, velocity = getAeroCoef()

		# Static Margine calculation
		SM = (AC.NP - AC.CG[0])/AC.wing.MAC
		AC.SM = SM

		# Calculate cruise velocity
		AC.vel, AC.ang = calcVelCruise(AC.CL, AC.CD, AC.weight, AC.wing.sref, AC.tail.sref)

		# Get gross lift
		flapped = False
		AC.gross_F, AC.wing_f, AC.tail_f = grossLift(AC.vel, AC.ang, AC.wing.sref, AC.tail.sref, flapped, AC.CL)

		AC.sec_L = calcSecLift(velocity, AC.sec_CL, sec_Chord)

		# print('Wing Lift = %f' % AC.wing_f)
		# print('Tail Lift = %f' % AC.tail_f)

		print("Cruise Velocity = %f m/s" % AC.vel)
		print("Cruise AOA = %f degrees" % AC.ang)
		print("CL of aircraft = %f" % AC.CL(AC.ang))
		print("CD of aircraft = %f" % AC.CD(AC.ang))
		print("SM = %f" % AC.SM)

		# Set output to updated instance of aircraft
		unknowns['out_aircraft'] = AC
		unknowns['SM'] = AC.SM


def getAeroCoef(geo_filename = './Aerodynamics/aircraft.txt', mass_filename = './Aerodynamics/aircraft.mass'):
	"""
	Using AVL, calculate the full-vehicle aerodynamic coefficients
	*As functions of the angle of attack


	Inputs
	----------
	geo_filename 	: 	String
		File name of the AVL geometry file for the aircraft

	mass_filename 	: 	String
		File name of the AVL geometry file for the aircraft

	Outputs
	----------
	alpha 			: 	ndarray
						Sweep of angle of attacks used
	CL,CD, CD, secCL, sec_Yle : Functions
		Functions that will return the value for the coeffiecent 
		for a given angle of attack 
		example: CL(10*np.pi/180)  <- note the use of radians

	NP : float
	   X location of NP in AVL coordinate system
	"""

	# Create the pyAVL case
	case = pyAVL.avlAnalysis(geo_file=geo_filename, mass_file = mass_filename)


	# Steady level flight contraints
	case.addConstraint('elevator', 0.00)
	case.addConstraint('rudder', 0.00)

	# Execute the case
	case.executeRun()

	# Calculate the neutral point
	case.calcNP()
	NP = case.NP
	
	case.clearVals()

	# Create a sweep over angle of attack
	# case.alphaSweep(-15, 30, 2)
	case.alphaSweep(-15, 15, 4)

	alpha = case.alpha
	sec_CL = case.sec_CL
	sec_Yle = case.sec_Yle
	sec_Chord = case.sec_Chord
	velocity = case.velocity

	# get func for aero coeificent
	CL = np.poly1d(np.polyfit(case.alpha,case.CL, 1))
	CD = np.poly1d(np.polyfit(case.alpha,case.CD, 2))
	CM = np.poly1d(np.polyfit(case.alpha,case.CM, 2))

	# # ----------------- Plot Outputs --------------------------
	# plt.figure(4)
	# plt.subplot(411)
	# plt.ylabel('CL')
	# plt.xlabel('Alpha')
	# plt.plot( np.degrees(case.alpha), case.CL, 'b-o')

	# plt.subplot(412)
	# plt.xlabel('CD')
	# plt.ylabel('CL')
	# plt.plot( case.CD, case.CL, 'b-o')


	# plt.subplot(413)
	# plt.ylabel('CM')
	# plt.xlabel('Alpha')
	# plt.plot(np.degrees(case.alpha), case.CM, 'b-o')


	# plt.subplot(414)
	# plt.ylabel('Elvator Deflection')
	# plt.xlabel('Alpha')
	# plt.plot(np.degrees(case.alpha), case.elev_def, 'b-o')

	# plt.show()
	print("NP = %f"% NP)
	print("Max Elevator deflection = %f deg" % max(case.elev_def))

	return (alpha, CL, CD, CM, NP, sec_CL, sec_Yle, sec_Chord, velocity)

# Declare Constants (global)
Rho = 1.225 
g = 9.81
mu_k = 0.005
inced_ang = -5.0 *np.pi/180.0

# Specify path of xfoil
xfoil_path = 'Aerodynamics/xfoil/elev_data'

# Use xfoil to get sectional values for an airfoil
alphas_tail, CLs_tail_flap = getDataXfoil(xfoil_path+ '_flap.dat')[0:2]
alphas_tail_noflap,CLs_tail_noflap = getDataXfoil(xfoil_path+ '.dat')[0:2]
alphas_tail = [x * np.pi/180 for x in alphas_tail]
CL_tail_flap = np.poly1d(np.polyfit(alphas_tail,CLs_tail_flap, 2))
CL_tail_noflap = np.poly1d(np.polyfit(alphas_tail_noflap,CLs_tail_noflap, 2))





def calcSecLift(velocity, sec_CL, sec_Chord):
	sec_L = []
	for n in range(len(sec_CL)):
		# sec_L[n] = [0.5*Rho*velocity[n][0]**2*sec_CL[n][x]*sec_Chord[n][x] for x in range(len(sec_CL[n]))]
		sec_L.append( [0.5*Rho*velocity[n][0]**2*sec_CL[n][x]*sec_Chord[n][x] for x in range(len(sec_CL[n]))] )

	return sec_L
