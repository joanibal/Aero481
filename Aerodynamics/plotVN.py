# Calculate Flight Envelope

import os,sys,inspect
sys.path.insert(1, os.path.join(sys.path[0], '..'))

# from sympy.solvers import solve
# from sympy import Symbol

import math
import numpy as np
import constants
import matplotlib.pyplot as plt

# Aircraft parameters
M = constants.M
Vk = constants.u_imperial*0.592484				# kts
cruise_altitude = 50000							# Set cruise altitude
gust_altitude = 20000							# Gust envelope at 20,000 ft
rho = 3.64e-4									# 50,000 ft (slugs/ft^3)
rho0 = 12.67e-4									# 20,000 ft (slugs/ft^3)
rho_SL = 23.77e-4								# Sea level density (slugs/ft^3)
convKts2fts = 1.688
g = 32.2										# gravity (ft/s) (non-negative)

C_Lmax = 1.3									# Max CL 
C_Lmin = -0.8									# Without high-lift devices

wing_loading = 62.34							# lbs/ft^2 (Taken from PDR report)
cf = 0.96										# correction factor to account for fuel burn (MTOW correction)
												# notes use 0.96 as start of cruise

g_chord = constants.Sref/(constants.b*3.28084) 	# Sref/b (geometric chord) (ft)
kappa = 0.97									# Assumed estimate from notes
beta = math.sqrt(1-M**2)
sweep_c_2 = 33.47								# Half chord sweep
Cl_alpha = 2*math.pi*constants.AR/(2+math.sqrt(constants.AR**2*(beta/kappa)**2*(1+(math.tan(sweep_c_2)**2)/(beta**2))+4))

# Equivalent airspeed 
V_TAS = Vk
V_EAS = V_TAS*(rho/rho_SL)**(1.0/2)
V_C = V_EAS
V_MO = 1.06*V_C 								# V_MO approximated as 1.06*V_C
V_D = 1.07*V_MO 								# V_D approximated as 1.07*V_MO

print('V_TAS: ' + str(V_TAS))
print('V_EAS: '+ str(V_EAS))
print('V_C: '+ str(V_C))
print('V_MO: '+ str(V_MO))
print('V_D: '+ str(V_D))


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

print('V_A: '+str(V_A))
print('V_S: '+ str(V_S))

# Gust Loads
mu = 2*(wing_loading*cf)/(rho0*g_chord*Cl_alpha*g)
K_g = 0.88*mu/(5.3+mu)

# D, C, B at 20, 000 ft
U_e = [25, 50, 66]		

# Solve roots to determine intersection point (U_e_b)
a = (rho_SL*convKts2fts**2*C_Lmax)/(2*wing_loading*cf)
b = -(K_g*Cl_alpha*U_e[2])/(498*wing_loading*cf)
c = -1
sol1 = (-b+math.sqrt(b**2-4*a*c))/(2*a)
sol2 = (-b-math.sqrt(b**2-4*a*c))/(2*a)
V_B_gustlimit_upper = sol1
if sol1 < 0:
	V_B_gustlimit_upper = sol2

# Solve for U_e_B gust
V_B_loadlimit_upper = (rho_SL*(convKts2fts*V_B_gustlimit_upper)**2*C_Lmax)/(2*cf*wing_loading)
V_B_loadlimit_lower = (-V_B_loadlimit_upper+2)
V_B_gustlimit_lower = (V_B_loadlimit_lower-1)*(498*wing_loading*cf)/(-K_g*Cl_alpha*U_e[2])

# Solve for U_e_C gust
V_C_gustlimit = V_C
V_C_loadlimit_upper = 1 + (K_g*Cl_alpha*U_e[1]*V_C_gustlimit)/(498*wing_loading*cf)
V_C_loadlimit_lower = 1 - (K_g*Cl_alpha*U_e[1]*V_C_gustlimit)/(498*wing_loading*cf)

# Solve for U_e_D gust
V_D_gustlimit = V_D
V_D_loadlimit_upper = 1 + (K_g*Cl_alpha*U_e[0]*V_D_gustlimit)/(498*wing_loading*cf)
V_D_loadlimit_lower = 1 - (K_g*Cl_alpha*U_e[0]*V_D_gustlimit)/(498*wing_loading*cf)


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

plt.text(V_B_gustlimit_upper, V_B_loadlimit_upper+0.1, '$V_{B}$', horizontalalignment='center')
plt.text(V_C_gustlimit, V_C_loadlimit_upper+0.1, '$V_{C}$', horizontalalignment='center')

plt.ylim(-1.5, n_limit_max+0.5)
plt.xlim(0, V_D_gustlimit+50)
plt.xlabel('$V_{EAS}$' + ' (kts)')
plt.ylabel('Load Factor ' + '$n$')
plt.title('V-' + '$n$' + ' at ' + str(gust_altitude) + ' ft')
plt.grid(True)
plt.show()