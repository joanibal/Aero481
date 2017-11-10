import os,sys,inspect

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import Sizing.horizontal_surf_sizing
from Aerodynamics.calcCoeff import *
import Sizing.Svt_calc
import Weight.weight_estimation
import numpy as np
import matplotlib.pyplot as plt

# wing weight calculations
Wt_carichner = (0.00428*Sref_wing**0.48)*((AR*M**0.43)/(100*tc)**0.76)*((MTOW*N)**0.84*w_lambda**0.14)/(np.cos(lambda_half)**1.54)

#horizontal tail calc
gamma_tail = ((MTOW*N)**0.813)*(S_HT**0.584)*((span_h/t_root_h)**0.033)*()
