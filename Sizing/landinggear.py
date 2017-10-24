import os,sys,inspect

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import constants as consts
import numpy as np

def landinggear(nose, main, fwdCG, aftCG, H, W, Wlanding, Vstall):
        #inputs: nose gear position, main gear position, forward CG position, aft CG position, height of CG, MTOW, landing weight, stall speed
        #units: ft, lbs, ft/s


    g = 32.2

    Na = aftCG-nose
    Nf = fwdCG-nose
    Ma = main-aftCG
    Mf = main-fwdCG
    B = main-nose

    maxSL = W*Na/B  # max static load
    maxSL_nose = W*Mf/B  # max static load, nose
    minSL_nose = W*Ma/B  # min static load, nose
    DBL_nose = 10*H*W/(g*B)

    wheel_load = 1.07*1.25*maxSL/consts.wheels_main
    wheel_load_nose = 1.07*1.25*DBL_nose/consts.wheels_nose
    KE_braking = 0.5*Wlanding*Vstall**2/(g*consts.wheels_main) #assumes brakes are only on main gear 

    #Ma/B and Mf/B are used to confirm landing gear location
    return (Ma/B), (Mf/B), wheel_load, wheel_load_nose, KE_braking

def static_margin(np, cg, w_mac):
    # np & cg location from the same datum
    # keep units consistent

    margin = (np-cg)/w_mac
    return margin

if __name__ == '__main__':
    Ma_B, Mf_B, wheel_load, wheel_load_nose, KE_brake = landinggear(consts.nose_x*3.28084, consts.main_x*3.28084, consts.cg_fwd*3.28084, consts.cg_aft*3.28084, consts.cg_h*3.28084, 66111.89, 41190.9325884, consts.v_landingstall )
    print wheel_load, wheel_load_nose, KE_brake