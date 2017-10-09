# Calculate the Angle of Incidence required

import math
import numpy as np
import matplotlib.pyplot as plt

# Define constants
Sref_main = 201.24
bref_main = 33.89
MAC_main = 6.61
Sref_HT = 36.72
bref_HT = 14.88
MAC_HT = 2.61
Sref_c = 19.99
bref_c = 9.14
MAC_c = 2.45
MTOW = 43075

# Define flight constants at 40,000 ft
W = MTOW*9.81								# Lift equals weight
M = 0.85									# Cruise Mach numnber
T_C = -56.5									# Temperature (Celcius)
T = T_C + 273.15							# Temperature (Kelvin)
p = 18822.69								# Absolute Pressure (Pa)
R = 287										# Gas Constant (J/kgK)
rho = p/(R*T)								# Air Density (kg/m^3)
a = math.sqrt(1.4*R*T)						# Speed of Sound (m/s)
u = M*a 									# Airspeed (m/s)
q = 0.5*rho*u**2							# Dynamic Pressure
print("Airspeed: " + str(u) + " m/s")

# Solve for the desired CL (L=W Assumption)
CL_cruise = math.sqrt(2*W/(rho*u**2*Sref_main))
print("Required Lift CL: " + str(CL_cruise))

# Forced CL at cruise (at 2.5 Deg Pitch up)
CL_cruise = 0.6657

# Cruise angle of attack
print("Required Wing Incidence at Cruise: " + str(-2.1812) + " degrees")

# Solve for longitudinal stability equilibrium (Position taken from nose of aircraft)
Xac_c = 3.594184							# Aerodynamic Center of Canard
Xac_wf = 20.161186							# Aerodynamic Center of Wing (Fuselage Effects Ignored)
Xac_h = 33.721935							# Aerodynamic Center of Tail
Xcg = 17.9873865							# CG Position
Cm_wing = -2.191

# Assume horizontal stabilizer provides lift, given that Cm_wing is negative and CG is ahead of NP
Mac_wf = q*Sref_main*MAC_main*Cm_wing
L_wf = q*Sref_main*CL_cruise

# Use interpolated data from XFOIL to predict lift and drag parameters
AoA = np.linspace(0, 5, 100)
NACA0012CL = 0.116*AoA+3e-17
NACA0012CD = 2e-05*AoA**2+4e-18*AoA+0.0049
D_HT = q*Sref_HT*NACA0012CD
L_HT = q*Sref_HT*NACA0012CL
CL_c = (-Mac_wf+L_wf*(Xac_wf-Xcg)+L_HT*(Xac_h-Xcg))/((Xcg-Xac_c)*(q*Sref_c))
L_c = q*Sref_c*CL_c
alpha_c = (CL_c-3e-17)/0.116
D_c = q*Sref_c*(2e-05*alpha_c**2+4e-18*alpha_c+0.0049)


plt.subplot(131)
plt.plot(AoA, L_HT, label = "Horizontal Stabilizer")
plt.plot(AoA, L_c, label = "Canard")
plt.title('Stabilizer Lift')
plt.xlabel('AoA (deg)')
plt.ylabel('Lift (N)')

plt.subplot(132)
plt.plot(AoA, D_HT, label = "Horizontal Stabilizer")
plt.plot(AoA, D_c, label = "Canard")
plt.title('Horizontal Stabilizer Drag')
plt.xlabel('AoA (deg)')
plt.ylabel('HT Drag (N)')

plt.subplot(133)
plt.plot(AoA, alpha_c)
plt.title('Stabilizer vs. Canard Incidence')
plt.xlabel('AoA (deg)')
plt.ylabel('AoA (deg)')
#plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

plt.show()