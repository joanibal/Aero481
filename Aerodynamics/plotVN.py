# Calculate Flight Envelope

import os,sys,inspect
sys.path.insert(1, os.path.join(sys.path[0], '..'))

# from sympy.solvers import solve
# from sympy import Symbol

import math
import numpy as np
import constants
import matplotlib.pyplot as plt
from atm import calcATM

# Aircraft parameters
M = constants.M
Vk = constants.u_imperial*0.592484				# kts
cruise_altitude = constants.alt					# Set cruise altitude
_, _, rho = calcATM(cruise_altitude)			# 50,000 ft (slugs/ft^3)
rho = 3.64e-4
gust_altitude = 53000							# Gust envelope at 20,000 ft
_, _, rho0 = calcATM(gust_altitude)				# Gust altitude ft (slugs/ft^3)
rho_SL = 23.77e-4								# Sea level density (slugs/ft^3)
convKts2fts = 1.688
g = 32.2										# gravity (ft/s) (non-negative)

# Clean
C_Lmax = constants.CL['max']['cruise']			# Max CL 
C_Lmin = -0.8									# Without high-lift devices

Sref = constants.Sref
#weight = 55773.7757505						# lbs (mtow) 
weight = 36495.9968901						# lbs (empty)
wing_loading = weight/Sref

# max
cf = 0.96										# correction factor to account for fuel burn (MTOW correction)
# empty											# notes use 0.96 as start of cruise
# cf = 1

g_chord = constants.Sref/(constants.b*3.28084) 	# Sref/b (geometric chord) (ft)
kappa = 0.97									# Assumed estimate from notes
												# Half chord sweep

def cl_a(AR, sweep, M, kappa):
	beta = math.sqrt(1-M**2)
	CL_alpha = 2*math.pi*AR/(2+math.sqrt(AR**2*(beta/kappa)**2*(1+(math.tan(sweep))/(beta**2))+4))
	return CL_alpha

def sweep_c_2(b, sweep, c_root, taper):
	sweep_halfchord = np.arctan((0.5*b*np.tan(sweep)-0.25*c_root+0.25*taper*c_root)/(0.5*b))
	return sweep_halfchord

#CL_alpha = 2*math.pi*constants.AR/(2+math.sqrt(constants.AR**2*(beta/kappa)**2*(1+(math.tan(sweep_c_2)**2)/(beta**2))+4))

# Calculate CL_alpha accounting for canard effects
sweep_c_2_canard = sweep_c_2(constants.span_c, constants.sweep_c, constants.c_root_c, constants.c_lambda)
sweep_c_2_wing = sweep_c_2(constants.b, constants.sweep, constants.c_root, constants.w_lambda)

CL_alpha_canard = cl_a(constants.AR_c, sweep_c_2_canard, constants.M, kappa)
CL_alpha_main_wing_0 = cl_a(constants.AR, sweep_c_2_wing, constants.M, kappa)
# Assuming wing is affected by downwash of canard
depsilon_dalpha_canard = 2*CL_alpha_canard/(math.pi*constants.AR_c)
# Corrected wing lift curve slope
CL_alpha_main_wing = CL_alpha_main_wing_0*(1 - depsilon_dalpha_canard)*0.9

# Calculate total wing (canard + main wing) lift curve slope
canard_fraction = constants.Sref_c_actual/constants.Sref 	# Percent of canard reference area w.r.t total Sref
CL_alpha = CL_alpha_canard*canard_fraction+CL_alpha_main_wing*(1-canard_fraction)

# Equivalent airspeed 
V_TAS = Vk
V_EAS = V_TAS*(rho/rho_SL)**(1.0/2)
V_C = V_EAS
V_MO = 1.06*V_C 								# V_MO approximated as 1.06*V_C
V_D = 1.07*V_MO 								# V_D approximated as 1.07*V_MO

print('V_TAS: ' + str(V_TAS) + ' kts')
print('V_EAS: '+ str(V_EAS) + ' kts')
print('V_C: '+ str(V_C) + ' kts')
print('V_MO: '+ str(V_MO) + ' kts')
print('V_D: '+ str(V_D) + ' kts')


# Max/min stall curves
# Solve for stall speeds and generate stall curves (Flight envelope)
n_limit_max = 2.5								# Limit load factor (FAR)

if wing_loading*constants.Sref < 50000:
	n_limit_max = 2.1+24000/(wing_loading*constants.Sref+10000)
	if n_limit_max > 3.8:
		n_limit_max = 3.8

