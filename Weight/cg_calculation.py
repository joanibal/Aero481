import os,sys,inspect

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import constants as consts
import numpy as np
from weight_refined import *

w_0, w_f, w_other = prelim_weight(consts.S_wing, consts.thrust_req, consts)
