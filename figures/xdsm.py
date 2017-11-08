from pyxdsm.XDSM import XDSM

# styling names for the boxes
opt = 'Optimization'
solver = 'MDA'
comp = 'Analysis'
group = 'Metamodel'
func = 'Function'

x = XDSM()

# x.add_system('TSplot', comp, 'T-S plot')

x.add_system('FP', solver, 'Fixed Point', stack=True)

# x.add_system('opt', opt, 'Optimizer')
x.add_system('W', comp, 'Weight Build Up')
# can fade out blocks to allow for emphasis on sub-sections of XDSM
x.add_system('conAnalysis', comp, 'Constrant Analysis')
x.add_system('Tcon', comp, 'Thrust Constraints')
x.add_system('conCurve', func, 'Constraint Curves')

# x.add_system('F', func, r'$F$')
# # stacked can be used to represent multiple instances that can be run in parallel
# x.add_system('G', func, r'$G$', stack=True)

x.add_input('TSplot', r'$S$')
x.connect('TSplot', 'FP', r'$S[i]$')
x.connect('TSplot', 'W', r'$S[i]$')
x.connect('TSplot', 'conAnalysis', r'$S[i]$')
x.connect('TSplot', 'Tcon', r'$S[i]$')
x.connect('FP', 'W', r'$T$[i]')
x.connect('W', 'conAnalysis', r'$\frac{W}{S}$')
x.connect('FP', 'conAnalysis', r'$T[i]$')
x.connect('conAnalysis', 'FP', r'$T[i]$')
x.connect('conAnalysis', 'Tcon', r'$T[i]$', stack=True)
x.connect('Tcon', 'conCurve', r'$\textb{S}, \textb{T}$')
x.connect('Tcon', 'TSplot', r'$i$')

x.add_input('FP', r'Flight Condition')
# x.add_input('FP', r'$S$', stack=True)


# x.connect('opt', 'G', r'$y_1, y_2$', stack=True)

# # x.connect('opt', 'D2', r'$z, y_1$')
# # x.connect('opt', 'F', r'$x, z$')
# # x.connect('opt', 'F', r'$y_1, y_2$')

# # you can also stack variables
# x.connect('opt', 'G', r'$y_1, y_2$', stack=True)

# x.connect('D1', 'opt', r'$\mathcal{R}(y_1)$')
# x.connect('D2', 'opt', r'$\mathcal{R}(y_2)$')


# x.connect('F', 'opt', r'$f$')
# x.connect('G', 'opt', r'$g$', stack=True)

# # can specify inputs to represent external information coming into the XDSM
# x.add_input('D1', r'$P_1$')
# x.add_input('D2', r'$P_2$')

# # can put outputs on the left or right sides
# x.add_output('opt', r'$x^*, z^*$', side='right')
# x.add_output('D1', r'$y_1^*$', side='left')
# x.add_output('D2', r'$y_2^*$', side='left')
# x.add_output('F', r'$f^*$', side='right')
# x.add_output('G', r'$g^*$', side='right')

x.write('ts')


# from pyxdsm.XDSM import XDSM

# #
# opt = 'Optimization'
# solver = 'MDA'
# comp = 'Analysis'
# group = 'Metamodel'
# func = 'Function'

# x = XDSM()

# x.add_system('opt', opt, 'Optimizer')
# x.add_system('solver', solver, 'Newton')
# x.add_system('D1', comp, r'$D_1$')
# x.add_system('D2', comp, r'$D_2$')
# x.add_system('F', func, r'$F$')
# x.add_system('G', func, r'$G$')


# x.connect('opt', 'D1', r'$x, z$')
# x.connect('opt', 'D2', r'$z$')
# x.connect('opt', 'F', r'$x, z$')
# x.connect('solver', 'D1', r'$y_2$')
# x.connect('solver', 'D2', r'$y_1$')
# x.connect('D1', 'solver', r'$\mathcal{R}(y_1)$')
# x.connect('solver', 'F', r'$y_1, y_2$')
# x.connect('D2', 'solver', r'$\mathcal{R}(y_2)$')
# x.connect('solver', 'G', r'$y_1, y_2$')


# x.connect('F', 'opt', r'$f$')
# x.connect('G', 'opt', r'$g$')

# x.add_output('opt', r'$x^*, z^*$', side='left')
# x.add_output('D1', r'$y_1^*$', side='left')
# x.add_output('D2', r'$y_2^*$', side='left')
# x.add_output('F', r'$f^*$', side='left')
# x.add_output('G', r'$g^*$', side='left')
# x.write('mdf')
