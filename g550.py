import numpy as np
from AircraftClass.classes import surface, Object
from Sizing.tailSizing import genTail
# Properties file for j481

# ===============================
#    READ THIS
# ===============================
# In order to prevent bugs...
# -  if you add anything to this file not in imperial, you are a bad person and karma will get you.
# -  if you do add something in SI add a _units at the end. Again SI is not advised and frowned upon.
# -  use pot_hole for variables, camelCase for functions and file, and  all folders are captilized CamelCase
# -  every thing should have a descriptive name, i.e Mach instead of M, nun_passengers instead of num_pass
# -  Don't name a variable according to a letter typically used to represent to b =/= span, lambda =/= taper
# -  if you are creating a lot of related variables ( weight_wing, weight_landing_gear, weight_mis) use a dictionary instead
# -  try not to use the j481 properties module in the lower level functions 

# used for selection in the code
name = 'g550'

#  ------------ Misson Parameters -----------------
runway_length = 7000                        # ft
altitude = 40000                            # ft
altitude_ceiling = 56000                    # ft
mach = 0.80
range_nMi = 6750                            # nMi
cruise_steps = 1                            # number of altitude levels for cruise

num_pilots = 2  #number of pilots
num_passengers = 8  #number of passengers
num_attendants = 2  #number of attendants

jetA_density = 6.71 #lb/gal

                   
#  ---------------- state variables -------------------
#cruise 
temp_cruise = -69.7                       # Temperature F
temp_cruise_K = (temp_cruise - 32)*5.0/9 + 273.15

density_cruise = (22650 * np.exp(1.73 - .000157*(altitude*0.3048)))/(287*temp_cruise_K)*0.00194032  # slugs/ft^3
speed_fps = mach*np.sqrt(1.4*287*temp_cruise_K)*3.28084  # velocity from m/s to ft/s
speed_kts = speed_fps*0.592484
q_cruise = 0.5*density_cruise*speed_fps**2          # Dynamic Pressure (imperial!!!!)
mu_cruise = 2.969e-7    #lbf*s/ft^2


# # Sea Level 
density_SL = 0.0023769                      # slugs/ft^3

# # Ceiling


# # assumes that the ceiling is
density_ceiling =  (22650 * np.exp(1.73 - .000157 * (altitude_ceiling * 0.3048))) / (287 * temp_cruise_K) * 0.00194032  # slugs/ft^3
# a_Ceiling = 573.57                          # knots



#  -------------------- propulsion -------------------------
SFC = 0.6414                                 # 1/hr
SFC_sealevel = 0.39                        # 1/hr
numEngines = 2
engine_thrust = 15385  # lbs - sea level

# design point
thrust_req = engine_thrust*numEngines #lbs

propulsion = Object()
propulsion.MAC_c = 16.24 # ft  # this isnt really a MAC, but it will make the loop in drag buildup easier
propulsion.length = propulsion.MAC_c
propulsion.diameter = 5.91 # ft
propulsion.interfernce_factor = 1.0
propulsion.wetted_area = 260.53 #ft^2,
propulsion.sweep = 0
propulsion.frac_laminar = 0.1
propulsion.finish = 'smoothPaint'

#  -------------------- Weight -------------------------
wight_per_person = 180          # lbf
weight_crew = (num_pilots + num_attendants)*wight_per_person
weight_payload = (num_pilots + num_attendants + num_passengers)*wight_per_person



#  -------------------- Geometry Definition -------------------------
# These get used every where and we don't want different definitions like before....


fuselage = Object()

fuselage.MAC_c = 85.83 # ft
fuselage.length = fuselage.MAC_c  # ft
fuselage.diameter = 7.83 # ft
fuselage.interfernce_factor = 1.0
fuselage.wetted_area = 1731.70 #ft^2,
fuselage.sweep = 0
fuselage.frac_laminar = 0.1
fuselage.finish = 'smoothPaint'
fuselage.empennage_upsweep = 6.08853 * 0.0174533        # deg ???                                               # rad
fuselage.cabinpressure = 10.17  # psi



