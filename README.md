                                                        
     MMMMMMMMMMMMM                            MMMMMMMMMMMMMM  
     MMMMMMMMMMMMMMM                        MMMMMMMMMMMMMMMM  
     MMMMMMMMMMMMMMMMM                    MMMMMMMMMMMMMMMMMM  
     MMMMMMMMMMMMMMMMMMM                MMMMMMMMMMMMMMMMMMMM  
        MMMMMMMMMMMMMMMMMMM            MMMMMMMMMMMMMMMMMM     
        MMMMMMMMMMMMMMMMMMMMM        MMMMMMMMMMMMMMMMMMMM     
        MMMMMMMMMMMMMMMMMMMMMMM    MMMMMMMMMMMMMMMMMMMMMM      
        MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM     
        MMMMMMMMM   MMMMMMMMMMMMMMMMMMMMMMMMM   MMMMMMMMM     
        MMMMMMMMM     MMMMMMMMMMMMMMMMMMMMM     MMMMMMMMM     
        MMMMMMMMM       MMMMMMMMMMMMMMMMM       MMMMMMMMM     
        MMMMMMMMM         MMMMMMMMMMMMM         MMMMMMMMM     
        MMMMMMMMM           MMMMMMMMM           MMMMMMMMM     
        MMMMMMMMM             MMMMM             MMMMMMMMM     
     MMMMMMMMMMMMMMM            M            MMMMMMMMMMMMMMM  
     MMMMMMMMMMMMMMM                         MMMMMMMMMMMMMMM  
     MMMMMMMMMMMMMMM                         MMMMMMMMMMMMMMM  
     MMMMMMMMMMMMMMM                         MMMMMMMMMMMMMMM  


@SHAM!
- Now that I have your attention, if you want to run this code you need to do it on a unix system. Additionally the scripts used to generate the results shown in the report are ....
    - Sizing/T_S_plot.py | generates the TS plot
    - Weight/weight_refined.py | the most up to date weight build up code
    - Sizing/tradeStudies.py | Preforms the trade studies and makes the figures
    


# AEROSPACE 481 code
the code in this repository is used for the design and analysis of a regional business jet for the senior design course Aerosp 481

# Authors 
Aaron Lu  
Saif Jamal   
Becky Hill  
Josh Anibal   

# How to use the code

Everything must be called from the Aero481 file level

for example 
$ python ./Sizing/sizing.py

If you add another directory, you will need to include a __init__.py file 
to import from the folder


# In order to prevent bugs...
-  if you add anything to this file not in imperial, you are a bad person and karma will get you.
-  if you do add something in SI add a _units at the end. Again SI is not advised and frowned upon.
-  use pot_hole for variables, camelCase for functions and file, and  all folders are capitalized CamelCase
-  every thing should have a descriptive name, i.e Mach instead of M, nun_passengers instead of num_pass
-  Don't name a variable according to a letter typically used to represent to b =/= span, lambda =/= taper
-  if you are creating a lot of related variables ( weight_wing, weight_landing_gear, weight_mis) use a dictionary instead
-  try not to use the j481 properties module in the lower level functions 
-  Copying and Pasting is the source of all evil -> try to write general non repetitive code 


v 2.0 updates
- moved to class based structure for surfaces
- removed ALL metric variables ( long live imperial!!!!)


