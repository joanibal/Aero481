#calculate Cd0 using the component build up method
import os,sys,inspect

sys.path.insert(1, os.path.join(sys.path[0], '..'))
import math
import numpy as np
import matplotlib.pyplot as plt
from Weight.weight_estimation import calcWeights
import constants

Rkva = 50
fuse_length = constants.fuse_length
La = fuse_length
numEngines = constants.numEngines
Ngen = numEngines

surfaces = {
            'fuselage':{
                        'charLeng':101.17, 				# ft
                        'diameter':8.8,  				# ft
                        'interferenceFactor': 1.0,
                        'swet':2323.66 					# ft^2
                        },
            'wing':{
                        'charLeng':3.17, 				# ft
                        't/c':0.12,
                        'Xmaxt/c':0.4,
                        'interferenceFactor': 1.0,
                        'swet': 1746.54 				# ft^2
                        },
            'vTail':{
                        'charLeng':3.09, 				# ft
                        't/c':0.12,
                        'Xmaxt/c':0.4,
                        'interferenceFactor': 1.0,
                        'swet': 252.18 					# ft^2
                        },
            'hTail':{
                        'charLeng':1.79,
                        't/c':0.12,
                        'Xmaxt/c':0.4,
                        'interferenceFactor': 1.0,
                        'swet': 216.24 					# ft^2
                        },
            'canard':{
                        'charLeng':1.79,
                        't/c':0.12,
                        'Xmaxt/c':0.4,
                        'interferenceFactor': 1.0,
                        'swet': 267.4 					# ft^2.
                        },
            'nacelle':{
                        'charLeng':12.5,
                        'diameter':4.83,
                        'interferenceFactor': 1.0,
                        'swet': 215.58 					# ft^2
                        }
             }


skinRoughness = {
				'camPaint': 3.3e-5,
				'smoothPaint': 2.08e-5,
				'producitonSM': 1.33e-5,
				'polishedSM': 0.50e-5,
				'smoothComp': 0.17e-5
}

# Reynolds number breakdown
# Cruise conditions (40k ft)
rho = constants.rho_imperial			# slugs/ft3
U = constants.u_imperial				# ft/s
mu = 2.969e-7							# lb s/ft^2
M = constants.M

# Fuselage with smooth paint (all turbulent)
Rfuse = rho*U*surfaces['fuselage']['charLeng']/mu
Rfuse_cutoff = 44.62*(surfaces['fuselage']['charLeng']/skinRoughness['smoothPaint'])**1.053*M**1.16

Re_fuse = Rfuse
if Rfuse_cutoff < Rfuse:
	Re_fuse = Rfuse_cutoff

Cf_fuse = 0.455/((math.log10(Re_fuse)**2.58)*(1+0.144*M**2)**0.65)

# Wing, vtail, htail, and canard (15% laminar, 85% turbulent)
# Wing (Polished Sheet Metal)
Rwing = rho*U*surfaces['wing']['charLeng']/mu
Rwing_laminar_cutoff = 32.21*(surfaces['wing']['charLeng']/skinRoughness['polishedSM'])**1.053
Rwing_turbulent_cutoff = 44.62*(surfaces['wing']['charLeng']/skinRoughness['polishedSM'])**1.053*M**1.16

# Vertical Tail (Smooth paint)
RvTail = rho*U*surfaces['vTail']['charLeng']/mu
RvTail_laminar_cutoff = 32.21*(surfaces['vTail']['charLeng']/skinRoughness['smoothPaint'])**1.053
RvTail_turbulent_cutoff = 44.62*(surfaces['vTail']['charLeng']/skinRoughness['smoothPaint'])**1.053*M**1.16

# Horizontal Tail (Polished Sheet Metal)
RhTail = rho*U*surfaces['hTail']['charLeng']/mu
RhTail_laminar_cutoff = 32.21*(surfaces['hTail']['charLeng']/skinRoughness['polishedSM'])**1.053
RhTail_turbulent_cutoff = 44.62*(surfaces['hTail']['charLeng']/skinRoughness['polishedSM'])**1.053*M**1.16

