from constants import *
import numpy as np
import matplotlib.pyplot as plt


Cd_0 = 0.01597
N = 100
W_S = np.linspace(0, 350, N)
CL_max = 2.5

# crusie 
T_W_cruise = 1.0/(0.2826**0.6)*(228.8*0.01597)/W_S + (W_S)*1/(228.8*np.pi)


# Ceiling 
T_W_ceiling = 1/(Density_Ceilng/Density_SL )**0.6 * ( 0.001 + 2*np.sqrt(Cd_0/(np.pi*9.8*0.85)))  


#takeoff 
T_W_Takeoff = W_S/(1*CL_max* 4948/37.5)

plt.plot(W_S, np.ones(N)*T_W_ceiling, 'r--')
plt.plot(W_S, T_W_cruise, 'r--')
plt.plot(W_S, T_W_Takeoff, 'g--')
plt.show()
