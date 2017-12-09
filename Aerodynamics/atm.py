import os,sys
import math
sys.path.insert(1, os.path.join(sys.path[0], '..'))

def calcATM(height):
	h = height*0.0003048
	h1 = 11
	h2 = 20
	h3 = 32
	a0 = -6.5e-3
	a2 = 1e-3
	g1 = 9.80665 
	mol =28.9644
	R0 = 8.31432
	R = R0/mol*1e3
	T0 = 288.15
	p0 = 1.01325e5
	rho0 = 1.2250
	T1 = T0 + a0*h1*1e3
	p1 = p0*(T1/T0)**(-g1/a0/R)
	rho1 = rho0*(T1/T0)**(-g1/a0/R-1)
	T2 = T1
	p2 = p1*math.exp(-g1/R/T2*(h2-h1)*1e3)
	rho2 = rho1*math.exp(-g1/R/T2*(h2-h1)*1e3)

	if h <= h1:
		#print('Troposphere')
		T = T0 + a0*h*1e3;
		p = p0*(T/T0)**(-g1/a0/R);
		rho = rho0*(T/T0)**(-g1/a0/R-1);
	elif h <= h2:
		#print('Tropopause')
		T = T1
		p = p1*math.exp(-g1/R/T*(h-h1)*1e3)
		rho = rho1*math.exp(-g1/R/T*(h-h1)*1e3)
	elif h <= h3:
		#disp('Stratosphere')
		T = T2 + a2*(h-h2)*1e3
		p = p2*(T/T2)**(-g1/a2/R)
		rho = rho2*(T/T2)**(-g1/a2/R-1)
	else:
		print('Error: the altitute should be less then 104987 ft')

	T -= 272.15
	p = p*0.000145038
	rho = rho*0.00194032

	return T, p, rho

if __name__ == '__main__':
	import math
	import constants
	t, p, r = calcATM(constants.alt)
	print('Temperature (C): ' + str(t))
	print('Pressure (psi): '+ str(p))
	print('Density (slugs/ft3): ' + str(r))