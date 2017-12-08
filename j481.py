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
name = 'j481'

#  ------------ Misson Parameters -----------------
runway_length = 4948                        # ft
altitude = 50000                            # ft
altitude_ceiling = 56000                            # ft
mach = 0.85
range_nMi = 5200                            # nMi
cruise_steps = 1                            # number of altitude levels for cruise

num_pilots = 2  #number of pilots
num_passengers = 8  #number of passengers
num_attendants = 1  #number of attendants

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


# Sea Level 
density_SL = 0.0023769                      # slugs/ft^3

# Ceiling

# density_ceiling =  2.26e-4                  # slugs/ft^3

# assumes that the ceiling is
density_ceiling =  (22650 * np.exp(1.73 - .000157 * (altitude_ceiling * 0.3048))) / (287 * temp_cruise_K) * 0.00194032  # slugs/ft^3
a_Ceiling = 573.57                          # knots



#  -------------------- propulsion -------------------------
SFC = 0.725                                 # 1/hr
SFC_sealevel = 0.346                        # 1/hr
numEngines = 2
# engine_thrust = 7760                        #lbs - sea level
engine_thrust = 7760  # lbs - sea level

# design point
thrust_req = engine_thrust*numEngines #lbs


#  -------------------- Weight -------------------------
wight_per_person = 180          # lbf
weight_crew = (num_pilots + num_attendants)*wight_per_person
weight_payload = (num_pilots + num_attendants + num_passengers)*wight_per_person



#  -------------------- Geometry Definition -------------------------
# These get used every where and we don't want different definitions like before....


# static_margin = 0.15
Sref = 950.  # < - include the decimal so python knows it's a double 
canard_area_ratio = 0.2 #1./9
wing_area_ratio = 1 - canard_area_ratio

# from airfoil exerimental paper
airfoil_t_c = 0.093

                    # horizonal, vertical
dist_to_surface = np.array([28.47769, 20.83])  # [distace to H tail, distance to V tail] in ft

wing = surface( wing_area_ratio*Sref, 9, 0.26, 36., offset=np.array([40, 4.4, 0]), twist=np.array([10,-4]), \
                airfoil_file='Aerodynamics/Airfoils/sc20612-il.dat', finish='polishedSM',\
                thickness_chord=airfoil_t_c, frac_laminar=0.35 )

wing.flap_position = np.array([0.1, 0.5])
wing.flap_deflection = {'landing': 30., 'takeoff': 15.}
wing.slat_position = np.array([0.1, 0.5])
wing.mounted_area = 132.8011 * 2  # ft

wing.Nspan = 10 
wing.update()


canard = surface( canard_area_ratio*Sref, 6, 0.25, 38., offset=np.array([9, 4.4, 0]), twist=np.array([2,2]), \
                airfoil_file='Aerodynamics/Airfoils/sc20612-il.dat', finish='polishedSM',\
                thickness_chord=airfoil_t_c, frac_laminar=0.35 )


canard.flap_position = np.array([0.0, 1.0])
canard.flap_deflection = {'landing': 20., 'takeoff': 10.}


                        

tail_vert, tail_horz = genTail(wing, dist_to_surface ,  canard=canard)



# I'm freestyling a bit here, but info about the nacelle and fuse 
# is stored the same way as was done for the other surfaces 



propulsion = Object()
propulsion.MAC_c = 12.5 # ft  # this isnt really a MAC, but it will make the loop in drag buildup easier
propulsion.length = propulsion.MAC_c
propulsion.diameter = 4.83 # ft
propulsion.interfernce_factor = 1.0
propulsion.wetted_area = 215.58 #ft^2,
propulsion.sweep = 0
propulsion.frac_laminar = 0.1
propulsion.finish = 'smoothPaint'
propulsion.comp = 1

fuselage = Object()

fuselage.MAC_c = 101.17 # ft
fuselage.length = fuselage.MAC_c
fuselage.diameter = 8.8 # ft
fuselage.interfernce_factor = 1.0
fuselage.wetted_area = 2323.66 #ft^2,
fuselage.sweep = 0
fuselage.frac_laminar = 0.1
fuselage.finish = 'smoothPaint'
fuselage.empennage_upsweep = 6.08853 * 0.0174533        # deg ???                                               # rad
fuselage.cabinpressure = 11.8  # psi


# interior = Object()


#  -------------------- Lift and Drag -------------------------
LD_ratio = 15       # used in weight_estimation and replaced later


# these values should come from AVL
CL= {
    'max': {
    'takeoff': 2.0,
    'cruise':  1.3,
    'landing': 2.7,
    },
    'cruise': 0.57,
    }
CL['max']['balked landing'] = CL['max']['landing'] * 0.85

e = {'takeoff':0.775,
     'cruise':0.835,
     'landing':0.725
     }



k = {}
for key in e.keys():
  k[key] = 1. / (np.pi * wing.aspect_ratio * e[key])
#  -------------------- Performance -------------------------


v_landingstall = 143.977436581 #ft/s


#  -------------------- Loading -------------------------
 

load_factor = 4.5
# sweep_half = math.atan((0.5*b*math.tan(sweep)-0.25*c_root + 0.25*w_lambda*c_root)/(0.5*b))
Keco = 0.686



cg_locations = {'wing':60.0,                
                'HT':105.0117,
                'canard':13.5491,
                'VT':93.7585,
                'fuselage':40.48,
                'main_gear':54.4441,
                'nose_gear':13.4351,
                'propulsion':70.4627}

cg_additional = {'fuel_control':cg_locations['wing'],
                'start_systems':cg_locations['propulsion'],
                'surface_control':cg_locations['wing'],
                'instruments':cg_locations['fuselage'],
                'furnishings':cg_locations['fuselage'],
                'avionics':cg_locations['fuselage'],
                'electronics':cg_locations['fuselage']}


#landing gear
wheels_nose = 2
wheels_main = 4
nose_x = 180.0*0.0254           #m (from datum at nose)
main_x = 20.7249521             #m (from datum at nose)

# A/C mass properties (datum at nose)
np_location = 54.46194  # ft
# ft (chosen because forward cg can be modified based on fuel placement)
cg_fwd = 49.2126
cg_aft = 52.723097  # empty CG location
cg_h = 8.2021  # ft

# quit()




