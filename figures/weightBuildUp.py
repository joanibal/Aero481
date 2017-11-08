from pyxdsm.XDSM import XDSM

# styling names for the boxes
opt = 'Optimization'
solver = 'MDA'
comp = 'Analysis'
group = 'Metamodel'
func = 'Function'

x = XDSM()


# x.add_system('opt', opt, 'Optimizer')
# x.add_system('Tail', comp, 'Tail Weight')
# x.add_system('Engine', comp, 'Engine Weight')
x.add_system('hist', func, 'Historic Weight')
x.add_system('FP', solver, 'Fixed Point')
x.add_system('Fuel', comp, 'Fuel Weight')
x.add_system('LG', comp, 'Landing Gear Weight')
x.add_system('Build', comp, 'Weight Build Up')

# x.add_system('F', func, r'$F$')
# # stacked can be used to represent multiple instances that can be run in parallel
# x.add_system('G', func, r'$G$', stack=True)

x.add_input('hist', r'$\frac{L}{D}, R, SFC, M$')
x.connect('hist', 'FP', r'$MTOW_{guess}$')
x.connect('FP', 'Fuel', r'$MTOW$')
x.connect('FP', 'LG', r'$MTOW$')

# x.connect('hist', 'Tail', r'$MTOW$')
# x.connect('Tail', 'Build', r'$W_{tail}$')
# x.connect('Engine', 'Build', r'$W_{fuel}$')
x.add_input('Build', r'$W_{LG},W_{Tail}$')

x.connect('Fuel', 'Build', r'$W_{fuel}$')
x.connect('LG', 'Build', r'$W_{LG}$')
x.connect('Build', 'FP', r'$MTOW$')
x.add_output('Build', r'$MTOW$', side='right')

# x.connect('conAnalysis', 'conCurve', r'$\frac{T}{W}$', stack=True)

x.write('weight')

