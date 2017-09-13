import numpy as np
import matplotlib.pyplot as plt

WTO = np.array([92500, 69600, 73000, 174200, 99600])
WE = np.array([50861, 43500, 36100, 102100, 54000])

A = np.vstack([np.log10(WE), np.ones(len(WE))]).T

B, A = np.linalg.lstsq(A, np.log10(WTO))[0]

print(A, B)


plt.plot(np.log10(WE), np.log10(WTO), 'o', label='Original data', markersize=10)
plt.plot(np.log10(WE), B*np.log10(WE) + A, 'r', label='Fitted line')
plt.legend()
plt.show()