# Canard (Polished Sheet Metal)
Rcanard = rho*U*surfaces['canard']['charLeng']/mu
Rcanard_laminar_cutoff = 32.21*(surfaces['canard']['charLeng']/skinRoughness['polishedSM'])**1.053
Rcanard_turbulent_cutoff = 44.62*(surfaces['canard']['charLeng']/skinRoughness['polishedSM'])**1.053*M**1.16

# Calculate component skin friction
Re_wing_laminar = Rwing
Re_wing_turbulent = Rwing
Re_vTail_laminar = RvTail
Re_vTail_turbulent = RvTail
Re_hTail_laminar = RhTail
Re_hTail_turbulent = RhTail
Re_canard_laminar = Rcanard
Re_canard_turbulent = Rcanard

if Rwing_laminar_cutoff < Rwing:
	Re_wing_laminar = Rwing_laminar_cutoff
if Rwing_turbulent_cutoff < Rwing:
	Re_wing_turbulent = Rwing_turbulent_cutoff
if RvTail_laminar_cutoff < RvTail:
	Re_vTail_laminar = RvTail_laminar_cutoff
if RvTail_turbulent_cutoff < RvTail:
	Re_vTail_turbulent = RvTail_laminar_cutoff
if RhTail_laminar_cutoff < RhTail:
	Re_hTail_laminar = RhTail_laminar_cutoff
if RhTail_turbulent_cutoff < RhTail:
	Re_hTail_turbulent = RhTail_laminar_cutoff
if Rcanard_laminar_cutoff < Rcanard:
	Re_canard_laminar = Rcanard_laminar_cutoff
if Rcanard_turbulent_cutoff < Rcanard:
	Re_canard_turbulent = Rcanard_laminar_cutoff

Cf_wing_laminar = 1.328/math.sqrt(Re_wing_laminar)*0.15
Cf_wing_turbulent = 0.455/((math.log10(Re_wing_turbulent))**2.58*(1+0.144*M**2)**0.65)*0.85

Cf_vTail_laminar = 1.328/math.sqrt(Re_vTail_laminar)*0.15
Cf_vTail_turbulent = 0.455/((math.log10(Re_vTail_turbulent))**2.58*(1+0.144*M**2)**0.65)*0.85

Cf_hTail_laminar = 1.328/math.sqrt(Re_hTail_laminar)*0.15
Cf_hTail_turbulent = 0.455/((math.log10(Re_hTail_turbulent))**2.58*(1+0.144*M**2)**0.65)*0.85

Cf_canard_laminar = 1.328/math.sqrt(Re_canard_laminar)*0.15
Cf_canard_turbulent = 0.455/((math.log10(Re_canard_turbulent))**2.58*(1+0.144*M**2)**0.65)*0.85

Cf_wing = Cf_wing_laminar+Cf_wing_turbulent
Cf_vTail = Cf_vTail_laminar+Cf_vTail_turbulent
Cf_hTail = Cf_hTail_laminar+Cf_hTail_turbulent
Cf_canard = Cf_canard_laminar+Cf_canard_turbulent

# Nacelle with smooth paint (all turbulent)
Rnacelle = rho*U*surfaces['nacelle']['charLeng']/mu
Rnacelle_cutoff = 44.62*(surfaces['nacelle']['charLeng']/skinRoughness['smoothPaint'])**1.053*M**1.16

Re_nacelle = Rnacelle
if Rnacelle_cutoff < Rnacelle:
	Re_nacelle = Rnacelle_cutoff

Cf_nacelle = 0.455/((math.log10(Re_nacelle)**2.58)*(1+0.144*M**2)**0.65)

