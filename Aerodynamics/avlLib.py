
import pyAVL

import numpy as np

from gen_files import gen_geo
import matplotlib.pyplot as plt

import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))


from AircraftClass.classes import surface, Object






def runAVL(CL=0.43, geo_file='j481.avl'):
	case = pyAVL.avlAnalysis(geo_file=geo_file)

	# Steady level flight contraints

	# this is actually triming using the canard becuse in pyAVl the first sufrace is assumed to be the elevator
	# thi is something that should be changed, but i didn't bother right now
	case.addConstraint('D1', 0.00)
	# case.addConstraint('D3', 0.00)
	case.addTrimCondition('CL', CL)

	# Execute the case
	case.executeRun()

	# case.calcNP()
	# print case.NP

	return case.CD[0], case.CDFF[0]



def gen_geo(Sref, MAC, Bref, cg, CDp, plane, file=None):
    
	if file is None:
		file = 'Aerodynamics/'+plane.name + '.avl'

	# incAng = [0,   0,    0,  0,   0  ]

	try:
		os.remove(file)
	except:
		pass

	f = open(file, 'w')


	def out(cmd):
		f.write(cmd + '\n')

	out('481\n')
		
	out('#======================================================')
	out('#------------------- Geometry File --------------------')
	out('#======================================================')
	out('# Imperial Used: ft, lbm, etc\n')

	out('#Mach')
	out('0.8')
	out('#IYsym   IZsym   Zsym')
	out(' 0       0       0')
	out('#Sref    Cref    Bref')
	out(str(Sref) + '  ' + str(MAC) + '  '+ str(Bref)) 
	out('#Xref    Yref    Zref')
	out(str(cg[0]) + ' '+ str(cg[1]) + ' '+ str(cg[2])) 
	out('# CDp')
	out(str(CDp) + '\n')
	for name, part in vars(plane).iteritems():
    		if (type(part) == surface ):
    				
				out('#======================================================')
				out('#--------------------- ' + name + ' -------------------')
				out('#======================================================')
				out('SURFACE')
				out(name)
				out('#Nchordwise  Cspace   [Nspan   Sspace]')
				out('4 1.00 ')
				if not(part.vertical):
					out('YDUPLICATE')
					out('0.0')
				
				out('SCALE')
				out('1.0  1.0  1.0')
				out('TRANSLATE')
				out('0.0  0.0  0.0')
				out('ANGLE')
				out('0.00')
				out('#------------------------------------------------------\n')

				for i in xrange(np.shape(part.coords)[0]):
					out('SECTION')	
					out('#Xle  Yle  Zle  |  Chord   Ainc   Nspan   Sspace')
					
					line = ''
					for j in xrange(np.shape(part.coords)[1]):
						line += str( part.coords[i][j]) + ' '

					out(line)
					out('AFILE')
					out(part.airfoil_file)
					out('')

					if ( name == 'canard'):
						out('CONTROL')
						out('# name gain Xhinge VYZhvec SgnDup')
						out('Canard 1.00 0.0   0 1 0    1.00')
						out('')
					
					if (name == 'tail_horz'):
						out('CONTROL')
						out('#surface gain xhinge hvec SgnDup')
						out('Elevator -1.00 0.5 0 1 0 1.00')
						out('')


	out('')
	out('#======================================================')
	out('#----------------------- Fuselage ---------------------')
	out('#======================================================')
	out('')
	out('#--------------------------------------------------')
	out('SURFACE')
	out('Fuselage H')
	out('#Nchordwise  Cspace   Nspanwise  Sspace')
	out('10          1.0')
	out('')
	out('')
	out('COMPONENT')
	out('1')
	out('')
	out('YDUPLICATE')
	out('0.0')
	out('')
	out('SCALE')
	out('1.0   1.0  1.0')
	out('')
	out('TRANSLATE')
	out('0.0   0.0   0.0')
	out('')
	out('')
	out('ANGLE')
	out('4.000')
	out('')
	out('')
	out('SECTION')
	out('#Xle   Yle    Zle      Chord   Ainc  Nspanwise  Sspace')
	out('0.0   0.0    0.0      86   0.    1          0.')
	out('# 124')
	out('SECTION')
	out('#Xle    Yle    Zle     Chord   Ainc  Nspanwise  Sspace')
	out('0.36   0.88    0.0     83.5   0.    1          0.')
	out('')
	out('SECTION')
	out('#Xle    Yle    Zle     Chord   Ainc  Nspanwise  Sspace')
	out('1.619   1.76    0.0     79.12   0.    1          0.')
	out('')
	out('SECTION')
	out('#Xle    Yle    Zle     Chord   Ainc  Nspanwise  Sspace')
	out('3.78   2.64   0.0     73.92   0.    1          0.')
	out('')
	out('SECTION')
	out('#Xle    Yle    Zle     Chord   Ainc  Nspanwise  Sspace')
	out('6.3   3.52   0.0      68.67   0.    1          0.')
	out('')
	out('SECTION')
	out('#Xle    Yle    Zle     Chord   Ainc  Nspanwise  Sspace')
	out('9   4.4    0.0      61    0.    1          0.')




	out('\n\n')
	out('# -- END OF FILE --')

	f.close()




