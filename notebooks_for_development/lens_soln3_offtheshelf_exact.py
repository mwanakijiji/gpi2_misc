#!/usr/bin/env python
# coding: utf-8

# This takes user inputs for parameters like lens positions and focal lengths, and
# calculates the final result on the detector. (This is useful after narrowing in
# on off-the-shelf lenses and checking the result)

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# off-the-shelf lens focal lengths (note there are some alternates too)
f_soln0b_R1_thor_warm = 59.8 # (mm)
f_soln3_R1_thor_warm = 124.6
f_soln3_R2_thor_warm = 74.8
f_soln0b_R1_newport_warm = 62.9 # (mm)
f_soln3_R1_newport_warm = 125.
f_soln3_R2_newport_warm = 75.6
f_soln0b_R1_edmund_warm = 60. # (mm)
f_soln3_R1_edmund_warm = 120.
f_soln3_R2_edmund_warm = 80.

 ## ## make lens more exact later, with finite thickness
 ## ## include thermal effect of focus
 ## ## " " of container

# (distances are measured from fold mirror upstream of relay 1
# lens unless otherwise specified)
soln_type = "3" # "0b" (single lens) or "3" (two positive lenses)
loc_R1_lens_old = 21.3 # old position (mm)
loc_R1_lens = loc_R1_lens_old # new position (mm)
f_R1_lens = f_soln3_R1_thor_warm # focal length of first relay lens (mm)
loc_R2_lens = 223.85
f_R2_lens = f_soln3_R2_thor_warm # focal length of second relay lens (mm)
loc_cold_shield = 65.65
loc_dewar_window = 120.25
loc_det_old = 116.05+21.3 # for comparison
#loc_opd_arm_possible = 110.
#loc_Barlow_lens = loc_det_old # choice of Barlow lens (lens 2) location

# this is a distance, but Lyot is upstream of mirror
dist_lyot_to_mirror = 106.7
#dist_lens_to_si_current = 116.05

# si in terms of so and f
def si(so_pass,f_pass):

    si_result = np.divide(so_pass,np.subtract(np.divide(so_pass,f_pass),1.))

    return si_result


# set wanted mangification of Lyot stop in detector
# (this is used in plots, but not calculations)
#abs_mag_max = 0.738 # mag for 10 pixel buffer on each side
abs_mag_max = 0.6912 # mag for filling 90% of shortest dimension (buffer of 5% on top, 5% on bottom)
#abs_mag_max = 0.906640625 # GPI 1.0 req

so_1 = dist_lyot_to_mirror + loc_R1_lens

# location of FT{Lyot} image downstream of lens 1
loc_ft_1 = loc_R1_lens + f_R1_lens

# find si1 (distance of image from first lens)
si_1 = si(so_pass = so_1, f_pass = f_R1_lens)

# find so2 (distance of first image from second lens)
loc_image_1 = si_1 + loc_R1_lens
so_2 = loc_R2_lens - loc_image_1

# find si2 (distance of final image from second lens)
si_2 = si(so_pass = so_2, f_pass = f_R2_lens)

# find abs location of detector to form image downstream of relay lens 2
loc_det = si_2 + loc_R2_lens

# find (abs val of) magnifications
mag_1 = np.divide(si_1, so_1)
mag_2 = np.divide(si_2, so_2)
mag_final = mag_1*mag_2
# relative to desired
mag_final_rel = np.divide(mag_final,abs_mag_max)

# plate scale at FT{Lyot}
PS_ftlyot = (1./f_R1_lens)*(360./(2*np.pi))

# locations of lens 1 focal points (relative to current lens)
'''
loc_lens1_fpt_rel = np.add(del_x_lens,foc_lens_1_test[num_foc])
# ... and absolute (relative to mirror); this is the second
# "object", which will be re-imaged by a second lens (if there is one)
loc_lens1_fpt_abs = np.add(loc_lens1_fpt_rel,loc_R1_lens_current)
'''


# absolute location of second image
'''
si_2_abs = np.add(loc_lens1_fpt_abs,np.add(foc_lens2_Barlow,si_2))
'''

# necessary absolute location of detector for focused image
'''
loc_det_nec = np.add(del_x_detect,loc_det_old)
'''

# consider a two-positive-lens solution (without a Barlow lens) and
# find the distance between the focal point of lens 1 and the detector;
# then any positive lens 2 that is inserted needs to have a positive focal
# length less than this; this info is printed, but not plotted
'''
dist_focpt1_det = np.subtract(loc_det,loc_lens1_fpt_abs)



# plate scale of FT{Lyot} image on final detector: 1/(M2*f1); then convert to asec/mm
PS_FTlyot = np.divide(1.,np.multiply(foc_lens_1_test[num_foc],mag_2_array)) * (3600.*360./(2.*np.pi))

# print FYI stuff
print("-----------------")
print("f = " + str(foc_lens_1_test[num_foc]))
#import ipdb; ipdb.set_trace()
df = pd.DataFrame(del_x_lens, columns=["del_x_lens"])
df["del_x_detect"] = del_x_detect
df["loc_detect_abs"] = loc_det
df["M_1_array"] = mag_1_array
df["M_2_array"] = mag_2_array
df["si_1"] = si_1_array
df["so_1"] = so_1_array
df["si_2"] = si_2
df["si_2_abs"] = si_2_abs
df["so_2"] = so_2
df["PS_FTlyot"] = PS_FTlyot # (asec/mm)
df["loc_lens1_fpt_abs"] = loc_lens1_fpt_abs
df["dist_focpt1_det"] = dist_focpt1_det
df["loc_Barlow_abs"] = loc_Barlow_abs
#df["PS_w_Barlow"] = PS_w_Barlow
df["foc_lens2_Barlow"] = foc_lens2_Barlow
print(df)
df.to_csv("figs/" + string_foc + ".txt")
'''

