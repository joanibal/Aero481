import os,sys,inspect

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import j481 as consts
from Weight.weight_refined import prelim_weight

w_0, w_f, _ = prelim_weight(consts.Sref, consts.thrust_req, consts)
Clmax_t = consts.CL['max']['takeoff']
Clmax_l = consts.CL['max']['landing']

TOP = (w_0/(consts.Sref))/(1*Clmax_t*(consts.thrust_req/w_0))
BFL = 37.5*TOP

ground_roll = 80*(w_0/(consts.Sref))*(1/(1*Clmax_l))
landing_field = 1.67*(ground_roll+1000)

print BFL, ground_roll, landing_field
