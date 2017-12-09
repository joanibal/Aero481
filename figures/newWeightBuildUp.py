from pyxdsm.XDSM import XDSM

# styling names for the boxes
opt = 'Optimization'
solver = 'MDA'
comp = 'Analysis'
group = 'Metamodel'
func = 'Function'

x = XDSM()


x.add_system('sizing', comp, 'Surfaces Sizing')
x.add_system('CD0', comp, 'Component CD0')
x.add_system('detW', comp, 'Detailed Weights')
x.add_system('resW', comp, 'Regression Weight')
# x.add_system('iter', solver, 'Fixed Point')
x.add_system('buildW', solver, 'Weight Build Up')
x.add_system('stepC', solver, 'Step Cruise')
x.add_system('AVL', func, 'pyAVL')
x.add_system('BR', comp, 'Breguet Range')
# x.add_system('BR', comp, 'Breguet Range')

# x.add_system('F', func, r'$F$')
# # # stacked can be used to represent multiple instances that can be run in parallel
# # x.add_system('G', func, r'$G$', stack=True)

x.add_input('sizing', r'$S_{ref}, T$')
x.connect('sizing', 'CD0', r'$S_{surface}, \overline{C}_{surface}}$' , stack=True)
x.connect('CD0', 'AVL', r'$C_{D0}$' )
# x.connect('CD0', 'detW')

x.connect('detW', 'resW', r'$W_{interior}, W_{engine}$' )
x.connect('resW',  'buildW', r'$MTOW$' )
x.connect('buildW', 'stepC', r'$MTOW$' )


x.connect('stepC',  'AVL', r'$/C_{L, cruise}$' )
x.connect('AVL', 'BR' , r'$\frac{L}{D} $' )
x.connect('BR', 'stepC', r'$W_{Fuel} $' )
x.connect('stepC', 'buildW' , r'$W_{Fuel} $' )

x.add_output('buildW', r'$MTOW$', side='right')

# # x.connect('conAnalysis', 'conCurve', r'$\frac{T}{W}$', stack=True)

x.write('test')

