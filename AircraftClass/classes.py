
import numpy as np


class surface(object):
    """
        class used to hold information about the all the surfaces of the plane
    """   

    def __init__(self, area, aspect_ratio, taper, sweep, \
                offset=np.array([0, 0, 0]),  twist=np.array([0,0]),\
                airfoil_file=None , num_sections=2, finish='smoothPaint',\
                Xmaxt=0.4, thickness_chord=0.1, interfernce_factor=1.0,\
                frac_laminar=0.0, vertical=False ):


        self.num_sections = num_sections
        self.twist= twist
        self.offset = offset
        self.airfoil_file = airfoil_file

        self.finish= finish
        self.Xmaxt= Xmaxt
        self.thickness_chord= thickness_chord
        self.interfernce_factor= interfernce_factor
        self.frac_laminar= frac_laminar
        self.vertical = vertical

        self.Nspan = 6
        self.Sspace = 0
        self.angle_incidence = 0 



        self._reset(area, aspect_ratio, taper, sweep)




    def update(self, area=None, aspect_ratio=None, taper=None, sweep=None):
        '''
            reinitlizes surface for the parameters
            
            # called like this

            #to change size
            j481.wing.update(area=1000)

        '''
        if area is None:
            area = self.area

        if aspect_ratio is None:
            aspect_ratio = self.aspect_ratio

        if taper is None:
            taper = self.taper

        if sweep is None:
            sweep = self.sweep


        self._reset(area, aspect_ratio , taper, sweep)
        return 

    def _genCoordinates(self):
        '''
            used to create the AVL coordinates for a surface 
        '''

        coords = np.array([self.offset[0],              self.offset[1],  self.offset[2], self.chord_root,self.twist[0], self.Nspan, self.Sspace])
        if self.vertical:
            xtip = self.offset[0] + (1 - self.taper)*self.chord_root/4 + self.span*np.sin(np.deg2rad(self.sweep))

            self.coords = np.vstack( (coords, np.array([ xtip,  self.offset[1], self.span + self.offset[2], self.chord_root*self.taper , self.twist[1], self.Nspan, self.Sspace]) ) )
        else:
            xtip = self.offset[0] + (1 - self.taper)*self.chord_root/4 + self.span/2*np.sin(np.deg2rad(self.sweep))
            self.coords = np.vstack( (coords, np.array([ xtip, self.span/2 + self.offset[1], self.offset[2], self.chord_root*self.taper , self.twist[1], self.Nspan, self.Sspace]) ) )
        return  


    def _setMAC(self):
        '''
            updates the MAC of the surface
        '''
        self.MAC_y = 2.0/3.0*self.chord_root*(1.0+self.taper+self.taper**2)/(1.0+self.taper)
        self.MAC_c = self.span/6.0*(1.0+2.0*self.taper)/(1.0+self.taper)
        return

    def _reset(self, area, aspect_ratio, taper, sweep):
        self.area = area
        self.aspect_ratio = aspect_ratio    
        self.taper = taper
        self.sweep = sweep


        self.span = np.sqrt(area*aspect_ratio)
        
        self.chord_root = 2*self.area/(self.span*(1 + self.taper))
            

        self.wetted_area = 2*self.area

        # Calculate the mean aerodynamic chord 
        self._setMAC()
        self._genCoordinates()


        self.approx_AC_x = self.coords[0,0]+self.MAC_y*np.sin(np.deg2rad(self.sweep))

        
        return


# python is real dumb and you can't add fields to object sssoooo...
class Object(object):
    pass

