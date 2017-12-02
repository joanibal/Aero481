import pyAVL
import numpy as np
# import matplotlib.pyplot as plt
from gen_files import gen_geo


# settup inital conditions
# aircraft parameters
Sref = 1060
wingSref0 = 950;
MAC = 14.63
Bref = 92.02

cg = [51.44619, 0, 0]
 
CDp = 0




Xle = np.array([5,       10.9592,  41.8333,   75.4948])
Yle = np.array([0,       2,        3,    46.0302])
Zle = np.array([-2.16535, -2.16535, -2.16535,   -2.75591])
C =   np.array([61,  51.21,  15.0591,   4.22244])
incAng = np.array([5, 5, 0, 0 ])
Nspan = np.array([4, 4, 30, 30])
Sspace = np.array([3, 3, 3, 3])
AFILE = np.array(['naca0008.dat', 'naca0008.dat', 'sc20612-il.dat', 'sc20612-il.dat'])

wing= np.vstack((Xle, Yle, Zle, C, incAng, Nspan, Sspace)).T




# Xle = np.array([41.8333,   75.4948])
# Yle = np.array([     0,    46.0302])
# Zle = np.array([ -2.16535,   -2.75591])
# C =   np.array([ 15.0591,   4.22244])
# incAng = np.array([0, 0 ])
# Nspan = np.array([60, 60])
# Sspace = np.array([3, 3])
# AFILE = np.array(['sc20612-il.dat', 'sc20612-il.dat'])

# wing= np.vstack((Xle, Yle, Zle, C, incAng, Nspan, Sspace)).T





wing0 = wing


Xle_c = np.array([10.9592, 18.7808])
Yle_c = np.array([0.0, 16.9])
Zle_c = np.array([-0.73, -0.984252])
C_c = np.array([7, 3])
incAng_c = np.array([2, 2])
Nspan_c = np.array([8, 8])
Sspace_c = np.array([3, 3])
AFILE_c = np.array(['sc20612-il.dat', 'sc20612-il.dat'])

canard= np.vstack((Xle_c, Yle_c, Zle_c,  C_c, incAng_c, Nspan_c, Sspace_c)).T

canard0 = canard








# gen_geo(Sref, MAC, Bref, cg, CDp,  wing0, AFILE, canard0, AFILE_c, file='J481T.avl')
# exit
# run the case

def runAVL():
	case = pyAVL.avlAnalysis(geo_file='J481T.avl')

	# Steady level flight contraints
	case.addConstraint('elevator', 0.00)
	case.addTrimCondition('CL', 0.57)

	# Execute the case
	case.executeRun()

	return case.CD[0]





# # ===============  Sweep ==============
# ===============  Sweep ==============
print(' ===============  Sweep ==============')
sweep_inital = 0.0 
sweep_final = 45.0

hspan = wing0[-1,1]


# for angle in np.linspace(sweep_inital, sweep_final, 10):


# 	d = np.tan(np.deg2rad(angle))*hspan
# 	wing[-1,0] = round(wing0[2,0]+0.25*wing0[2,3]+d-0.25*wing0[-1,3], 4)

# 	gen_geo(Sref, MAC, Bref, cg, CDp,  wing, AFILE, canard0, AFILE_c, file='J481T.avl')
# 	print runAVL()





# ===============  Taper ==============
print(' ===============  Taper ==============')

taper_final = 0.0

wing = wing0
tip_quarterchord_position = wing0[-1,0] - 0.25*wing0[-1,3]
# print '\n# wing0 taper ratio trade study from 1 to ', taper_final

# for taper in np.linspace(1.0, taper_final, 10):

# 	wing[0,3] = wingSref0/(hspan*(1 + taper))
# 	wing[-1, 3] = taper*wing[0,3]
# 	wing[-1,0] = round(tip_quarterchord_position+wing[-1, 3]*0.25, 4)



# 	gen_geo(Sref, MAC, Bref, cg, CDp,  wing, AFILE, canard0, AFILE_c, file='J481T.avl')
# 	print runAVL()




# ===============  AR ==============
print(' ===============  AR ==============')
wing = wing0
taper_ratio = wing[-1,3]/wing[0,3]
root_X_quarterchord = wing[0,0] + 0.25*wing[0,3]
AR_init = 7
AR_final = 15



root_coord = []
tip_coord = []



sweep_quarterchord = np.arctan((wing[-1,0] - wing[0,0]+0.25*wing[0,3] +0.25*wing[-1,3])/hspan )