# # static_margin = 0.15
Sref = 1140.  # < - include the decimal so python knows it's a float 

                    # horizonal, vertical
dist_to_surface = np.array([39.36, 30.26])  # [distace to H tail, distance to V tail] in ft



wing = surface(Sref, 7.4, 0.26, 27., offset=np.array([33.9, 4.4, 0]),\
                 airfoil_file='Aerodynamics/Airfoils/sc20612-il.dat', finish='polishedSM', thickness_chord=0.1, frac_laminar=0.35 )

wing.flap_position = np.array([0.1, 0.5])
wing.flap_deflection = {'landing': 30., 'takeoff': 15.}
wing.slat_position = np.array([0.1, 0.5])
wing.mounted_area = 149.62 * 2  # ft

wing.Nspan = 10 
wing.update()

tail_vert = surface(140.16, 0.98, 0.65, 37., offset=np.array([65, 0, 10]), \
                airfoil_file='Aerodynamics/Airfoils/sc0012.dat', finish='polishedSM',\
                thickness_chord=0.095, frac_laminar=0.35, vertical=True )

tail_horz = surface(244.87, 5.05, 0.41, 30., offset=np.array([75, 0, 23]), twist=np.array([10,-4]), \
                airfoil_file='Aerodynamics/Airfoils/sc0012.dat', finish='polishedSM', thickness_chord=0.09, frac_laminar=0.35 )


# tail_vert, tail_horz = genTail(wing, dist_to_surface )


# #  -------------------- Lift and Drag -------------------------
# LD_ratio = 15       # used in weight_estimation and replaced later

CD0 = {'cruise':0.01519}
# # these values should come from AVL
CL= {
    'max': {
    'takeoff': 1.56,
    'cruise':  1.0,
    'landing': 2.1,
    },
    'cruise': 0.57,
    }
CL['max']['balked landing'] = CL['max']['landing'] * 0.85

e = {
    'takeoff':0.8,
     'cruise':0.925,
     'landing':0.8
     }



k = {}
for key in e.keys():
  k[key] = 1. / (np.pi * wing.aspect_ratio * e[key])
# #  -------------------- Performance -------------------------


# v_landingstall = 143.977436581 #ft/s


# #  -------------------- Loading -------------------------
 

load_factor = 4.5
# # sweep_half = math.atan((0.5*b*math.tan(sweep)-0.25*c_root + 0.25*w_lambda*c_root)/(0.5*b))
Keco = 0.686

# # ------------------ Composite Factors ----------------------
# # listed in weight_refined.py
# # canard.comp = 1
# # wing.comp = 0.8
# # tail_horz.comp = 0.75
# # tail_vert.comp = 0.75
# # fuselage.comp = 0.75
# # propulsion.comp = 1.0

# # gear_comp = 0.92


# cg_locations = {'wing':60.0,                
#                 'HT':105.0117,
#                 'canard':13.5491,
#                 'VT':93.7585,
#                 'fuselage':40.48,
#                 'main_gear':54.4441,
#                 'nose_gear':13.4351,
#                 'propulsion':70.4627}

# cg_additional = {'fuel_control':cg_locations['wing'],
#                 'start_systems':cg_locations['propulsion'],
#                 'surface_control':cg_locations['wing'],
#                 'instruments':cg_locations['fuselage'],
#                 'furnishings':cg_locations['fuselage'],
#                 'avionics':cg_locations['fuselage'],
#                 'electronics':cg_locations['fuselage']}


# #landing gear
# wheels_nose = 2
# wheels_main = 4
# nose_x = 180.0*0.0254           #m (from datum at nose)
# main_x = 20.7249521             #m (from datum at nose)

# # A/C mass properties (datum at nose)
# np_location = 54.46194  # ft
# # ft (chosen because forward cg can be modified based on fuel placement)
# cg_fwd = 49.2126
# cg_aft = 52.723097  # empty CG location
# cg_h = 8.2021  # ft

# # quit()




