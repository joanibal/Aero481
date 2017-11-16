import os,sys,inspect
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import numpy as np 

def sweep_study(root, tip, angle_final, angle_step):
	hspan = tip['Y'] - root['Y'] 
	print '# wing sweep angle trade study from 0 to', angle_final
	for angle in range(0, angle_final, angle_step):
		d = np.tan(np.deg2rad(angle))*hspan
		tip_X = round(root['X']+0.25*root['c']+d-0.25*tip['c'], 4)
		print '#',tip_X, tip['Y'], tip['Z'], tip['c'], tip['Ainc'], tip['Nspan'], tip['Sspace']
	return 0

def taper_study(root, tip, taper_final, taper_step_number):
	tip_quarterchord_position = tip['X'] - 0.25*tip['c']
	print '\n# wing sweep angle trade study from 1 to ', taper_final
	taper = np.linspace(1.0, taper_final, num=taper_step_number)
	for i in range(0, len(taper)):
		tip_c = taper[i]*root['c']
		tip_X = round(tip_quarterchord_position+tip_c*0.25, 4)
		print '#',tip_X, tip['Y'], tip['Z'], tip_c, tip['Ainc'], tip['Nspan'], tip['Sspace']
	return 0

def AR_study(root, tip, Sref_wing, sweep_quarterchord, AR_init, AR_final, AR_step):
	taper_ratio = tip['c']/root['c']
	AR = np.linspace(AR_init, AR_final, AR_step)
	root_X_quarterchord = root['X'] + 0.25*root['c']
	
	root_coord = []
	tip_coord = []

	for i in range(0, len(AR)):
		b = (AR[i]*Sref_wing)**0.5
		# print b
		c_root = 2*Sref_wing/(b*(1+taper_ratio))
		# print c_root
		c_tip = taper_ratio*c_root
		# print c_tip
		tan_sweep_LE = np.tan(sweep_quarterchord)+ (1-taper_ratio)/(AR[i]*(1+taper_ratio))
		# print tan_sweep_LE
		root_X_LE = root_X_quarterchord + 0.25*c_root
		# print root_X_LE
		tip_X_LE = tan_sweep_LE*b*0.5 + root_X_LE
		# print tip_X_LE
		root_coord.append('# '+str(round(root_X_LE,4))+' '+str(root['Y'])+' '+str(root['Z'])+' '+str(round(c_root,4))+' '+str(root['Ainc'])+' '+str(root['Nspan'])+' '+str(root['Sspace']))
		tip_coord.append('# '+str(round(tip_X_LE,4))+' '+str(round(0.5*b,4))+' '+str(tip['Z'])+' '+str(round(c_tip,4))+' '+str(tip['Ainc'])+' '+str(tip['Nspan'])+' '+str(tip['Sspace']))


	print '\n# AR study root coordinates from '+str(round(AR_init,4))+' to '+str(round(AR_final,4))
	for line in root_coord:
		print line
	print '\n# AR study tip coordinates '+str(round(AR_init,4))+' to '+str(round(AR_final,4))
	for line in tip_coord:
		print line

	return 0

def Sref_study(root, tip, sweep_quarterchord, sref_start, sref_end, steps):	
	taper_ratio = tip['c']/root['c'] 
	Sref = np.linspace(sref_start, sref_end, steps)
	print '\n# Sref trade study from', sref_start,'to', sref_end
	for i in range(0, len(Sref)):
		b = 2*Sref[i]/(root['c']*(1+taper_ratio))
		AR = b**2.0/Sref[i]
		tan_sweep_LE = np.tan(sweep_quarterchord)+ (1-taper_ratio)/(AR*(1+taper_ratio))
		print '# '+str(round((tan_sweep_LE*0.5*b)+root['X'], 4))+' '+str(round(0.5*b,4))+' '+str(tip['Z'])+' '+str(tip['c'])+' '+str(tip['Ainc'])+' '+str(tip['Nspan'])+' '+str(tip['Sspace'])

	return 0	

if __name__ == '__main__':
	import constants as consts

	# base case
	#43.7336 0.0000 -2.16535 16.2402 0.0 19 3 (original root)
	root = {'X':43.7336,
			'Y':0.0000,
			'Z':-2.16535,
			'c':16.2402,
			'Ainc':0,
			'Nspan':19,
			'Sspace':3}
	# 75.4948 46.0302 -2.75591 4.22244 -2 19 3 (original tip)
	tip = {'X':75.4948,
		   'Y':46.0302,
		   'Z':-2.75591,
		   'c':4.22244,
		   'Ainc':-2,
		   'Nspan':19,
		   'Sspace':3,}

	sweep_study(root, tip, 40, 2) #final sweep angle & angle step size
	taper_study(root, tip, 0, 20) #taper final & number of steps
	AR_study(root, tip, consts.S_wing, consts.sweep, 1.0, 16.0, 20.0) #start AR & final AR & number of steps
	Sref_study(root, tip, consts.sweep, 900, 2500, 20) #start Sref, end Sref, number of steps