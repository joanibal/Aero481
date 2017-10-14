# class Aircraft(object):
# 	def __init__(self):
#         pass

class surface(object):
    """
    """   

    def __init__(self, chord_root, taper, span):
        self.span = span	
        self.taper = taper
        self.chord = {}
        self.chord['root'] = chord_root
        self.chord['tip'] = chord_root*taper

        # Calulate surface reference area
        self.Sref = self.calcSref()
       
       # Calculate the mean aerodynamic chord 
        self.MAC, self.yMAC  = self.calcMAC()
        # self.dihedral = dihedral				# dihedral angle (degrees)
        # self.sweep = sweep						# sweep (quarter chord in degrees)


    def calcSref(self):
        return 2* self.span/2*(self.chord['root'] + self.chord['tip'])

    def calcMAC(self):
        c_MAC = 2.0/3.0*self.chord['root']*(1.0+self.taper+self.taper**2)/(1.0+self.taper)
        y_MAC = self.span/6.0*(1.0+2.0*self.taper)/(1.0+self.taper)
        return c_MAC, y_MAC


if __name__ == '__main__':
    import os,sys,inspect

    sys.path.insert(1, os.path.join(sys.path[0], '..'))
    import constants as consts

    tail = surface(consts.L_HT, consts.taper_HT, consts.c_root_HT)
    print tail.Sref, tail.MAC