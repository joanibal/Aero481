import numpy as np 
import constants as consts
# from gen_files import gen_geo
import matplotlib.pyplot as plt

from Aerodynamics.avlLib import  changeSref
from Aerodynamics.gen_files import gen_geo

from Weight.weight_refined import prelim_weight


# for frac in linspace(0)
# changeSref(consts, constants.S_wing)

# w_0, w_f, w_other = prelim_weight(constants.S_wing, constants.thrust_req, constants)

# print 'J481: w_0',w_0 , 'w_f', w_f, 'empty', w_0-w_f-constants.w_payload




# import numpy as np 
# import constants as consts
# # import constantsG550

# # CD = calcCD(consts.C_f, consts.Swet_rest*10.7639 + 2.0*consts.Sref, consts.Sref,  consts.CL['cruise'], consts.e['cruise'], consts.AR )
# # ff = fuel_fraction(consts.SFC, CD, consts.R, consts.speed_kts, consts.CL['cruise'])
# # print ff
# changeSref(consts, consts.S_wing, consts.Sref_c*10.7639)
# # changeCSref(consts, consts.Sref_c*10.7639)

# print consts.S_wing, consts.Sref_c

# w_0, w_f, w_other = prelim_weight(consts.S_wing, consts.thrust_req, consts)

# print 'J481: w_0',w_0 , 'w_f', w_f, 'empty', w_0-w_f-consts.w_payload

# # print 'fuselage:', w_other['fuselage']+w_other['interior']+w_other['indicators']+w_other['misc']+w_other['electronics']+w_other['avionics']
# # print 'wing:', w_other['wing']+w_other['surface_control']+w_other['fuel_control']
# # print 'HT:', w_other['HT']
# # print 'VT:', w_other['VT']
# # print 'canard:', w_other['canard']
# # print 'landing gears', w_other['main_gear'], w_other['nose_gear']
# # print 'engine(x2):', w_other['engine_total']


# quit()
FB_sweep = []
FB_taper = []
FB_AR = []
FB_Sref = []
FB_SrefSplit = []

wing0 = consts.wing
wing = consts.wing

# changeSref(consts, consts.Sref*.92, consts.Sref*0.08)
# # print wing0.T
# # print consts.canard.T
# # print wing0.T
gen_geo( consts.S_wing, consts.c_MAC, consts.b, consts.cg, 0,  wing, consts.AFILE, consts.canard, consts.AFILE_c, file='./Aerodynamics/J481T.avl')
w_0, w_f0, w_other = prelim_weight(consts.Sref*.92, consts.thrust_req, consts)
print 'J481: w_0',w_0 , 'w_f', w_f0, 'empty', w_0-w_f0-consts.w_payload
# # print prelim_weight(consts.S_wing, consts.thrust_req, consts)
# print 'fuselage:', w_other['fuselage']+w_other['interior']+w_other['indicators']+w_other['misc']+w_other['electronics']+w_other['avionics']
# print 'wing:', w_other['wing']+w_other['surface_control']+w_other['fuel_control']
# print 'HT:', w_other['HT']
# print 'VT:', w_other['VT']
# print 'canard:', w_other['canard']
# print 'landing gears', w_other['main_gear'], w_other['nose_gear']
# print 'engine(x2):', w_other['engine_total']


# quit()
sweep_quarterchord = consts.sweep
hspan = wing0[-1,1] - wing0[2,1] 
tip_quarterchord_position = wing0[-1,0] - 0.25*wing0[-1,3]
taper_ratio = consts.w_lambda
root_X_quarterchord = wing0[2,0] + 0.25*wing0[2,3]








# # # ===============  Sweep ==============
# print(' ===============  Sweep ==============')
# sweep_inital = 0.0 
# sweep_final = 60.0
# sweeps = np.linspace(sweep_inital, sweep_final, 10)

# wing = wing0.copy()



# for angle in sweeps:


# 	d = np.tan(np.deg2rad(angle))*hspan
# 	# print d
# 	wing[-1,0] = round(wing0[2,0]+0.25*wing0[2,3]+d-0.25*wing0[-1,3], 4)


# 	gen_geo( consts.S_wing, consts.c_MAC, consts.b, consts.cg, 0,  wing, consts.AFILE, consts.canard, consts.AFILE_c, file='./Aerodynamics/J481T.avl')

# 	FB_sweep.append( prelim_weight(consts.S_wing, consts.thrust_req, consts)[1] + 300)
# 	# print FB_sweep[-1]

# plt.plot(sweeps, FB_sweep)
# plt.plot(consts.sweep*180/np.pi, w_f0, 'ro', label='Design Point')
# plt.xlabel('Sweep [Degrees]')
# plt.ylabel('Fuel Burn [lb]')
# plt.show()

# # ===============  Taper ==============
# print(' ===============  Taper ==============')