n_limit_norm = 1.0								# Limit load factor (FAR)


V_A = math.sqrt((2*cf*wing_loading*n_limit_max)/(rho_SL*C_Lmax))/convKts2fts

v_upper = np.linspace(0, V_A)
n_upper = (rho_SL*(convKts2fts*v_upper)**2*C_Lmax)/(2*cf*wing_loading)

n_limit_min = -1
v_lower_limit = math.sqrt((2*cf*wing_loading*n_limit_min)/(rho_SL*C_Lmin))/convKts2fts
v_lower = np.linspace(0, v_lower_limit)
n_lower = (rho_SL*(convKts2fts*v_lower)**2*C_Lmin)/(2*cf*wing_loading)

V_S = math.sqrt((2*cf*wing_loading*n_limit_norm*(-0.5))/(rho_SL*C_Lmin))/convKts2fts
V_S_n_upper = (rho_SL*(convKts2fts*V_S)**2*C_Lmax)/(2*cf*wing_loading)
V_S_n_lower = (rho_SL*(convKts2fts*V_S)**2*C_Lmin)/(2*cf*wing_loading)

print('V_A: '+str(V_A) + ' kts')
print('V_S: '+ str(V_S) + ' kts')

# Gust Loads
# Solve for gust speeds at altitude

b_B = 50000-((50000-20000)/(38-66))*38
b_C = 50000-((50000-20000)/(25-50))*25
b_D = 50000-((50000-20000)/(12.5-25))*12.5

U_e = [25, 50, 66]								# Default 20,000 ft

if gust_altitude < 50000 and gust_altitude > 20000:
	U_e[2] = (gust_altitude-b_B)/((50000-20000)/(38-66))
	U_e[1] = (gust_altitude-b_B)/((50000-20000)/(25-50))
	U_e[0] = (gust_altitude-b_B)/((50000-20000)/(12.5-25))
elif gust_altitude >= 50000:
	U_e[2] = 38
	U_e[1] = 25
	U_e[0] = 12.5

print('\nGust velocities at ' + str(gust_altitude) + ' ft')
print('V_B (rough gust): ' + str(U_e[2]) + ' kts') 
print('V_C (gust at max design speed): ' + str(U_e[1]) + ' kts')
print('V_D (gust at max dive speed): ' + str(U_e[0]) + ' kts')

mu = 2*(wing_loading*cf)/(rho0*g_chord*CL_alpha*g)
K_g = 0.88*mu/(5.3+mu)

# Solve roots to determine intersection point (U_e_b)
a = (rho_SL*convKts2fts**2*C_Lmax)/(2*wing_loading*cf)
b = -(K_g*CL_alpha*U_e[2])/(498*wing_loading*cf)
c = -1
sol1 = (-b+math.sqrt(b**2-4*a*c))/(2*a)
sol2 = (-b-math.sqrt(b**2-4*a*c))/(2*a)
V_B_gustlimit_upper = sol1
if sol1 < 0:
	V_B_gustlimit_upper = sol2

# Solve for U_e_B gust
V_B_loadlimit_upper = (rho_SL*(convKts2fts*V_B_gustlimit_upper)**2*C_Lmax)/(2*cf*wing_loading)
V_B_loadlimit_lower = (-V_B_loadlimit_upper+2)
V_B_gustlimit_lower = (V_B_loadlimit_lower-1)*(498*wing_loading*cf)/(-K_g*CL_alpha*U_e[2])

# Solve for U_e_C gust
V_C_gustlimit = V_C
V_C_loadlimit_upper = 1 + (K_g*CL_alpha*U_e[1]*V_C_gustlimit)/(498*wing_loading*cf)
V_C_loadlimit_lower = 1 - (K_g*CL_alpha*U_e[1]*V_C_gustlimit)/(498*wing_loading*cf)

# Solve for U_e_D gust
V_D_gustlimit = V_D
V_D_loadlimit_upper = 1 + (K_g*CL_alpha*U_e[0]*V_D_gustlimit)/(498*wing_loading*cf)
V_D_loadlimit_lower = 1 - (K_g*CL_alpha*U_e[0]*V_D_gustlimit)/(498*wing_loading*cf)


# Plot the v-n diagram
plt.plot()

