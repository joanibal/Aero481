
import pyAVL

import numpy as np

from gen_files import gen_geo
import matplotlib.pyplot as plt







def runAVL(CL=0.57, geo_file='J481T.avl'):
	case = pyAVL.avlAnalysis(geo_file=geo_file)

	# Steady level flight contraints
	case.addConstraint('elevator', 0.00)
	case.addTrimCondition('CL', CL)

	# Execute the case
	case.executeRun()

	# case.calcNP()
	# print case.NP

	return case.CD[0]

# plt.plot(case.sec_Yle[0], case.sec_CL[0]*case.sec_Chord[0]/10.9339)
def liftDistPlot(geo_file):
	CL = 0.57
	case = pyAVL.avlAnalysis(geo_file=geo_file)

	# Steady level flight contraints
	case.addConstraint('elevator', 0.00)
	case.addTrimCondition('CL', CL)

	# Execute the case
	case.executeRun()

	# case.calcNP()
	# print case.NP
	case = pyAVL.avlAnalysis(geo_file=geo_file)

	# Steady level flight contraints
	case.addConstraint('elevator', 0.00)
	case.addTrimCondition('CL', CL)

	# Execute the case
	case.executeRun()

	a = 46.2331050223;
	a2 = 13.03;
	b = (CL/2)/(a*np.pi)

	# l_ellipse = np.sqrt((np.linspace(0, a)**2/a**2 - 1)*b**2)
	l_ellipse = 0.58*np.sqrt((1 - np.linspace(0, a)**2/a**2 ))
	l_ellipse2 = 0.245*np.sqrt((1 - np.linspace(0, a2)**2/a2**2 ))
		# print  np.linspace(0, a)**2
	# print a**2
	# print b**2
	# # print (np.linspace(0, a)**2/a**2 - 1)
	# print l_ellipse
	# case.calcNP()
	# print case.NP
	lift, = plt.plot(case.sec_Yle[0], case.sec_CL[0]*case.sec_Chord[0]/10.9339,label='wing Distribution', linewidth=2)
	lift2, = plt.plot(case.sec_Yle2[0], case.sec_CL2[0]*case.sec_Chord2[0]/10.9339,label='Canard Distribution', linewidth=2)
	elip, = plt.plot(np.linspace(0, a), l_ellipse, '--', label='Elliptical')
	elip2, = plt.plot(np.linspace(0, a2), l_ellipse2, '--', label='Elliptical')

	plt.xlabel('Y Leading Edge [ft]', fontsize=20)
	plt.ylabel('Cl*C/Cref', fontsize=20)
	plt.legend(fontsize=12, loc='upper right')
	plt.show()

def changeSref(consts, Sref, Sref_c):
	wingSref = consts.Sref


	sweep_quarterchord = consts.sweep
	# print(sweep_quarterchord)
	root_X_quarterchord = consts.wing[2,0] + 0.25*consts.wing[2,3]

	consts.wing[-1, 1] = (consts.AR*wingSref)**(0.5)/2
	# print 'wing[-1,1]', wing[-1,1]
	consts.wing[2, 0] = wingSref/(consts.wing[-1,1]*(1+consts.w_lambda))
	# print consts.wing[0, 0]
	# print (consts.wing[-1,1]*(1+consts.w_lambda))
# 
	root_X_LE = root_X_quarterchord - 0.25*consts.wing[2, 3]
	# print root_X_quarterchord , 0.25*consts.wing[0, 0]
	# quit()
	tan_sweep_LE = np.tan(sweep_quarterchord)+ (1-consts.w_lambda)/(consts.AR*(1+consts.w_lambda))

	# print tan_sweep_LE


	tip_X_LE = tan_sweep_LE*(consts.wing[-1, 1]- consts.wing[2, 1]) + root_X_LE


	consts.wing[2,0] = root_X_LE
	# consts.wing[0,3] = c_root

	consts.wing[-1,0] = tip_X_LE
	# consts.wing[-1,1] = b/2

	consts.wing[-1,3] = consts.wing[2, 3]*consts.w_lambda







	AR_c = consts.span_c**2/(consts.Sref_c*10.7639) 

	sweep_quarterchord_C = consts.sweep_c
	# print(sweep_quarterchord_C)
	root_X_quarterchord_c = consts.canard[0,0] + 0.25*consts.canard[0,3]

	consts.canard[-1, 1] = (AR_c*Sref_c)**(0.5)/2
	# print 'canard[-1,1]', canard[-1,1]
	consts.canard[0, 0] = Sref_c/(consts.canard[-1,1]*(1+consts.taper_c))
	# print consts.canard[0, 0]
	# print (consts.canard[-1,1]*(1+consts.taper_c))
