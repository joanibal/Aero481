from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from matplotlib.font_manager import FontProperties

# create new figure, axes instances.
fig=plt.figure()
ax=fig.add_axes([0.1,0.1,0.8,0.8])
# np.linspace(0,)




# range in m from  nm 
radiusOper = 5200*1852.0 #m

radiusEarth = 6371*1000.0 # m

gcAngle = radiusOper/radiusEarth

# alpha = 0;

lat_1 = 33.9225
long_1 = -118.3345 


def tand(x):
    return np.tan(x * np.pi / 180)

def sind(x):
    return np.sin(x * np.pi / 180)

def cosd(x):
    return np.cos(x * np.pi / 180)

def resCoords (A):
    """
    Get sum of the forces, used for fsolve
    """
    dellong = A[0]
    # lat_2 = A[1]

    F = np.empty(1)

    # F[0] = tand(alpha) - sind(dellong)/(cosd(lat_1)*tand(lat_2) - sind(lat_1)*cosd(dellong))
    F[0] = np.tan(gcAngle) - np.sqrt( (cosd(lat_1)* sind(lat_2) - sind(lat_1)*cosd(lat_2)*cosd(dellong))**2 + ( cosd(lat_2)*sind(dellong) )**2  )\
                            /(sind(lat_1)*sind(lat_2) + cosd(lat_1)*cosd(lat_2)*cosd(dellong))
    
    # if np.abs(dellong) > 180:
    #     F[0] += np.abs(dellong) - 180
    # print F

    return F

tol = 0.01;

latRange = []
longRange = []
for lat_2 in np.linspace(-53,60.03103, 200):

    # print('=========', alpha)

    # Fsolve to balance lift and weight
    Z = fsolve(resCoords,np.array([0]), xtol=1e-15, maxfev=200)
    # Z = fsolve(resCoords,np.array([ 0, 0]))
    # print Z
    # print lat_2,  Z[0]
    # print('=========', alpha)
    if (Z[0] > 180):
        Z[0] -= 360 
    elif (Z[0] < -180):
        Z[0] += 360 


    latRange.append(lat_2)
    longRange.append( long_1 + Z[0])
    # if (longRange[-1] > 180):
    #     Z[0] += 360  
    latRange.append(lat_2)
    longRange.append(long_1 - Z[0] )



    # if (abs(abs(Z[0]) - 180) < tol):
    #     break

    # if (longRange[-1] > -180):
    #     Z[0] += 360 

    # if (np.abs(Z[0]) >= 178):
    #     print('broke')

    #     break



longRange, latRange = zip(*sorted(zip(longRange, latRange)))

# longRange = np.array(longRange)
# latRange = np.array(latRange)

# longRange[longRange < -180] += 360 
# print(longRange)
# print(latRange)
# quit()
# setup mercator map projection.
m = Basemap(llcrnrlon=-299.,llcrnrlat=-60.,urcrnrlon=60.,urcrnrlat=75.,\
            rsphere=(6378137.00,6356752.3142),\
            resolution='l',projection='merc',\
            lat_0=40.,lon_0=-20.,lat_ts=20.)
# nylat, nylon are lat/lon of New York
lonlat = 51.5048; lonlon = 0.0495
# lonlat, lonlon are lat/lon of London.
# lonlat = 51.53; lonlon = 0.08
# draw great circle route between NY and London
# m.drawgreatcircle(nylon,nylat,lonlon,lonlat,linewidth=2,color='b')
m.drawcoastlines()
m.fillcontinents()
# draw parallels
# m.drawparallels(np.arange(10,90,20),labels=[1,1,0,1])
# # draw meridians
# m.drawmeridians(np.arange(-180,180,30),labels=[1,1,0,1])
# ax.set_title('Great Circle from New York to London')
x,y = m(longRange, latRange)
m.drawgreatcircle(long_1,lat_1,lonlon,lonlat,del_s=1000, linewidth=2,color='r')

plt.plot(x, y)
plt.fill_between(x, y, [1e9]*len(y), alpha=0.5,)

HHR_x,HHR_y = m(long_1, lat_1)
LCY_x,LCY_y = m(lonlon, lonlat)

CPH_x, CPH_y = m( 12.6508, 55.6180) # Copenhagen
BSB_x, BSB_y = m( -47.9172, -15.8697 ) # Brasilia
HND_x, HND_y = m( (139.7798-360), 35.5494) # Tokyo

plt.plot(HHR_x, HHR_y, 'k*', markersize=8, color='#8B0000')
plt.plot(LCY_x, LCY_y, 'k*', markersize=8, color='#8B0000')

plt.plot(BSB_x, BSB_y, 'b*', markersize=8, color='midnightblue')
plt.plot(CPH_x, CPH_y, 'b*', markersize=8, color='midnightblue')
plt.plot(HND_x, HND_y, 'b*', markersize=8, color='midnightblue')


font = FontProperties()
font.set_weight('bold')
font.set_size('x-large')
plt.text(HHR_x - 1.5e6, HHR_y  - 0.2e6 , 'LA', fontproperties=font, color='#8B0000')
plt.text(LCY_x - 2.5e6, LCY_y  - 0.6e6 , 'London', fontproperties=font, color='#8B0000')

# plt.text(BSB_x - 1.95e6, BSB_y  - 0.2e6 , 'Brasilia', fontproperties=font, color='midnightblue')
plt.text(BSB_x - 1.95e6, BSB_y  + 0.25e6 , 'Brasilia', fontproperties=font, color='midnightblue')
plt.text(CPH_x + 0.3e6, CPH_y  - 0.55e6 , 'Copenhagen', fontproperties=font, color='midnightblue')
plt.text(HND_x + 0.3e6, HND_y - 0.2e6, 'Tokyo', fontproperties=font, color='midnightblue')



# at 40000 th plane will take this long to get to LCY
a = np.sqrt(1.4*287*216.65)
v = 0.85*a
time = radiusOper/v

time = time/60/60;
print time

plt.show()
