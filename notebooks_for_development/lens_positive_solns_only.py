import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# (distances are measured from fold mirror upstream of relay 1
# lens unless otherwise specified)
loc_R1_lens_current = 21.3
loc_cold_shield = 65.65
loc_dewar_window = 120.25
loc_detector_current = 116.05+21.3
loc_opd_arm_possible = 110.
#loc_Barlow_lens = loc_detector_current # choice of Barlow lens (lens 2) location

# this is a distance, but Lyot is upstream of mirror
dist_lyot_to_mirror = 106.7
dist_lens_to_si_current = 116.05

# si in terms of so and f
def si(so_pass,f_pass):

    si_result = np.divide(so_pass,np.subtract(np.divide(so_pass,f_pass),1.))

    return si_result

# set the new location of the relay lens 1
loc_lens1_abs = loc_R1_lens_current

# set a focal length so that the FT{Lyot} is just downstream of the current detector location
# (this gives us some room, so that we can move the detector back and capture that image)

detect_downstream_offset = 5. # (mm)
f1_new = loc_detector_current - loc_lens1_abs + detect_downstream_offset

print(f1_new)

# location of the plane for imaging FT{Lyot}
loc_FTlyot_abs = loc_lens1_abs + f1_new

print(loc_FTlyot_abs)
