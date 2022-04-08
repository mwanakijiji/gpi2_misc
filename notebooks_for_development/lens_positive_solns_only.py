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

# set mangification of Lyot stop in detector
#abs_mag_max = 0.738 # mag for 10 pixel buffer on each side
abs_mag_max = 0.6912 # mag for filling 90% of shortest dimension (buffer of 5% on top, 5% on bottom)
#abs_mag_max = 0.906640625 # GPI 1.0 req

# si in terms of so and f
def si(so_pass,f_pass):

    si_result = np.divide(so_pass,np.subtract(np.divide(so_pass,f_pass),1.))

    return si_result

# set the new location of the relay lens 1
loc_lens1_abs = loc_R1_lens_current

# set a focal length so that the FT{Lyot} is just downstream of the current detector location
# (this gives us some room, so that we can move the detector back and capture that image)

detect_downstream_offset = 5. # (mm)

# needed focal length of relay 1 lens
f1_new = loc_detector_current - loc_lens1_abs + detect_downstream_offset

print("f1 new: ", f1_new)

# location of the plane for imaging FT{Lyot} (i.e., plane where there is focal point
# of relay lens 1); this is where the detector would have to be for imaging FT{Lyot}
loc_FTlyot_abs = loc_lens1_abs + f1_new

# position of image 1 (note this is {Lyot} (NOT FT{Lyot}); we need this to find the
# {Lyot} after relay lens 2 (image 2), but we will not access image 1 directly
#f1_new = 80.
so1 = loc_lens1_abs+dist_lyot_to_mirror
si1_rel = si(so_pass = so1,
        f_pass = f1_new)

si1_abs = si1_rel + loc_lens1_abs

# loop over test f2 values
f2_test = np.linspace(10., 120., num=41)

si2_abs_array = np.zeros(len(f2_test))
M_total_array = np.zeros(len(f2_test))

# plate scale at focus of relay lens 1 (and convert to asec/mm)
PS_1 = (1./f1_new) * (3600.*360./(2.*np.pi))

for num_foc in range(0,len(f2_test)):

    loc_R2_lens = loc_FTlyot_abs + f2_test[num_foc]
    so2 = loc_R2_lens - si1_abs
    si2_rel = si(so_pass = so2, f_pass = f2_test[num_foc])
    si2_abs = si2_rel + loc_R2_lens
    M1 = (si1_rel/so1)
    M2 = (si2_rel/so2)
    M_total = M1*M2

    print("PS_1", PS_1)
    print("f2", f2_test[num_foc])
    print("loc_R2_lens", loc_R2_lens)
    print("si1_rel", si1_rel)
    print("si1_abs", si1_abs)
    print("so2", so2)
    print("si2_rel", si2_rel)
    print("si2_abs", si2_abs)
    print("M1", M1)
    print("M2", M2)
    print("M_total", M_total)
    print("----")

    si2_abs_array[num_foc] = si2_abs
    M_total_array[num_foc] = M_total

fig, ax1 = plt.subplots(1, 1, figsize=(15,10))

ax1.scatter(si2_abs_array,f2_test)

ax1.annotate("current detector location", (loc_detector_current,100), color="k")
ax1.axvline(x=loc_detector_current, color="gray", linestyle="--")

ax1.annotate("FT{Lyot} plane", (loc_FTlyot_abs,50), color="k")
ax1.axvline(x=loc_FTlyot_abs, color="gray", linestyle="--")

# annotate magnifications
for i, txt in enumerate(M_total_array):
    if (np.abs(np.round(txt,3)) > abs_mag_max):
        # exceeds limit of magnification
        color_string = "r"
    else:
        color_string = "k"
    ax1.annotate("M_tot = "+str(np.round(txt,3)), (si2_abs_array[i], 7+f2_test[i]), color=color_string, rotation=90)

ax1.set_xlabel("{Lyot} absolute location (mm OPD)")
ax1.set_ylabel("Relay lens 2 focal length (mm)")

#plt.tight_layout()
plt.show()
