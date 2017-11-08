from pyxdsm.XDSM import XDSM

# styling names for the boxes
opt = 'Optimization'
solver = 'MDA'
comp = 'Analysis'
group = 'Metamodel'
func = 'Function'

x = XDSM()


# x.add_system('opt', opt, 'Optimizer')
x.add_system('W', comp, 'Weight Estimate')
x.add_system('Drag', comp, 'Drag Polar')
x.add_system('conAnalysis', comp, 'Constrant Analysis', stack=True)
x.add_system('conCurve', func, 'Constraint Curves')

# x.add_system('F', func, r'$F$')
# # stacked can be used to represent multiple instances that can be run in parallel
# x.add_system('G', func, r'$G$', stack=True)

x.add_input('conAnalysis', r'$\frac{W}{S}$')
x.connect('W', 'Drag', r'$MTOW$')
x.connect('Drag', 'conAnalysis', r'$C_{D0}, k$')
x.connect('conAnalysis', 'conCurve', r'$\frac{T}{W}$', stack=True)

x.write('tW')

