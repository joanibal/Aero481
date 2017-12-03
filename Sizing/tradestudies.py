import numpy as np 
import constants as consts
# from gen_files import gen_geo


from Aerodynamics.avlLib import  changeSref
from Aerodynamics.gen_files import gen_geo

from Weight.weight_refined import prelim_weight


# for frac in linspace(0)
# changeSref(consts, constants.S_wing)

# w_0, w_f, w_other = prelim_weight(constants.S_wing, constants.thrust_req, constants)

# print 'J481: w_0',w_0 , 'w_f', w_f, 'empty', w_0-w_f-constants.w_payload

wing0 = consts.wing
sweep_quarterchord = consts.sweep
hspan = wing0[-1,1]
tip_quarterchord_position = wing0[-1,0] - 0.25*wing0[-1,3]

# ===============  Sweep ==============
print(' ===============  Sweep ==============')
sweep_inital = 0.0 
sweep_final = 45.0
wing = wing0



# for angle in np.linspace(sweep_inital, sweep_final, 10):


# 	d = np.tan(np.deg2rad(angle))*hspan
# 	wing[-1,0] = round(wing0[2,0]+0.25*wing0[2,3]+d-0.25*wing0[-1,3], 4)

# 	gen_geo( consts.Sref, consts.c_MAC, consts.b, consts.cg, 0,  wing, consts.AFILE, consts.canard, consts.AFILE_c, file='./Aerodynamics/J481T.avl')

# 	w_0, _, _ = prelim_weight(consts.Sref, consts.thrust_req, consts)
# 	print w_0



# ===============  Taper ==============
# print(' ===============  Taper ==============')

# taper_final = 0.0

# wing = wing0
# print '\n# wing0 taper ratio trade study from 1 to ', taper_final

# for taper in np.linspace(1.0, taper_final, 10):

# 	wing[0,3] = consts.S_wing/(hspan*(1 + taper))
# 	wing[-1, 3] = taper*wing[0,3]
# 	wing[-1,0] = round(tip_quarterchord_position+wing[-1, 3]*0.25, 4)



# 	gen_geo(consts.Sref, consts.c_MAC, consts.b, consts.cg, 0, wing, consts.AFILE, consts.canard, consts.AFILE_c, file='./Aerodynamics/J481T.avl')
	
# 	w_0, _, _ = prelim_weight(consts.Sref, consts.thrust_req, consts)
# 	print w_0


# # ===============  AR ==============
print(' ===============  AR ==============')
wing = wing0
taper_ratio = wing[-1,3]/wing[0,3]
root_X_quarterchord = wing[0,0] + 0.25*wing[0,3]
AR_init = 7
AR_final = 15



# root_coord = []
# tip_coord = []




# for AR in np.linspace(consts.AR_init, AR_final, 10):

# 	b = (AR*(consts.S_wing))**0.5
# 	# print b
# 	c_root = consts.S_wing/(b/2*(1+taper_ratio))
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


# 	gen_geo(consts.Sref, consts.c_MAC, consts.b, consts.cg, 0, wing, consts.AFILE, consts.canard, consts.AFILE_c, file='./Aerodynamics/J481T.avl')
	
# 	w_0, _, _ = prelim_weight(consts.Sref, consts.thrust_req, consts)
# 	print w_0



# # ===============  Sref ==============
print(' ===============  Sref ==============')
wing = wing0

# for a constant aspect ratio
# AR = Bref**2/S_wing



sref_start = 700.0
sref_end = 2000.0

for wingSref in np.linspace(sref_start, sref_end, 10):

	wing[-1, 1] = np.sqrt(consts.AR*wingSref)
	# print 'wing[-1,1]', wing[-1,1]
	wing[0, 0] = wingSref/(wing[-1,1]*(1+taper_ratio))
	# print wing[0, 0]
	# print (wing[-1,1]*(1+taper_ratio))
# 
	root_X_LE = root_X_quarterchord - 0.25*wing[0, 3]
	# print root_X_quarterchord , 0.25*wing[0, 0]
	# quit()
	tan_sweep_LE = np.tan(sweep_quarterchord)+ (1-taper_ratio)/(consts.AR*(1+taper_ratio))

	# print tan_sweep_LE


	tip_X_LE = tan_sweep_LE*wing[-1, 1]*0.5 + root_X_LE


	wing[0,0] = root_X_LE
	# wing[0,3] = c_root

	wing[-1,0] = tip_X_LE
	# wing[-1,1] = b/2

	wing[-1,3] = wing[0, 3]*taper_ratio
	gen_geo(consts.Sref, consts.c_MAC, consts.b, consts.cg, 0, wing, consts.AFILE, consts.canard, consts.AFILE_c, file='./Aerodynamics/J481T.avl')
	
	w_0, _, _ = prelim_weight(consts.Sref, consts.thrust_req, consts)
	print w_0