# print stuff
print("-------")
print("loc_R1_lens:", loc_R1_lens)
print("loc_R2_lens:", loc_R2_lens)
print("loc_det FT{Lyot}:", loc_ft_1)
print("loc_det {Lyot}:", loc_det)

plt.clf()
fig, ax1 = plt.subplots(1, 1, figsize=(15,10))

# arbitrary, but should be non-zero
ax1.set_ylim([0,100])
ax1.set_ylabel("(arbitrary)")

# location of lens 1
ax1.scatter(loc_R1_lens_old, 50, color="b", s=600, alpha=0.3)
ax1.scatter(loc_R1_lens, 50, color="b", s=600)
ax1.annotate("relay 1 lens", (loc_R1_lens, 55), color="k", rotation=90)

# detector, for imaging FT{Lyot}
ax1.annotate("new detect\nFT{Lyot}", (loc_ft_1,70), color="k")
ax1.axvline(x=loc_ft_1, color="g", linestyle="--", linewidth=6)

# location of FT{Lyot}
ax1.scatter(loc_ft_1, 50, color="orange", s=600)
ax1.annotate("FT{Lyot}", (loc_ft_1, 55), color="k", rotation=90)

# location of lens 2
ax1.scatter(loc_R2_lens, 50, color="r", s=600)
ax1.annotate("relay 2 lens", (loc_R2_lens, 55), color="k", rotation=90)

'''
# indicate locations of FT{Lyot}
# (the y here is just to point the datapoint in a visually OK place)
ax1.scatter(loc_lens1_fpt_abs, loc_det, color="r")

# indicate locations of Barlow lens (note subtraction, because x-axis is relative to current lens 1)
# (the y here is just to point the datapoint in a visually OK place)
ax1.scatter(loc_Barlow_abs, loc_det, color="k")



# indicate 1 focal length away from lens, where we expect FT{Lyot} to be
#ft_pos_line = np.add(del_x_lens,foc_lens_1_test[num_foc])
#ax1.annotate("FT location", (del_x_lens[1],ft_pos_line[1]), color="k")
#ax1.plot(del_x_lens, ft_pos_line, color="k", linestyle=":")
#ax1.fill_between(del_x_lens, -100, 0, color="gray")

# current lens 1
ax1.annotate("current lens 1", (loc_R1_lens_current,100), color="k")
ax1.axvline(x=loc_R1_lens_current, color="gray", linestyle="--")
#ax1.annotate("current detect", (-5,116.05), color="k")
#ax1.axhline(y=116.05, color="gray", linestyle="--")
'''

# fold mirror
ax1.annotate("fold mirror", (0,100), color="k")
ax1.axvline(x=0, color="gray", linestyle="--")

# cold shield
ax1.annotate("cold shield", (loc_cold_shield,100), color="k")
ax1.axvline(x=loc_cold_shield, color="gray", linestyle="--")
#ax1.annotate("cold shield", (-5,44.35), color="k")
#ax1.axhline(y=44.35, color="gray", linestyle="--")

# dewar window
ax1.annotate("dewar window", (loc_dewar_window,100), color="k")
ax1.axvline(x=loc_dewar_window, color="gray", linestyle="--")
#ax1.annotate("dewar window", (-5,98.95), color="k")
#ax1.axhline(y=98.95, color="gray", linestyle="--")

# detector, for imaging {Lyot}
ax1.annotate("current detect", (loc_det_old,100), color="k")
ax1.axvline(x=loc_det_old, color="g", linestyle="--", linewidth=6, alpha=0.5)
ax1.annotate("new detect\n{Lyot}", (loc_det,70), color="k")
ax1.axvline(x=loc_det, color="g", linestyle="--", linewidth=6)

ax1.set_xlabel("Absolute position (from mirror)")
#ax1.annotate("current detect", (-5,116.05), color="k")
#ax1.axhline(y=116.05, color="gray", linestyle="--")

ax1.set_xlim([-20,320])

plt.suptitle("lens 1 physical f = " + str(f_R1_lens) + " mm\n"\
            +"lens 2 physical f = " + str(f_R2_lens) + " mm\n"\
            +"FT{Lyot} PS= " + str(np.round(PS_ftlyot,3)) + " deg/mm\n"\
            +"{Lyot} (i.e., 2 lens) M_total = "+str(np.round(mag_final,4)) + " (" + str(np.round(mag_final_rel,4)) +" relative to optimal)")

string_full = "figs/junk.png"
#plt.tight_layout()
plt.savefig(string_full, edgecolor="white")
#plt.close()
print("Wrote " + string_full)

#plt.show()
