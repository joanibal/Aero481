'''
pyAVL

pyAVL is a wrapper for Mark Drela's AVL code. The purpose of this
class is to provide an easy to use wrapper for avl for intergration
into other projects. 

Developers:
-----------
- Josh Anibal (JLA)

History
-------
    v. 1.0 - Initial Class Creation (JLA, 08 2016)
    v. 1.1 - Added CDFF and sectional properties for all surfaces (JLA, 12 2017)
'''

__version__ = 1.1

# =============================================================================
# Standard Python modules
# =============================================================================

# import os, copy, pdb, time

# =============================================================================
# External Python modules
# =============================================================================

import numpy as np

# =============================================================================
# Extension modules
# =============================================================================

import pyavl as avl

class Error(Exception):
    """
    Format the error message in a box to make it clear this
    was a expliclty raised exception.
    """
    def __init__(self, message):
        msg = '\n+'+'-'*76+'+'+'\n' + '| pyAVL Error: '
        i = 14
        for word in message.split():
            if len(word) + i + 1 > 76: # Finish line and start new one
                msg += ' '*(76-i)+'|\n| ' + word + ' '
                i = 1 + len(word)+1
            else:
                msg += word + ' '
                i += len(word)+1
        msg += ' '*(76-i) + '|\n' + '+'+'-'*76+'+'+'\n'
        print(msg)
        Exception.__init__(self)


class avlAnalysis(object):
    def __init__(self, geo_file =None, mass_file =None,  aircraft_object = None ):

        self.resetData()



    
        if not(geo_file == None):
            try:
                # check to make sure files exist 
                file = geo_file
                f = open(geo_file,'r')
                f.close()

                if not(mass_file is None):
                    file = mass_file
                    f = open(mass_file,'r')
                    f.close
            except:
                raise Error(':  There was an error opening the file %s'%(file))
                
            avl.avl()   
            avl.loadgeo(geo_file)
      

            if not(mass_file is None):
                avl.loadmass(mass_file)


        elif not(aircraft_object == None):

            pass


        else:
            raise Error('neither a geometry file or aircraft object was given')
            
        return


    def addConstraint(self,varible,val):

        self.__exe = False

        options = {'alpha':['A', 'A '],
                   'beta':['B', 'B '],
                   'roll rate':['R', 'R '],
                   'pitch rate':['P', 'P '],
                   'yaw rate':['Y', 'Y'],
                   'D1':['D1', 'PM '],
                   'D2': ['D2', 'YM '],
                   'D3': ['D3', 'RM ']}


        if not(varible in options):
            raise Error(':  constraint varible not a valid option ')
            
        avl.conset(options[varible][0],(options[varible][1] +  str(val) + ' \n'))
        return

    def addTrimCondition(self, varible, val):

        self.__exe = False

        options = {'bankAng':['B'],
                   'CL':['C'],
                   'velocity':['V'],
                   'mass':['M'],
                   'dens':['D'],
                   'G':['G'],
                   'X_cg': ['X'],
                   'Y_cg': ['Y'],
                   'Z_cg': ['Z']}

        if not(varible in options):
            raise Error(':  constraint varible not a valid option ')
            


        avl.trmset('C1','1 ',options[varible][0],(str(val) +'  \n'))
        pass
        return


    def executeRun(self):

        self.__exe = True

        avl.oper()

        self.alpha = np.append( self.alpha, float(avl.case_r.alfa))  # *(180.0/np.pi) # returend in radians)
        self.CL = np.append(self.CL, float(avl.case_r.cltot))
        self.CD = np.append(self.CD, float(avl.case_r.cdtot))   # = np append(avl.case_r.cdvtot)  for total viscous)
        self.CDV = np.append(self.CDV, float(avl.case_r.cdvtot))   # = np append(avl.case_r.cdvtot)  for total viscous)
        self.CDFF = np.append(self.CDFF, float(avl.case_r.cdff))
        self.CM = np.append(self.CM, float(avl.case_r.cmtot))
        self.span_eff = np.append(self.span_eff, float(avl.case_r.spanef))



        deflecs = (np.trim_zeros(avl.case_r.delcon)).reshape( len(np.trim_zeros(avl.case_r.delcon)), 1)
        # print deflecs,  avl.case_r.delcon
        # x.astype(int)
        

        if self.control_deflection.size==0:
            self.control_deflection = deflecs
        else:
            self.control_deflection = np.hstack((self.control_deflection, deflecs) )


        self.velocity = np.append(self.velocity, np.asarray(avl.case_r.vinf))

        # get section properties
        # NS = avl.surf_i.nj[0]
        NS = np.trim_zeros(avl.surf_i.nj)
        # print NS
        # print np.trim_zeros(avl.strp_r.clstrp[:])

        # start = 0
        sec_CLs =[]
        sec_CDs =[]
        sec_Chords =[]
        sec_Yles =[]
        end = 0
        for i in xrange(0,len(NS)):
            start = end  
            end   = start + NS[i] 
            sec_CLs.append(avl.strp_r.clstrp[start:end])
            sec_CDs.append(avl.strp_r.cdstrp[start:end])
            sec_Chords.append(avl.strp_r.chord[start:end])
            sec_Yles.append(avl.strp_r.rle[1][start:end])


        self.sec_CL.append(sec_CLs)
        self.sec_CD.append(sec_CDs)
        self.sec_Chord.append(sec_Chords)
        self.sec_Yle.append(sec_Yles)


        surf_CLs = (np.trim_zeros(avl.surf_r.clsurf)).reshape( len(np.trim_zeros(avl.surf_r.clsurf)), 1)
        surf_CDs = (np.trim_zeros(avl.surf_r.cdsurf)).reshape( len(np.trim_zeros(avl.surf_r.cdsurf)), 1)

        if self.surf_CL.size==0:
            self.surf_CL = surf_CLs
            self.surf_CD = surf_CDs
        else:
            self.surf_CL = surf_CLs = np.hstack((self.surf_CL, surf_CLs) )
            self.surf_CD = surf_CDs = np.hstack((self.surf_CD, surf_CDs) )





        # print 'alfa:', avl.case_r.alfa   

        # print 'CLTOT:', avl.case_r.cltot
        # print 'CdTOT:', avl.case_r.cdtot
        # print 'CmTOT:', avl.case_r.cmtot
        # print 'Dname', avl.case_c.dname
        # print 'Delcon', avl.case_r.delcon


        

        return 

    def calcNP(self):
        # executeRun must be run first 

        if not(self.__exe):
            raise Error(':  executeRun() must be called first')
            

        avl.calcst()
        self.NP = avl.case_r.xnp
        # print 'Xnp:', avl.case_r.xnp

        return

    

    def alphaSweep(self, start_alpha, end_alpha, increment=1):

        alphas = np.arange(start_alpha, end_alpha+increment, increment)

        for alf in alphas:
            self.addConstraint('alpha',alf)  
            self.executeRun()

        return

    def CLSweep(self, start_CL, end_CL, increment=0.1):

        CLs = np.arange(start_CL, end_CL+increment, increment)

        for cl in CLs:
            self.addTrimCondition('CL',cl)  
            self.executeRun()

        return


    def resetData(self):
        self.__exe = False

        self.alpha =np.zeros(0)
        self.CL = np.zeros(0)
        self.CD = np.zeros(0)
        self.CDV = np.zeros(0)
        self.CDFF = np.zeros(0)        
        self.CM = np.zeros(0)
        self.span_eff = np.zeros(0)

        self.elev_def = np.zeros(0)
        self.rud_def = np.zeros(0)

        self.velocity = np.zeros(0)

        self.control_deflection = np.empty(0)

        self.sec_CL = []
        self.sec_CD = []
        self.sec_Chord = []
        self.sec_Yle = []

        self.surf_CL = np.empty(0)
        self.surf_CD = np.empty(0)

    # def calcSectionalCPDist(self):

    #     for N in [1, avl.case_i.nsurf]:

    #         J1 = avl.surf_i.jfrst(N)
    #         JN = J1 + avl.surf_i.nj - 1
    #         JINC = 1

    #         CPSCL = avl.   cpfac*  avl.case_r.cref


    #         for 


    #     return