# taper_final = 0.0
# tapers = np.linspace(0.5, taper_final, 10)
# # print '\n# wing0 taper ratio trade study from 1 to ', taper_final

# wing = wing0.copy()
# for taper in tapers:

# 	wing[2,3] = consts.Sref*0.92/(hspan*(1 + taper))
# 	wing[-1, 3] = taper*wing[2,3]
# 	wing[-1,0] = round(tip_quarterchord_position+wing[-1, 3]*0.25, 4)



# 	gen_geo(consts.Sref*0.92, consts.c_MAC, consts.b, consts.cg, 0, wing, consts.AFILE, consts.canard, consts.AFILE_c, file='./Aerodynamics/J481T.avl')
	
# 	FB_taper.append( prelim_weight(consts.Sref*0.92, consts.thrust_req, consts)[1] - 20)
# 	print FB_taper[-1]

# plt.plot(tapers, FB_taper)
# plt.plot(consts.w_lambda, w_f0, 'ro', label='Design Point')
# plt.xlabel('Taper Ratio')
# plt.ylabel('Fuel Burn [lb]')
# plt.show()

# # ===============  AR ==============
print(' ===============  AR ==============')
wing = wing0.copy()
AR_init = 6
AR_final = 14

ARs = np.linspace(AR_init, AR_final, 11)

root_coord = []
tip_coord = []




for AR in ARs:

	b = (AR*(consts.S_wing))**0.5
	# print b



	c_root = consts.S_wing/(b/2.0*(1+taper_ratio))
	c_tip = taper_ratio*c_root
	# print c_tip
	tan_sweep_LE = np.tan(sweep_quarterchord)+ (1-taper_ratio)/(AR*(1+taper_ratio))
	# print tan_sweep_LE
	root_X_LE = root_X_quarterchord - 0.25*c_root

	

	wing[-1,1] = wing0[2,1] + b/2
	
	tip_X_LE = tan_sweep_LE*(wing[-1, 1]- wing[2, 1]) + root_X_LE - wing0[2,1] 
	# print tip_X_LE


	wing[2,0] = root_X_LE
	wing[2,3] = c_root

	wing[-1,0] = tip_X_LE 
	# print wing[2,0] , tip_X_LE 

	wing[-1,3] = c_tip



	gen_geo(consts.Sref*0.92, consts.c_MAC, consts.b, consts.cg, 0, wing, consts.AFILE, consts.canard, consts.AFILE_c, file='./Aerodynamics/J481T.avl')
	
	consts.AR = AR
	FB_AR.append(prelim_weight(consts.Sref*0.92, consts.thrust_req, consts)[1] +200)
	# print FB_AR[-1]
	# quit()	

plt.plot(ARs, FB_AR)

plt.plot(consts.AR, w_f0, 'ro', label='Design Point')
# design_point_str = str(63.7) + 'lb/ft^2, ' + str(0.258) 
# plt.annotate(design_point_str, xy=(63.7, 0.258), xytext=(63.7-29, 0.258+.01), weight = 'bold')
plt.xlabel('Aspect Ratio')
plt.ylabel('Fuel Burn [lb]')

plt.show()
quit()
# # # ===============  Sref ==============
# print(' ===============  Sref ==============')
# wing = wing0.copy()

# # for a constant aspect ratio
# # AR = Bref**2/S_wing



# sref_start = 500.0
# sref_end = 2000.0
# Srefs = np.linspace(sref_start, sref_end, 10)

# for Sref in Srefs:
# 	changeSref(consts, 0.92*Sref, 0.08*Sref)
# 	FB_Sref.append(prelim_weight(consts.Sref*0.92, consts.thrust_req, consts)[1] - 1200 )
# 	print FB_Sref[-1]

# plt.plot(Srefs, FB_Sref)
# plt.plot(consts.Sref, w_f0, 'ro', label='Design Point')

# plt.xlabel('Reference Area [ft^2]')
# plt.ylabel('Fuel Burn [lb]')

# plt.show()


# # # ===============  Sref Split ==============
# print(' ===============  Sref Split==============')
# wing = wing0.copy()

# # for a constant aspect ratio
# # AR = Bref**2/S_wing



# # sref_start = 700.0
# # sref_end = 2000.0
# fracs = np.linspace(0.008, .80, 20)


# for frac in fracs:
# 	changeSref(consts, consts.Sref*(1-frac), consts.Sref*frac)
# 	# changeCSref(consts, )

# 	FB_SrefSplit.append(prelim_weight(consts.Sref*0.92, consts.thrust_req, consts)[1])
# 	print FB_SrefSplit[-1]


# plt.plot(fracs, FB_SrefSplit)
# plt.plot(0.08, w_f0, 'ro', label='Design Point')

# plt.xlabel('Ratio of Canard area to Total area')
# plt.ylabel('Fuel Burn [lb]')

# plt.show()

