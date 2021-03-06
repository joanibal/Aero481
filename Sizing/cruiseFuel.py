import os,sys,inspect
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from constants import *
import numpy as np

def cruiseFuel(c, S):  # S must be in [m]
    CD = C_f * (Swet_rest + 2*S)/S + CL_cruise/(np.pi*AR*e)
    cruiseFraction = np.exp(R*c*CD/(speed_kts*CL_cruise))
    ff5_vary = 1/cruiseFraction
    return ff5_vary
