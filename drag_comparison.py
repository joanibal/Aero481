import numpy as np

# factors for increased aspect ratio and/or reference area
ARfact = 1.05 #aspect ratio factor
reffact = 1.05 #reference area factor

# constants given initial geometry
AR = 9

CDi_init = (1.05+0.007*np.pi*AR)/(np.pi*AR) # initial C_D induced, simplified to exclude values that would cancel out with new drag
CDi_new = (1.05+0.007*np.pi*AR*ARfact)/(np.pi*AR*ARfact) #C_D induced with the increased aspect ratio, simplified to exclude values that would cancel out with initial drag

Dratio = (CDi_new*reffact)/CDi_init #new drag/initial drag after simplification
Dpercent = (Dratio-1)*100 # %change in drag

print(str(Dpercent) + '%')
