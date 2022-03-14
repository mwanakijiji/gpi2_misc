#!/usr/bin/env python
# coding: utf-8

# This is for some trial-and-error to see what focal lengths we might need

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# si in terms of so and f
'''
def si(so_pass,f_pass):

    si_result = np.divide(so_pass,np.subtract(np.divide(so_pass,f_pass),1.))

    return si_result
'''

# set constants (mm)
r1 = 5.
r2 = 5.25
r3 = 7.
r4 = 11.
r5 = 8.
r6 = 4.72
# distances relative to large fold mirror
# (distances are measured from fold mirror upstream of relay 1
# lens unless otherwise specified)
loc_R1_lens_current = 21.3
loc_cold_shield = 65.65
loc_dewar_window = 120.25
loc_detector_current = 116.05+21.3
loc_opd_arm_possible = 110.

# desired magnification of pupil lens on detector
#abs_mag_max = 0.738 # mag for 10 pixel buffer on each side
#abs_mag_max = 0.6912 # mag for filling 90% of shortest dimension (buffer of 5% on top, 5% on bottom)
abs_mag_max = 0.906640625 # GPI 1.0 req

# Relay 1 lens
# choice of focal lengths
foc_1_test = np.linspace(50., 300., num=30)
# choice of focal lengths will translate into new position relative to mirror
loc_R1_lens_new = np.subtract(foc_1_test,106.7)

# Relay 2 lens
# choice of focal lengths consistent with magnification
# (this magnification valid for small angles)
foc_2_test = np.divide(foc_1_test,abs_mag_max)


# mirror-FT{Lyot} distance array
loc_ft_lyot = np.add(loc_R1_lens_new,foc_1_test)

# find characteristic size of FT{Lyot} image
size_ft_lyot = np.divide(1.,foc_1_test)*np.arctan(r1/foc_1_test)

# mirror-lens R2 distance
loc_R2_lens_new = np.add(loc_ft_lyot,foc_2_test)

# location of R2 relative to current detector position
R2_rel_det_now = np.subtract(loc_R2_lens_new,loc_detector_current)

#import ipdb; ipdb.set_trace()

# print FYI stuff
print("-----------------")
'''
print("f = " + str(foc_test[num_foc]))
df = pd.DataFrame(del_x_lens, columns=["del_x_lens"])
df["del_x_detect"] = del_x_detect
df["mag_array"] = mag_array
df["si"] = si_array
df["so"] = so_test
print(df)
'''

# plot parameter space of lens/detector displacements
fig, ax1 = plt.subplots(1, 1, figsize=(15,8))
#import ipdb; ipdb.set_trace()
for i, txt1 in enumerate(list(foc_1_test)):
    ax1.annotate("(f_R1 = "+str(np.round(txt1,1)) + ", ", (loc_R1_lens_new[i]+5, loc_R2_lens_new[i]), color="k")
for i, txt2 in enumerate(list(foc_2_test)):
    ax1.annotate("f_R2 = "+str(np.round(txt2,1)) + ")", (loc_R1_lens_new[i]+35, loc_R2_lens_new[i]), color="k")
ax1.scatter(loc_R1_lens_new,loc_R2_lens_new, color="blue")
ax1.scatter(loc_R1_lens_new,loc_ft_lyot, color="red")
ax1.set_xlabel("R1 lens pos (mm, rel to large fold mirror)")
ax1.set_ylabel("blue: R2 lens pos\nred: FT[Lyot] plane\n(mm, rel to large fold mirror)")

# indicate 1 focal length away from lens, where we expect FT{Lyot} to be (approximation)
'''
ft_pos_line = np.add(del_x_lens,foc_test[num_foc]) # FT{Lyot}
lyot_post_ft_pos_line = np.add(del_x_lens,2.*foc_test[num_foc]) # {Lyot}
ax1.annotate("FT{Lyot}", (del_x_lens[1],ft_pos_line[1]), color="k")
ax1.plot(del_x_lens, ft_pos_line, color="k", linestyle=":")
ax1.annotate("{Lyot}", (del_x_lens[1],lyot_post_ft_pos_line[1]), color="k")
ax1.plot(del_x_lens, lyot_post_ft_pos_line, color="k", linestyle=":")
#ax1.fill_between(del_x_lens, -100, 0, color="gray")
ax1.set_ylim([0,300])
#ax1.set_title("Lens inside dewar")
'''

# cold shield
ax1.annotate("cold\nshield", (loc_cold_shield,50), color="k")
ax1.axvline(x=loc_cold_shield, color="gray", linestyle="--")
#ax1.annotate("cold shield", (-5,44.35), color="k")
#ax1.axhline(y=44.35, color="gray", linestyle="--")

# dewar window
ax1.annotate("dewar\nwindow", (loc_dewar_window,50), color="k")
ax1.axvline(x=loc_dewar_window, color="gray", linestyle="--")
#ax1.annotate("dewar window", (-5,98.95), color="k")
#ax1.axhline(y=98.95, color="gray", linestyle="--")

# current detector
ax1.annotate("current\ndetect", (loc_detector_current,50), color="k")
ax1.axvline(x=loc_detector_current, color="gray", linestyle="--")
ax1.annotate("current\ndetect", (-50,loc_detector_current), color="k")
ax1.axhline(y=loc_detector_current, color="gray", linestyle="--")

# current R1 lens
ax1.annotate("current\nR1 lens", (loc_R1_lens_current,50), color="k")
ax1.axvline(x=loc_R1_lens_current, color="gray", linestyle="--")

#loc_detector_current
# possible location for OPD arm
ax1.annotate("possible\nOPD arm", (loc_opd_arm_possible,70), color="k")
ax1.axvline(x=loc_opd_arm_possible, color="gray", linestyle="--")

plt.suptitle("Magnification M = "+str(np.round(abs_mag_max,3)))
'''
string_foc = str(foc_test[num_foc]).replace(".","_")
string_full = "figs/" + string_foc + ".png"
plt.savefig(string_full, edgecolor="white")
print("Wrote " + string_full)
'''
plt.show()