# 
	root_X_LE_c = root_X_quarterchord_c - 0.25*consts.canard[0, 3]
	# print root_X_quarterchord , 0.25*consts.canard[0, 0]
	# quit()
	tan_sweep_LE_c = np.tan(sweep_quarterchord_C)+ (1-consts.taper_c)/(AR_c*(1+consts.taper_c))

	# print tan_sweep_LE_c


	tip_X_LE_c = tan_sweep_LE_c*consts.canard[-1, 1] + root_X_LE_c


	consts.canard[0,0] = root_X_LE_c
	# consts.canard[0,3] = c_root

	consts.canard[-1,0] = tip_X_LE_c
	# consts.canard[-1,1] = b/2

	consts.canard[-1,3] = consts.canard[0, 3]*consts.taper_c



	gen_geo( Sref , consts.c_MAC*3.28084, consts.b*3.28084, consts.cg, 0,  consts.wing, consts.AFILE, consts.canard, consts.AFILE_c, file='./Aerodynamics/J481T.avl')
	



	# print 'updated'
	# print consts.wing.T






	return 

if __name__ == '__main__':
	liftDistPlot('J4812.avl') 

# import pyAVL
# import numpy as np
# # import matplotlib.pyplot as plt
# from gen_files import gen_geo


# # settup inital conditions
# # aircraft parameters
# Sref = 1060
# consts.S_wing0 = 950;
# MAC = 14.63
# Bref = 92.02

# cg = [51.44619, 0, 0]
 
# CDp = 0




# Xle = np.array([5,       10.9592,  41.8333,   75.4948])
# Yle = np.array([0,       2,        3,    46.0302])
# Zle = np.array([-2.16535, -2.16535, -2.16535,   -2.75591])
# C =   np.array([61,  51.21,  15.0591,   4.22244])
# incAng = np.array([5, 5, 0, 0 ])
# Nspan = np.array([2, 2, 10, 10])
# Sspace = np.array([3, 3, 3, 3])
# AFILE = np.array(['naca0008.dat', 'naca0008.dat', 'sc20612-il.dat', 'sc20612-il.dat'])

# wing= np.vstack((Xle, Yle, Zle, C, incAng, Nspan, Sspace)).T





# Xle_c = np.array([10.9592, 18.7808])
# Yle_c = np.array([0.0, 16.9])
# Zle_c = np.array([-0.73, -0.984252])
# C_c = np.array([7, 3])
# incAng_c = np.array([2, 2])
# Nspan_c = np.array([8, 8])
# Sspace_c = np.array([3, 3])
# AFILE_c = np.array(['sc20612-il.dat', 'sc20612-il.dat'])

# canard= np.vstack((Xle_c, Yle_c, Zle_c,  C_c, incAng_c, Nspan_c, Sspace_c)).T



# # print(' ===============  Sweep ==============')

# def changeSweep(consts, sweep):

# 	hspan = consts.wing[-1,1]

# 	d = np.tan(np.deg2rad(sweep))*hspan
# 	wing[-1,0] = round(consts.wing[2,0]+0.25*consts.wing[2,3]+d-0.25*consts.wing[-1,3], 4)

# 	gen_geo(Sref, MAC, Bref, cg, CDp,  wing, AFILE, canard0, AFILE_c, file='./Aerodynamics/J481T.avl')

# 	return 0





# # ===============  Taper ==============

	
# def changeTaper(consts, taper)
	

# 	wing[0,3] = consts.wing/(consts.wing[-1,1]*(1 + taper))
# 	wing[-1, 3] = taper*wing[0,3]
# 	wing[-1,0] = round(tip_quarterchord_position+wing[-1, 3]*0.25, 4)