# plt.plot(case.sec_Yle[0], case.sec_CL[0]*case.sec_Chord[0]/10.9339)
def liftDistPlot(plane, CL):

	gen_geo(plane.Sref, plane.wing.MAC_c, plane.wing.span,
	        np.array([plane.cg_fwd, 0, 0]), 0, plane, file='Aerodynamics/'+plane.name +'.avl')
	
	case = pyAVL.avlAnalysis(geo_file='Aerodynamics/'+plane.name +'.avl')

	# Steady level flight contraints
	case.addConstraint('D1', 0.00)
	case.addTrimCondition('CL', CL)

	# Execute the case
	case.executeRun()

	print case.surf_CL
	i = 0
	for surf in [ plane.canard, plane.wing]:

		b_2 = surf.span/2;
		# b = (CL/2)/(a*np.pi)
		print case.surf_CL[i][0]
		print 4/np.pi*case.surf_CL[i][0]*plane.wing.MAC_c*np.sqrt((1 - np.linspace(0, b_2)**2/b_2**2 ))


		# l_ellipse = 4/np.pi*case.surf_CL[0]*surf.MAC_c*np.sqrt((1 - np.linspace(0, b_2)**2/b_2**2 ))



		# lift, = plt.plot(case.sec_Yle[0], case.sec_CL[0]*case.sec_Chord[0]/10.9339,label='wing Distribution', linewidth=2)

		i += 2



	# lift2, = plt.plot(case.sec_Yle2[0], case.sec_CL2[0]*case.sec_Chord2[0]/10.9339,label='Canard Distribution', linewidth=2)
	# elip, = plt.plot(np.linspace(0, a), l_ellipse, '--', label='Elliptical')
	# elip2, = plt.plot(np.linspace(0, a2), l_ellipse2, '--', label='Elliptical')
 
	# plt.xlabel('Y Leading Edge [ft]', fontsize=20)
	# plt.ylabel('Cl*C/Cref', fontsize=20)
	# plt.legend(fontsize=12, loc='upper right')
	# plt.show()
	return case.CD[0]
 




if __name__ == '__main__':
	import j481 
	import g550 
	from calcCoeff import compentCDMethod

	# CD0 = compentCDMethod(
	# 	plane, plane.mach, plane.mu_cruise, plane.speed_fps, plane.density_cruise)
	# gen_geo(j481.Sref, j481.wing.MAC_c, j481.wing.span,
	#         np.array([j481.cg_fwd, 0, 0]), 0, j481, file='Aerodynamics/j481.avl')
	# print runAVL(CL=0.55, geo_file='Aerodynamics/j481.avl')



	# gen_geo(g550.Sref, g550.wing.MAC_c, g550.wing.span,
 #        np.array([g550.wing.offset[0] + g550.wing.MAC_c*.5, 0, 0]), 0, g550, file='Aerodynamics/g550.avl')
	# print runAVL(geo_file='Aerodynamics/g550.avl')

	# # print runAVL(geo_file='j481.avl')

	liftDistPlot(j481, 0.43)

	print('done')
