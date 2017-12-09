#Cost Analysis
import os,sys,inspect

sys.path.insert(1, os.path.join(sys.path[0], '..'))
import numpy as np
from Weight.weight_estimation import calcWeights

#Define constants
b_year = 1993					#Base year
t_year = 2017					#Then year
# MTOW, _, W_f, _ = calcWeights((5000+200),15, 0.657, M=0.85, weight_payload)				#Maximum Takeoff Weight
MTOW = 55774.0
W_f = 17298.0
t_b = 10.5						#Estimated flight time (assuming 1 stage mission)
nCrew = 2						#Number of crew members
n_attd = 1						#Number of attendants
P_f = 6							#Price/gal of Jet A fuel
rho_f = 6.71					#lb/gal of Jet A fuel at 15 deg C
# W_f	= 10000						#Fuel weight
W_oil = 0.0125*W_f*(t_b/100) 	#Assuming 100 block per oil change
P_oil = 53.89					#Cost per gallon of oil
rho_oil = 8.37461337			#Oil density
b_year_nav = 1989				#Base year navigation
R = 5200						#Range estimation of 5200 nmi
R_L = 20						#Maintenance labor rate (USD/hr)
T0 = 15000						#Estimated thrust 15,000 lbs/engine
n_eng = 2						#Specify number of engines
n_pax = 8						#Number of passengers

#Calculate CEF
bCEF = 5.17053 + 0.104981*(b_year - 2006)
tCEF = 5.17053 + 0.104981*(t_year - 2006)
CEF = tCEF/bCEF
print('CEF: ' + str(CEF))

#Solve for crew costs
C_crew = (482 + 0.590*(MTOW/1000))*CEF*t_b
spCrew = C_crew/nCrew;								#Specific crew cost
print('Specific Crew Cost: $' + str(spCrew))

#Solve for attendants costs
C_attd = 78*n_attd*CEF*t_b
print('Attendants Cost: $' + str(C_attd))

#Solve for fuel costs
C_f = 1.02*W_f*P_f/rho_f
print('Fuel Costs: $' + str(C_f))

#Solve for oil cost
C_oil = 1.02*W_oil*(P_oil/rho_oil)
print('Oil Cost: $' + str(C_oil))

#Solve for airport costs
C_airport = 4.25*(MTOW/1000)*CEF
print('Airport Costs: $' + str(C_airport))

#Solve for navigation fees
#Solve for new CEF for given base year
bCEF_nav = 5.17053 + 0.104981*(b_year_nav - 2006)
CEF_nav = tCEF/bCEF_nav

#Calculate nav fees
C_nav = 0.5*CEF_nav*(1.852*R/t_b)*np.sqrt(0.00045359237*MTOW/50)
print('Navigational Fees: $' + str(C_nav))

#Maintenance reference
#https://www.avjobs.com/salaries-wages-pay/hourly-aviation-pay.asp

#Solve for airframe maintenance
C_aircraft = 10**(3.3191+0.8043*np.log10(MTOW))*CEF
C_engines = 10**(2.3044+0.8858*np.log10(MTOW))*CEF
C_airframe = C_aircraft - C_engines
W_AMPR = MTOW										#Assume W_AMPR is equal to MTOW
C_ML = 1.03*(3+(0.067*W_AMPR/1000))*R_L				#Labor Cost
C_MM = 1.03*(30*CEF)+(0.79*10**(-5))*R_L
C_airframeMaintenance = (C_ML+C_MM)*t_b				#Total A/C airframe cost
print('Total airframe maintenance cost: $' + str(C_airframeMaintenance))

#Solve for engine maintenance
C_ML = (0.645 + (0.05*T0/10**4)) * (0.566 + 0.434/t_b) * R_L
C_MM = (25+(18*T0/10**4)) * (0.62+0.38/t_b) * CEF
C_engMaint = n_eng*(C_ML + C_MM)*t_b
print('Total engine maintenance cost: $' + str(C_engMaint))

#Total COC
COC = (2*spCrew) + C_attd + C_f + C_oil + C_airport+ C_nav + C_airframeMaintenance + C_engMaint
print('Total COC: $' + str(COC))
