import pyAVL
import numpy as np
import matplotlib.pyplot as plt
from gen_files import gen_geo


# settup inital conditions
# aircraft parameters
Sref = 1060
MAC = 14.63
Bref = 92.02

cg = [51.44619, 0, 0]
 
CDp = 0

Xle = [41.8333, 45.19918, 58.663, 75.4948]
Yle = [0, 7.14237, 24.42585, 46.0302]
C = [15.0591, 13.975434, 9.64077, 4.22244]



gen_geo(Sref, MAC, Bref, cg, CDp, Xle, Yle, C, Xle_c, Yle_c, C_c)
    

quit()

# for sweep in xrange


# for taper in xrange




# for area in range 


# for 





case = pyAVL.avlAnalysis(geo_file='aircraft.txt', mass_file = 'aircraft.mass')





# Steady level flight contraints
case.addConstraint('elevator', 0.00)
case.addConstraint('rudder', 0.00)

# Execute the case
case.executeRun()

# Calculate the neutral point
case.calcNP()
NP = case.NP

case.clearVals()

# Create a sweep over angle of attack
# case.alphaSweep(-15, 30, 2)
case.alphaSweep(-15, 15, 4)

alpha = case.alpha
sec_CL = case.sec_CL
sec_Yle = case.sec_Yle
sec_Chord = case.sec_Chord
velocity = case.velocity

# get func for aero coeificent
CL = np.poly1d(np.polyfit(case.alpha,case.CL, 1))
CD = np.poly1d(np.polyfit(case.alpha,case.CD, 2))
CM = np.poly1d(np.polyfit(case.alpha,case.CM, 2))

# ----------------- Plot Outputs --------------------------
plt.figure(4)
plt.subplot(411)
plt.ylabel('CL')
plt.xlabel('Alpha')
plt.plot( np.degrees(case.alpha), case.CL, 'b-o')

plt.subplot(412)
plt.xlabel('CD')
plt.ylabel('CL')
plt.plot( case.CD, case.CL, 'b-o')


plt.subplot(413)
plt.ylabel('CM')
plt.xlabel('Alpha')
plt.plot(np.degrees(case.alpha), case.CM, 'b-o')


plt.subplot(414)
plt.ylabel('Elvator Deflection')
plt.xlabel('Alpha')
plt.plot(np.degrees(case.alpha), case.elev_def, 'b-o')

plt.show()
print("NP = %f"% NP)
print("Max Elevator deflection = %f deg" % max(case.elev_def))
