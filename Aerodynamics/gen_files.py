
import numpy as np
import os



def gen_mass( m_total, cg, I, filename = 'aircraft.mass'):
	
	try:
		os.remove('./aircraft.mass')
	except:
		pass

	f = open('./aircraft.mass', 'w')


	def out(cmd):
		f.write(cmd + '\n')

	out('Lunit = 1.0 m')
	out('Tunit = 1.0 s')
	out('Munit = 1 kg')
	out('g   = 9.81')
	out('rho = 1.225')
	out('#-------------------------')

	out('# Mass Xcg Ycg Zcg     Ixx Iyy Izz Ixy Ixz Iyz Component')
	out('# (kg) (m) (m) (m)     (kg-m^2) (kg-m^2) (kg-m^2) (kg-m^2) (kg-m^2) (kg-m^2)')
	out('*   1.    1.    1.    1.    1.     1.    1.    1.    1.    1.')
	out('+   0.    0.    0.    0.    0.     0.    0.    0.    0.    0.') 
	out( str(m_total) + ' ' + str(cg[0]) + ' ' + str(cg[1]) + ' ' + str(cg[2]) + ' ' + str(I[0]) + ' ' + str(I[1])  + ' ' + str(I[2]) + ' ' + str(I[3]) + ' ' + str(I[4]) + ' ' + str(I[5]) +	' !	Aircraft')

def gen_geo(Sref, MAC, Bref, cg, CDp, wing, AFILE, canard, AFILE_c, file='./aircraft.txt'):

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

	out('#======================================================')
	out('#--------------------- Main Wing ----------------------')
	out('#======================================================')
	out('SURFACE')
	out('Wing')
	out('#Nchordwise  Cspace   [Nspan   Sspace]')
	out('6 1.00 ')
	out('YDUPLICATE')
	out('0.0')
	out('SCALE')
	out('1.0  1.0  1.0')
	out('TRANSLATE')
	out('0.0  0.0  0.0')
	out('ANGLE')
	out('2.500')
	out('#------------------------------------------------------\n')

	for i in xrange(np.shape(wing)[0]):
		out('SECTION')	
		out('#Xle  Yle  Zle  |  Chord   Ainc   Nspan   Sspace')

		line = ''
		for j in xrange(np.shape(wing)[1]):
			line += str( wing[i][j]) + ' '

		out(line)
		out('AFILE')
		out(AFILE[i])
		out('')




	out('#======================================================')
	out('#----------------------- Canard -----------------------')
	out('#======================================================')
	out('SURFACE')
	out('Canard')
	out('#Nchordwise  Cspace   [Nspan   Sspace]')
	out('4 1.00 ')
	out('YDUPLICATE')
	out('0.0')
	out('SCALE')
	out('1.0  1.0  1.0')
	out('TRANSLATE')
	out('0.0  0.0  0.0')
	out('ANGLE')
	out('0')
	out('#------------------------------------------------------\n')

	for i in xrange(np.shape(canard)[0]):
		out('SECTION')
		out('#Xle  Yle  Zle  |  Chord   Ainc   Nspan   Sspace')

		line = ''
		for j in xrange(np.shape(canard)[1]):
			line += str(canard[i][j]) + ' '

		out(line)
		out('AFILE')

		out(AFILE_c[i])
		out('')
		out('CONTROL')
		out('# name gain Xhinge VYZhvec SgnDup')
		out('Canard 1.00 0.0   0 1 0    1.00')
		out('')





	# Horizontal surface data
	out('')
	out('#======================================================')
	out('#------------------- Horizontal Tail ------------------')
	out('#======================================================')
	out('SURFACE')
	out('Horizontal Tail')
	out('#Nchordwise  Cspace   Nspan   Sspace')
	out('4 1.00 20 2.0 ')
	out('YDUPLICATE')
	out('0.0')
	out('SCALE')
	out('1.0  1.0  1.0')
	out('TRANSLATE')
	out('0.0  0.0  0.0')
	out('ANGLE')
	out('0')	
	out('')
	out('#------------------TAIL ROOT/ELEVATOR------------------')
	out('SECTION')
	out('#Xle   Yle     Zle     Chord   Ainc')
	out('96.919 0.0000 18.2415 7.70997 0.000 7 1')
	out('NACA')
	out('0012')
	out('CLAF')
	out('1.1078')
	out('')
	out('CONTROL')
	out('#surface gain xhinge hvec SgnDup')
	out('Elevator -1.00 0.5 0 1 0 1.00')
	out('')
	out('#--------------------TAIL Tip--------------------------')
	out('SECTION')
	out('#Xle   Yle     Zle     Chord   Ainc')
	out('108.795 12.5984 18.2415 3.16109 0.000 7 1')
	out('NACA')
	out('0012')
	out('CLAF')
	out('1.1078')
	out('')
	out('CONTROL')
	out('#surface gain xhinge hvec SgnDup')
	out('Elevator -1.00 0.5 0 1 0 1.00')
	out('')
	out('#======================================================')
	out('#------------------- Vertical Tail --------------------')
	out('#======================================================')
	out('SURFACE')
	out('Vertical Tail')
	out('# Nchordwise Cspace Nspanwise Sspace')
	out('4 1 10 -2.0')
	out('#Xscale Yscale Zscale')
	out('SCALE')
	out('1.0 1.0 1.0')
	out('')
	out('ANGLE')
	out('0.0')
	out('TRANSLATE')
	out('0.0 0.0 0.0')
	out('')
	out('#----------------------ROOT/RUDDER---------------------')
	out('SECTION')
	out('#Xle   Yle     Zle     Chord   Ainc')
	out('86.6496 0.0000 5.8727 11.4829 0.000 7 1')
	out('NACA')
	out('0012')
	out('CLAF')
	out('1.1078')
	out('')
	out('CONTROL')
	out('#surface gain xhinge hvec SgnDup')
	out('Rudder 1.00 0.5 0 0 1 -1.00')
	out('')
	out('#-----------------------TIP/RUDDER---------------------')
	out('SECTION')
	out('#Xle   Yle     Zle     Chord   Ainc')
	out('97.706 0.0000 19.2257 8.61221 0.000 7 1')
	out('NACA')
	out('0012')
	out('CLAF')
	out('1.1078')
	out('CONTROL')
	out('#surface gain xhinge hvec SgnDup')
	out('Rudder 1.00 0.5 0 0 1 -1.00')
	out('#------------------------------------------------------')
	out('\n\n')
	out('# -- END OF FILE --')

	f.close()
	# close file


	# plt.draw()
	# plt.pause(1)


# -- END OF FILE --			
