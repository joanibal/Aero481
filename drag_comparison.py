import numpy as np

# factors for increased aspect ratio and/or reference area
ARfact = 1.05 #aspect ratio factor
reffact = 1.05 #reference area factor

# constants given initial geometry
CD0 = 0.0250260642922
CL = 0.4527
AR = 9

CDi_init = ((CL**2)*(1.05+0.007*np.pi*AR))/(np.pi*AR) # initial C_D induced
CDi_new = ((CL**2)*(1.05+0.007*np.pi*AR*ARfact))/(np.pi*AR*ARfact) #C_D induced with the increased aspect ratio

Dratio = (CDi_new*reffact)/CDi_init #new drag/initial drag after simplification
Dpercent = (Dratio-1)*100 # %change in drag

print(str(Dpercent) + '%')