#### fortran code

#       DO N = 1, NSURF

#         J1 = JFRST(N)
#         JN = JFRST(N) + NJ(N)-1
#         JINC = 1



#            CPSCL = CPFAC*CREF


#          IP = 0
#          DO J = J1, JN, JINC
#            I1 = IJFRST(J)
#            NV = NVSTRP(J)
#            DO II = 1, NV
#              IV = I1 + II-1
#              XAVE = RV(1,IV)
#              YAVE = RV(2,IV)
#              ZAVE = RV(3,IV)
#              DELYZ = DCP(IV) * CPSCL
#              XLOAD = XAVE
#              YLOAD = YAVE + DELYZ*ENSY(J) 
#              ZLOAD = ZAVE + DELYZ*ENSZ(J)

# c             XLOAD = XAVE + DELYZ*ENC(1,IV) 
# c             YLOAD = YAVE + DELYZ*ENC(2,IV) 
# c             ZLOAD = ZAVE + DELYZ*ENC(3,IV)

#              IF(II.GT.1) THEN
#                IP = IP+1
#                PTS_LINES(1,1,IP) = XLOADOLD
#                PTS_LINES(2,1,IP) = YLOADOLD
#                PTS_LINES(3,1,IP) = ZLOADOLD
#                PTS_LINES(1,2,IP) = XLOAD
#                PTS_LINES(2,2,IP) = YLOAD
#                PTS_LINES(3,2,IP) = ZLOAD
#                ID_LINES(IP) = 0
#              ENDIF             
#              XLOADOLD = XLOAD
#              YLOADOLD = YLOAD
#              ZLOADOLD = ZLOAD
#            END DO
#          END DO
#          NLINES = IP
#          NPROJ = 2*NLINES
#          CALL VIEWPROJ(PTS_LINES,NPROJ,PTS_LPROJ)
#          CALL PLOTLINES(NLINES,PTS_LPROJ,ID_LINES)
#          CALL NEWCOLOR(ICOL)
#          CALL NEWPEN(IPN)
#         ENDIF
# C
