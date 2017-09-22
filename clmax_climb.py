from cl_calc import *

def clmax_climb(wingloading, segment):

    C_l = cl_calc(wingloading)

    if segment == 1:
        ks = 1.2
    elif segment == 2:
        ks = 1.15
    elif segment == 3:
        ks = 1.2
    elif segment == 4:
        ks = 1.25
    elif segment == 5:
        ks = 1.3
    else:
        ks = 1.5

    clmax = C_l*ks**2

    return clmax
