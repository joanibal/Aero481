import os,sys,inspect

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import j481
import numpy as np

def landinggear(Na, Nf, Ma, Mf, B, H, W, Wlanding, Vstall):
        #inputs: nose gear position, main gear position, forward CG position, aft CG position, height of CG, MTOW, landing weight, stall speed
        #units: ft, lbs, ft/s


    g = 32.2

    # Na = aftCG-nose
    # Nf = fwdCG-nose
    # Ma = main-aftCG
    # Mf = main-fwdCG
    # B = main-nose

    maxSL = W*Na/B  # max static load
    maxSL_nose = W*Mf/B  # max static load, nose
    minSL_nose = W*Ma/B  # min static load, nose
    DBL_nose = 10*H*W/(g*B)

    wheel_load = 1.07*1.25*maxSL/j481.wheels_main
    wheel_load_nose = 1.07*1.25*DBL_nose/j481.wheels_nose
    KE_braking = 0.5*Wlanding*Vstall**2/(g*j481.wheels_main) #assumes brakes are only on main gear

    #Ma/B and Mf/B are used to confirm landing gear location
    return (Ma/B), (Mf/B), wheel_load, wheel_load_nose, KE_braking

# def static_margin(np, cg, w_mac):
#     # np & cg location from the same datum
#     # keep units consistent
#
#     margin = (np-cg)/w_mac
#     return margin

if __name__ == '__main__':
    # from Weight.weight_buildup import prelim_weight
    from Aerodynamics.calcStall import stallSpeed

    # w_0, w_fuel = prelim_weight(j481.Sref/0.09203, j481.thrust_req, j481)
    w_0 = 55774.0
    print(w_0)
    weight_landing = 0.77*w_0




    Ma_B, Mf_B, wheel_load, wheel_load_nose, KE_brake = landinggear(j481.gear['Na'], j481.gear['Nf'], j481.gear['Ma'], j481.gear['Mf'], j481.gear['B'], j481.gear['H'], w_0, weight_landing, stallSpeed(j481.CL['max']['landing'],weight_landing,j481.density_SL) )
    print Ma_B, Mf_B, wheel_load, wheel_load_nose, KE_brake

    # 27.75x8.75-14.5 tire choice (mains)
    # 13.5x6.0-4 tire choice (nose)
