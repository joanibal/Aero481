
import matplotlib.pyplot as plt
import matplotlib.animation as animation
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

def gen_geo(Sref, MAC, b_wing, cg, CDp, Xle, Yle, C, Xle_t, Yle_t, C_t):

	incAng = [0,   0,    0,  0,   0  ]

	try:
		os.remove('./aircraft.txt')
	except:
		pass

	f = open('./aircraft.txt', 'w')


	def out(cmd):
		f.write(cmd + '\n')

	out('MACH MDAO AVL\n')
		
	out('#======================================================')
	out('#------------------- Geometry File --------------------')
	out('#======================================================')
	out('# AVL Conventions')
	out('# SI Used: m, kg, etc\n')

	out('#Mach')
	out('0.0')
	out('#IYsym   IZsym   Zsym')
	out(' 0       0       0')
	out('#Sref    Cref    b_wing')
	out(str(Sref) + '  ' + str(MAC) + '  '+ str(b_wing)) 
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
	out('     7        1.0      20      -2.0')
	out('YDUPLICATE')
	out('0.0')
	out('SCALE')
	out('1.0  1.0  1.0')
	out('TRANSLATE')
	out('0.0  0.0  0.0')
	out('ANGLE')
	out('0.0')
	out('#------------------------------------------------------\n')

	for i in range(0, len(C)):
		out('SECTION')
		out('#Xle  Yle  Zle  |  Chord   Ainc   Nspan   Sspace')
		out(str(Xle[i]) + '    ' + str(Yle[i]) + '    0       '+ str(C[i]) + '     '+ str(incAng[i])+'      '+ '5      3')
		out('AFILE')
		out('airfoils/A_'+str(i+1) + '.dat')



	# Horizontal surface data
	out('')
	out('#======================================================')
	out('#------------------- Horizontal Tail ------------------')
	out('#======================================================')
	out('SURFACE')
	out('Horizontal Tail')
	out('#Nchordwise  Cspace   Nspan   Sspace')
	out('7       1.0           10        -2 ')
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
	out(str(Xle_t[0]) + '  ' +  str(Yle_t[0]) + '   0.0  '+ str(C_t[0]) +'  0.000')
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
	out(str(Xle_t[1]) + '  ' +  str(Yle_t[1]) + ' 0.000   '+ str(C_t[1]) +'  0.000')
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
	out('10 1.00 10 -2.0')
	out('YDUPLICATE')
	out('0.0')
	out('#Xscale Yscale Zscale')
	out('SCALE')
	out('1.0 1.0 1.0')
	out('')
	out('ANGLE')
	out('0.0')
	out('TRANSLATE')
	out('0.0 0.0 0.0')
	out('')
	out('INDEX')
	out('2')
	out('')
	out('#----------------------ROOT/RUDDER---------------------')
	out('SECTION')
	out('#Xle   Yle     Zle     Chord   Ainc')
	out(str(Xle_t[0]) + ' 0.0   0 ' +str(C_t[0]) + '   0.000')
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
	out(str(Xle_t[0]) + ' 0.0   0.2  ' +str(C_t[0]) + '   0.000')
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
