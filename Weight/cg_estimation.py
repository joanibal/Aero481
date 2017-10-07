import numpy as np 
# import constants

#constants from CAD 
# - overestimated because does not account for intersection
# - used for rough estimation
# - constants based on general aviation

Swet_wing = 4466.8470952 #ft^2
Swet_HT = 813.6998538 #ft^2
Swet_VT = 397.8730152 #ft^2
Swet_c = 443.6997602 #ft^2
Swet_fuse = 2389.0744993-110.584 #ft^2

#weight calcuations
w_wing = 2.5*Swet_wing
w_HT = 2.0*Swet_HT
w_VT = 2.0*Swet_VT
w_c = 2.0*Swet_c
w_fuse = 1.4*Swet_fuse

print w_wing, w_HT, w_VT, w_c, w_fuse

# w_0, _, _, _ = calcWeights(constants.R,constants.L_D, constants.SFC, M=constants.machCruise)

w_0 = 94965.0 #lb
w_landing_gear = w_0*0.057 #lb
w_nose_gear = w_landing_gear*0.15 #lb
w_main_gear = 0.85*w_landing_gear/2.0 #lb
w_engine = 16096.3201*1.4 #lb
w_all_else = 0.1*w_0 #lb

print w_nose_gear, w_main_gear, w_engine, w_all_else

print w_wing+w_HT+w_VT+w_c+w_fuse+w_landing_gear+w_engine*2+w_all_else