# Calculate component Form Factor
# Fuselage
f_fuse = surfaces['fuselage']['charLeng']/(math.sqrt((4/math.pi)*(math.pi*(surfaces['fuselage']['diameter']/2)**2)))
FF_Fuse = (1+60/f_fuse**3+f_fuse/400)

# Nacelle
f_nacelle = surfaces['nacelle']['charLeng']/(math.sqrt((4/math.pi)*(math.pi*(surfaces['nacelle']['diameter']/2)**2)))
FF_nacelle = (1+0.35/f_nacelle)

# Main wing, vertical tail, horizontal tail, and canard
FF_wing = (1+(0.6/surfaces['wing']['Xmaxt/c'])*surfaces['wing']['t/c'])+100*(surfaces['wing']['t/c']**4)\
			*(1.34*M**0.18*(math.cos(constants.sweep))**0.28)
FF_vTail = (1+(0.6/surfaces['vTail']['Xmaxt/c'])*surfaces['vTail']['t/c'])+100\
			*(surfaces['vTail']['t/c']**4)*(1.34*M**0.18*(math.cos(constants.sweep_VT*0.0174533))**0.28)
FF_hTail = (1+(0.6/surfaces['hTail']['Xmaxt/c'])*surfaces['hTail']['t/c'])+100\
			*(surfaces['hTail']['t/c']**4)*(1.34*M**0.18*(math.cos(constants.sweep_HT*0.0174533))**0.28)
FF_canard = (1+(0.6/surfaces['canard']['Xmaxt/c'])*surfaces['canard']['t/c'])+100\
			*(surfaces['canard']['t/c']**4)*(1.34*M**0.18*(math.cos(constants.sweep_c*0.0174533))**0.28)

# Interference factor (in surfaces dictionary)

# Missing Form Drag (da = drag area (D\q))
empennage_upsweep = 6.08853*0.0174533														# rad
da_fuse = 3.83*empennage_upsweep**2.5*(math.pi*(surfaces['fuselage']['diameter']/2)**2)
# regular wheel and tire, in tandem, and round strut (for nose, and two aft main gears)
da_lg = (0.25+0.15+0.30)*3
# 4.5 sq ft for main landing gear

da_engine_windmill = (0.3*math.pi*(surfaces['nacelle']['diameter']/2)**2)*2					# engine windmilling effects
CD_mis = (da_fuse+da_lg+da_engine_windmill)/constants.Sref

# NOTE: Need to include speed brakes, spoilers, and bluff surface form drag

# Flap induced CD0
delCd0_flap_takeoff = 0.0023*(0.40)*(15)			# 15 degree takeoff flap deflection
delCd0_flap_cruise = 0.0023*(0.40)*(0)				# 0 degree cruise flap deflection
delCd0_flap_landing = 0.0023*(0.40)*(40)			# 40 degree landing flap deflection

# Calculate Cd0 estimate using component build-up method
sumComponents = Cf_fuse*FF_Fuse*surfaces['fuselage']['interferenceFactor']*surfaces['fuselage']['swet'] + \
				Cf_wing*FF_wing*surfaces['wing']['interferenceFactor']*surfaces['wing']['swet'] + \
				Cf_vTail*FF_vTail*surfaces['vTail']['interferenceFactor']*surfaces['vTail']['swet'] + \
				Cf_hTail*FF_hTail*surfaces['hTail']['interferenceFactor']*surfaces['hTail']['swet'] + \
				Cf_canard*FF_canard*surfaces['canard']['interferenceFactor']*surfaces['canard']['swet'] + \
				Cf_nacelle*FF_nacelle*surfaces['nacelle']['interferenceFactor']*surfaces['nacelle']['swet']*2

Cd0 = sumComponents/constants.Sref+CD_mis
Cd0 = Cd0 + Cd0*(3.5/100) 							# Account for Leak and Protuberance Drag
print("Parasitic Drag: " + str(Cd0))