# for AR in np.linspace(AR_init, AR_final, 10):

# 	b = (AR*(wingSref0))**0.5
# 	# print b
# 	c_root = wingSref0/(b/2*(1+taper_ratio))
# 	# print c_root, taper_ratio
# 	c_tip = taper_ratio*c_root
# 	# print c_tip
# 	tan_sweep_LE = np.tan(sweep_quarterchord)+ (1-taper_ratio)/(AR*(1+taper_ratio))
# 	# print tan_sweep_LE
# 	root_X_LE = root_X_quarterchord - 0.25*c_root
# 	# print root_X_LE
# 	tip_X_LE = tan_sweep_LE*b*0.5 + root_X_LE
# 	# print tip_X_LE


# 	wing[0,0] = root_X_LE
# 	wing[0,3] = c_root

# 	wing[-1,0] = tip_X_LE
# 	wing[-1,1] = b/2

# 	wing[-1,3] = c_tip


# 	gen_geo(Sref, MAC, Bref, cg, CDp,  wing, AFILE, canard0, AFILE_c, file='J481T.avl')
# 	print runAVL()



# ===============  Sref ==============
print(' ===============  Sref ==============')
wing = wing0

# for a constant aspect ratio
AR = Bref**2/wingSref0



sref_start = 700.0
sref_end = 2000.0

for wingSref in np.linspace(sref_start, sref_end, 10):

	wing[-1, 1] = np.sqrt(AR*wingSref)
	# print 'wing[-1,1]', wing[-1,1]
	wing[0, 0] = wingSref/(wing[-1,1]*(1+taper_ratio))
	# print wing[0, 0]
	# print (wing[-1,1]*(1+taper_ratio))
# 
	root_X_LE = root_X_quarterchord - 0.25*wing[0, 3]
	# print root_X_quarterchord , 0.25*wing[0, 0]
	# quit()
	tan_sweep_LE = np.tan(sweep_quarterchord)+ (1-taper_ratio)/(AR*(1+taper_ratio))

	# print tan_sweep_LE


	tip_X_LE = tan_sweep_LE*wing[-1, 1]*0.5 + root_X_LE


	wing[0,0] = root_X_LE
	# wing[0,3] = c_root

	wing[-1,0] = tip_X_LE
	# wing[-1,1] = b/2

	wing[-1,3] = wing[0, 3]*taper_ratio

	gen_geo( Sref, MAC, Bref, cg, CDp,  wing, AFILE, canard0, AFILE_c, file='J481T.avl')
	print runAVL()

# print ' # '+str(round((tan_sweep_LE*0.5*b)+root['X'], 4))+' '+str(round(0.5*b,4))

# 	return 0	

# if __name__ == '__main__':
# 	import constants as consts

# 	# base case
# 	#43.7336 0.0000 -2.16535 16.2402 0.0 19 3 (original root)
# 	root = {'X':43.7336,
# 			'Y':0.0000,
# 			'Z':-2.16535,
# 			'c':16.2402,
# 			'Ainc':0,
# 			'Nspan':19,
# 			'Sspace':3}
# 	# 75.4948 46.0302 -2.75591 4.22244 -2 19 3 (original tip)
# 	tip = {'X':75.4948,
# 		   'Y':46.0302,
# 		   'Z':-2.75591,
# 		   'c':4.22244,
# 		   'Ainc':-2,
# 		   'Nspan':19,
# 		   'Sspace':3,}

# 	sweep_study(root, tip, 42, 2) #final sweep angle & angle step size
# 	taper_study(root, tip, 0, 21) #taper final & number of steps
# 	AR_study(root, tip, consts.S_wing, consts.sweep, 1.0, 16, 16) #start AR & final AR & number of steps
# 	Sref_study(root, tip, consts.sweep, 900, 2500, 17) #start Sref, end Sref, number of steps


# runAVL()
# quit()
    




# # for taper in xrange




# # for area in range 


# # for 






# # Calculate the neutral point
# case.calcNP()
# NP = case.NP

# case.clearVals()

# # Create a sweep over angle of attack
# # case.alphaSweep(-15, 30, 2)
# case.alphaSweep(-15, 15, 4)

# alpha = case.alpha
# sec_CL = case.sec_CL
# sec_Yle = case.sec_Yle
# sec_Chord = case.sec_Chord
# velocity = case.velocity

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
# print("NP = %f"% NP)
# print("Max Elevator deflection = %f deg" % max(case.elev_def))
