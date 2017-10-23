#Calculate the Critical Mach Number for Airfoil

import os,sys,inspect

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from sympy.solvers import solve
from sympy import Symbol
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
import math
import numpy as np
import constants

a = constants.a
gamma = 1.4 			#Cp/Cv (ideal)
M_cruise = constants.M

#Calculate Reynolds Number at Cruise
rho = constants.rho
D = constants.c_root
mu = 2.995e-7*47.88026
U = constants.u
Re = rho*U*D/mu
print("Re (Root Chord):" + str(Re))

#XFOIL minimum Cp at Alpha = 0
cp_0 = -0.9965
cpmin = cp_0/math.sqrt(1-M_cruise**2)
cpcrit = cpmin
func = lambda M : 2/(gamma*M**2)*(((1+((gamma-1)/2)*M**2)/(1+(gamma-1)/2))**(gamma/(gamma-1))-1)-cpcrit
M_guess = 1
M_solution = fsolve(func, M_guess)

print("Critical Mach Number: " + str(M_solution))