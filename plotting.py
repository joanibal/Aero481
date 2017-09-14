import numpy as np
import matplotlib.pyplot as plt

WTO = np.array([92500, 69600, 73000, 174200, 99600])
WE = np.array([50861, 43500, 36100, 102100, 54000])

weight_fraction =

plt.plot(np.log10(WTO), np.log10(np.divide(WE, WTO)), 'o')
plt.show()
