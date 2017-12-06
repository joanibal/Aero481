import os,sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))



import numpy as np
from AircraftClass.classes import surface


def genTail(wing, dist_to_surface, vol_coeff=np.array([0.66, 0.041]), canard=None):
    '''
        fuction to generate an approperatly sized tail 
        inputs:
            wing: surface()
                main wing which the tail will be used to trim
            dist_to_surface: np.array([], dtype=double)
                distance from the aerodynamic center of the tail to
                 the aerodynamic center of the horizontal tail and vertical.
                 The order is horizonatal, vertical 
            vol_coeff: np.array([], dtype=double)
                volume coefficents use for tail sizing. defaults are 
                the g550 values. The order is horizonatal then vertical 
            canard: surface()
                used to calculation of tail size

        returns:
            tail: surface()
                an appropreately sized tail object
    '''
    AR_horz = 4
    AR_vert = 1.5

    taper_vert = 0.8
    taper_horz = 0.35

    # used to provent shock induced speration on the control surfaces
    sweep_margin = 2


    # add distance to canard to dist_to_surface
    dist_to_surface = np.append(dist_to_surface, [ wing.approx_AC_x - canard.approx_AC_x])


    #finds total required area
    S_total_horz_tail = vol_coeff[0]*wing.MAC_c*wing.area/dist_to_surface[0]
    
    if not(canard is None):
        S_horz_tail =(S_total_horz_tail*dist_to_surface[0] - canard.area*dist_to_surface[2])/dist_to_surface[0]
    else:
        S_horz_tail = S_total_horz_tail
    

    S_vert_tail = vol_coeff[1]*wing.span*wing.area/dist_to_surface[1]



    tail_vert = surface( S_vert_tail, AR_vert, taper_vert, (wing.sweep + sweep_margin), offset=np.array([0, 0, 0]),  \
                airfoil_file='Aerodynamics/Airfoils/sc0012.dat', finish='smoothPaint',\
                thickness_chord=0.12, frac_laminar=0.35, vertical=True )


    tail_horz = surface( S_horz_tail, AR_horz, taper_horz, (wing.sweep + sweep_margin), offset=np.array([0, 0, 0]),  \
                airfoil_file='Aerodynamics/Airfoils/sc0012.dat', finish='smoothPaint',\
                thickness_chord=0.12, frac_laminar=0.35 )

    
    # move the surface into place once there an estimate of the AC location on each surface
    tail_vert.offset= np.array([ wing.approx_AC_x + dist_to_surface[1] - tail_vert.approx_AC_x, 0, wing.coords[0,1] ])
    tail_vert.update()

    tail_horz.offset= np.array([ wing.approx_AC_x + dist_to_surface[0] - tail_horz.approx_AC_x, 0, tail_vert.coords[1,2] ])
    tail_horz.update()


    return tail_vert, tail_horz