#Plot flight envelope
x1, y1 = [V_A, V_D], [n_limit_max, n_limit_max]							# Plot horizontal line between VA and VD
x2, y2 = [V_D, V_D], [n_limit_max, 0]									# Plot vertical line bounded by VD
x3, y3 = [V_D, V_C], [0, -1] 											# Plot linear relationship between VD and VC
x4, y4 = [v_lower_limit, V_C], [n_limit_min, n_limit_min]				# Plot horizontal line between lower stall curve and VC
x5, y5 = [V_S, V_S], [V_S_n_lower, V_S_n_upper]							# Plot the vertical stall speed VC

plt.plot(v_upper, n_upper, color = 'k', linewidth= 2.0)					# Plot upper stall curve
plt.plot(v_lower, n_lower, color = 'k', linewidth= 2.0)					# Plot lower stall curve
plt.plot(x1, y1, color = 'k', linewidth = 2.0)
plt.plot(x2, y2, color = 'k', linewidth = 2.0)
plt.plot(x3, y3, color = 'k', linewidth = 2.0)
plt.plot(x4, y4, color = 'k', linewidth = 2.0)
plt.plot(x5, y5, color = 'k', linewidth = 2.0)

plt.text(V_A, n_limit_max+0.1, '$V_{A}$', horizontalalignment='center')
plt.text(V_D, n_limit_max+0.1, '$V_{D}$', horizontalalignment='center')
plt.text(V_S, V_S_n_upper+0.1, '$V_{S}$', horizontalalignment='center')
#plt.text(V_C_gustlimit, n_limit_min-0.15, '$V_{C}$', horizontalalignment='center')

# Plot gust envelope
x6, y6 = [0, V_B_gustlimit_upper], [1, V_B_loadlimit_upper]				# Upper and lower gusts V_B
x7, y7 = [0, V_B_gustlimit_lower], [1, V_B_loadlimit_lower]
x8, y8 = [0, V_C_gustlimit], [1, V_C_loadlimit_upper]					# Upper and lower gusts V_C
x9, y9 = [0, V_C_gustlimit], [1, V_C_loadlimit_lower]
x10, y10 = [0, V_D_gustlimit], [1, V_D_loadlimit_upper]					# Uppe rand lower gusts V_D
x11, y11 = [0, V_D_gustlimit], [1, V_D_loadlimit_lower]
x12, y12 = [V_B_gustlimit_upper, V_C_gustlimit], [V_B_loadlimit_upper, V_C_loadlimit_upper]		# Fill gust envelope
x13, y13 = [V_C_gustlimit, V_D_gustlimit], [V_C_loadlimit_upper, V_D_loadlimit_upper]
x14, y14 = [V_D_gustlimit, V_D_gustlimit], [V_D_loadlimit_upper, V_D_loadlimit_lower]
x15, y15 = [V_D_gustlimit, V_C_gustlimit], [V_D_loadlimit_lower, V_C_loadlimit_lower]
x16, y16 = [V_C_gustlimit, V_B_gustlimit_lower], [V_C_loadlimit_lower, V_B_loadlimit_lower]

plt.plot(x6, y6, color = 'r', linestyle = '--' , linewidth = 2.0) 
plt.plot(x7, y7, color = 'r', linestyle = '--' , linewidth = 2.0)
plt.plot(x8, y8, color = 'b', linestyle = '--' , linewidth = 2.0) 
plt.plot(x9, y9, color = 'b', linestyle = '--' , linewidth = 2.0)
plt.plot(x10, y10, color = 'b', linestyle = '--' , linewidth = 2.0) 
plt.plot(x11, y11, color = 'b', linestyle = '--' , linewidth = 2.0) 
plt.plot(x12, y12, color = 'r', linewidth = 2.0) 
plt.plot(x13, y13, color = 'r', linewidth = 2.0) 
plt.plot(x14, y14, color = 'r', linewidth = 2.0) 
plt.plot(x15, y15, color = 'r', linewidth = 2.0) 
plt.plot(x16, y16, color = 'r', linewidth = 2.0)

plt.text(V_B_gustlimit_upper, V_B_loadlimit_upper+0.15, '$V_{B}$', horizontalalignment='center')
plt.text(V_C_gustlimit, V_C_loadlimit_upper+0.1, '$V_{C}$', horizontalalignment='center')

plt.ylim(-1.5, n_limit_max+0.5)
plt.xlim(0, V_D_gustlimit+50)
plt.xlabel('$V_{EAS}$' + ' (kts)')
plt.ylabel('Load Factor ' + '$n$')
plt.title('V-' + '$n$' + ' at ' + str(gust_altitude) + ' ft')
#plt.grid(True)
plt.show()