#test pyAVL wrapper
import numpy as np

import pyAVL


# case = pyAVL.avlAnalysis()


case = pyAVL.avlAnalysis(geo_file='aircraft.txt', mass_file ='aircraft.mass')

# case.addConstraint('alpha', 3)
case.addConstraint('D1', 0.00)
case.addConstraint('D2', 0.00)

# case.addTrimCondition('CL', 1.0)
# case.addConstraint('alpha', 0.00)

case.executeRun()

print '----------------- Neutral Point ----------------'
case.calcNP()
print case.NP, ' X Np'
case.resetData()


case.alphaSweep(0, 10)

print '----------------- alpha sweep ----------------'
print '   Angle        Cl           Cd          Cdff          Cdv          Cm'
for i in xrange(len(case.alpha)):
    print ' %10.6f   %10.6f   %10.6f   %10.6f   %10.6f   %10.6f   '%(case.alpha[i]*(180/np.pi),case.CL[i],case.CD[i], case.CDFF[i], case.CDV[i],  case.CM[i])


case.resetData()

case.CLSweep(0.6, 1.6)

print '----------------- CL sweep ----------------'
print '   Angle        Cl           Cd          Cdff          Cdv          Cm'
for i in xrange(len(case.alpha)):
    print ' %10.6f   %10.6f   %10.6f   %10.6f   %10.6f   %10.6f   '%(case.alpha[i]*(180/np.pi),case.CL[i],case.CD[i], case.CDFF[i], case.CDV[i],  case.CM[i])

# print case.control_deflection
# print case.surf_CL

   
 # correct output
# ----------------- Neutral Point ----------------
# 0.379904295282  X Np
# ----------------- alpha sweep ----------------
#    Angle        Cl           Cd          Cdff          Cdv          Cm
#    0.000000     0.938616     0.063291     0.026654     0.011600     0.000000   
#    1.000000     1.011160     0.071276     0.026654     0.011600     0.000000   
#    2.000000     1.083098     0.079784     0.032476     0.011600    -0.000000   
#    3.000000     1.154380     0.088796     0.038813     0.011600     0.000000   
#    4.000000     1.224957     0.098291     0.045658     0.011600     0.000000   
#    5.000000     1.294782     0.108248     0.053001     0.011600    -0.000000   
#    6.000000     1.363809     0.118642     0.060835     0.011600    -0.000000   
#    7.000000     1.431993     0.129449     0.069149     0.011600    -0.000000   
#    8.000000     1.499289     0.140643     0.077934     0.011600     0.000000   
#    9.000000     1.565657     0.152196     0.087179     0.011600     0.000000   
#   10.000000     1.631056     0.164079     0.096872     0.011600    -0.000000   
# ----------------- CL sweep ----------------
#    Angle        Cl           Cd          Cdff          Cdv          Cm
#   -4.580877     0.600000     0.033839     0.026654     0.011600    -0.000000   
#   -3.240347     0.700000     0.041206     0.026654     0.011600     0.000000   
#   -1.890446     0.800000     0.049685     0.032476     0.011600    -0.000000   
#   -0.529164     0.900000     0.059283     0.038813     0.011600    -0.000000   
#    0.845640     1.000000     0.070009     0.045658     0.011600    -0.000000   
#    2.236265     1.100000     0.081868     0.053001     0.011600    -0.000000   
#    3.645202     1.200000     0.094868     0.060835     0.011600    -0.000000   
#    5.075178     1.300000     0.109014     0.069149     0.011600    -0.000000   
#    6.529203     1.400000     0.124311     0.077934     0.011600    -0.000000   
#    8.010633     1.500000     0.140764     0.087179     0.011600    -0.000000   
#    9.523246     1.600000     0.158375     0.096872     0.011600    -0.000000   