# 	gen_geo(Sref, MAC, Bref, cg, CDp,  wing, AFILE, canard0, AFILE_c, file='J481T.avl')
# 	print runAVL()



# taper_final = 0.0

# wing = wing0
# tip_quarterchord_position = wing0[-1,0] - 0.25*wing0[-1,3]
# # print '\n# wing0 taper ratio trade study from 1 to ', taper_final

# # for taper in np.linspace(1.0, taper_final, 10):



# # ===============  AR ==============
# print(' ===============  AR ==============')
# wing = wing0
# consts.w_lambda = wing[-1,3]/wing[0,3]
# root_X_quarterchord = wing[0,0] + 0.25*wing[0,3]
# AR_init = 7
# AR_final = 15



# root_coord = []
# tip_coord = []



# sweep_quarterchord = np.arctan((wing[-1,0] - wing[0,0]+0.25*wing[0,3] +0.25*wing[-1,3])/hspan )

# # for AR in np.linspace(AR_init, AR_final, 10):

# # 	b = (AR*(S_wing0))**0.5
# # 	# print b
# # 	c_root = S_wing0/(b/2*(1+consts.w_lambda))
# # 	# print c_root, consts.w_lambda
# # 	c_tip = consts.w_lambda*c_root
# # 	# print c_tip
# # 	tan_sweep_LE = np.tan(sweep_quarterchord)+ (1-consts.w_lambda)/(AR*(1+consts.w_lambda))
# # 	# print tan_sweep_LE
# # 	root_X_LE = root_X_quarterchord - 0.25*c_root
# # 	# print root_X_LE
# # 	tip_X_LE = tan_sweep_LE*b*0.5 + root_X_LE
# # 	# print tip_X_LE


# # 	wing[0,0] = root_X_LE
# # 	wing[0,3] = c_root

# # 	wing[-1,0] = tip_X_LE
# # 	wing[-1,1] = b/2

# # 	wing[-1,3] = c_tip


# # 	gen_geo(Sref, MAC, Bref, cg, CDp,  wing, AFILE, canard0, AFILE_c, file='J481T.avl')
# # 	print runAVL()



# ===============  Sref ==============
# print(' ===============  Sref ==============')
# wing = wing0

# # for a constant aspect ratio
# AR = Bref**2/S_wing0



# sref_start = 700.0
# sref_end = 2000.0



# def changeCSref(consts, Sref_c):


# 	AR_c = consts.span_c**2/(consts.Sref_c*10.7639) 

# 	sweep_quarterchord_C = consts.sweep_c
# 	# print(sweep_quarterchord_C)
# 	root_X_quarterchord_c = consts.canard[0,0] + 0.25*consts.canard[0,3]

# 	consts.canard[-1, 1] = (AR_c*Sref_c)**(0.5)/2
# 	# print 'canard[-1,1]', canard[-1,1]
# 	consts.canard[0, 0] = Sref_c/(consts.canard[-1,1]*(1+consts.taper_c))
# 	# print consts.canard[0, 0]
# 	# print (consts.canard[-1,1]*(1+consts.taper_c))
# # 
# 	root_X_LE_c = root_X_quarterchord_c - 0.25*consts.canard[0, 3]
# 	# print root_X_quarterchord , 0.25*consts.canard[0, 0]
# 	# quit()
# 	tan_sweep_LE_c = np.tan(sweep_quarterchord_C)+ (1-consts.taper_c)/(AR*(1+consts.taper_c))

# 	# print tan_sweep_LE_c


# 	tip_X_LE_c = tan_sweep_LE_c*consts.canard[-1, 1]*0.5 + root_X_LE_c


# 	consts.canard[0,0] = root_X_LE_c
# 	# consts.canard[0,3] = c_root

# 	consts.canard[-1,0] = tip_X_LE_c
# 	# consts.canard[-1,1] = b/2

# 	consts.canard[-1,3] = consts.canard[0, 3]*consts.taper_c
# 	# print consts.wing
# 	gen_geo( Sref, consts.c_MAC, consts.b, consts.cg, 0,  consts.wing, consts.AFILE, consts.canard, consts.AFILE_c, file='./Aerodynamics/J481T.avl')
	
# 	return 




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



