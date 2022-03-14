#!/usr/bin/env python
# coding: utf-8

# This is for some trial-and-error to see what focal lengths we might need

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

# f in terms of so and si
def f_needed(so_pass,si_pass):

    f_result = np.divide(so_pass*si_pass, so_pass + si_pass)

    return f_result

# try moving lens; note these are relative movements
# (+: downstream; -: upstream)
del_x_lens = np.arange(-10., 130., step=3.0) # displacement of lens (might be bumping into walls and elements)

# distance between object and lens
so_1_array = np.add(dist_lyot_to_mirror+loc_R1_lens_current, del_x_lens)

# choices of lens 1 focal lengths
foc_lens_1_test = np.linspace(50., 120., num=71)

# set mangification of Lyot stop in detector
#abs_mag_max = 0.738 # mag for 10 pixel buffer on each side
abs_mag_max = 0.6912 # mag for filling 90% of shortest dimension (buffer of 5% on top, 5% on bottom)
#abs_mag_max = 0.906640625 # GPI 1.0 req

# loop over possible focal lengths of lens 1
for num_foc in range(0,len(foc_lens_1_test)):

    # find the si array (distance of image from lens)
    si_1_array = si(so_pass = so_1_array, f_pass = foc_lens_1_test[num_foc])

    # find needed detector displacement from current
    del_x_detect = np.subtract(
                                np.add(so_1_array,si_1_array),
                                loc_R1_lens_current+dist_lyot_to_mirror+dist_lens_to_si_current
                                )

    # find (abs val of) magnifications
    mag_array = np.divide(si_1_array,so_1_array)

    # locations of lens 1 focal points (relative to current lens)
    loc_lens1_fpt_rel = np.add(del_x_lens,foc_lens_1_test[num_foc])
    # ... and absolute (relative to mirror); this is the second
    # "object", which will be re-imaged by a second lens (if there is one)
    loc_lens1_fpt_abs = np.add(loc_lens1_fpt_rel,loc_R1_lens_current)

    # if Barlow lens is upstream of lens 1 focal point by upstr_Barlow_dist,
    # calculate focal length to project FT{Lyot} onto detector
    upstr_Barlow_dist = 5. # (mm); note sign convention here: + means Barlow is upstream of focal point
    # absolute location of Barlow lens
    loc_Barlow_abs = np.subtract(loc_lens1_fpt_abs,upstr_Barlow_dist)
    # the focal length required to image the FT on the same detector
    # if the Barlow lens is in
    foc_lens2_Barlow = f_needed(so_pass=-upstr_Barlow_dist,
                        si_pass=np.subtract(del_x_detect+loc_detector_current,loc_Barlow_abs))

    # remove all negative values, because they are unphysical (Barlow
    # downstream of the focal point)
    #idx_unphysical = Barlow_rel_lens1foc<0
    #foc_lens2_Barlow[idx_unphysical] = np.nan

    # print FYI stuff
    print("-----------------")
    print("f = " + str(foc_lens_1_test[num_foc]))
    #import ipdb; ipdb.set_trace()
    df = pd.DataFrame(del_x_lens, columns=["del_x_lens"])
    df["del_x_detect"] = del_x_detect
    df["mag_array"] = mag_array
    df["si"] = si_1_array
    df["so"] = so_1_array
    print(df)

    plt.clf()
    fig, ax1 = plt.subplots(1, 1, figsize=(15,5))

    # annotate magnifications
    for i, txt in enumerate(mag_array):
        if (np.round(txt,3) > abs_mag_max):
            # exceeds limit of magnification
            color_string = "r"
        else:
            color_string = "k"
        ax1.annotate("M_1 = "+str(np.round(txt,3)) + ", ", (del_x_lens[i], 7+del_x_detect[i]), color=color_string, rotation=90)
    # annotate Barlow focal lengths
    for i, txt2 in enumerate(foc_lens2_Barlow):
        ax1.annotate("f_B = "+str(np.round(txt2,3)), (del_x_lens[i], 67+del_x_detect[i]), color="k", rotation=90)
    ax1.scatter(del_x_lens,del_x_detect, color="b")
    # indicate locations of FT{Lyot}
    ax1.scatter(loc_lens1_fpt_rel, del_x_detect,color="r")
    # indicate locations of Barlow lens (note subtraction, because x-axis is relative to current lens 1)
    ax1.scatter(np.subtract(loc_Barlow_abs,loc_R1_lens_current), del_x_detect,color="k")
    ax1.set_xlabel("lens 1 displacement (mm)")
    ax1.set_ylabel("blue: detector displacement (mm)\nred: location of focus of lens 1 FT{Lyot} plane\nblack: location of Barlow lens")

    # indicate 1 focal length away from lens, where we expect FT{Lyot} to be
    #ft_pos_line = np.add(del_x_lens,foc_lens_1_test[num_foc])
    #ax1.annotate("FT location", (del_x_lens[1],ft_pos_line[1]), color="k")
    #ax1.plot(del_x_lens, ft_pos_line, color="k", linestyle=":")
    #ax1.fill_between(del_x_lens, -100, 0, color="gray")
    ax1.set_ylim([0,200])
    #ax1.set_title("Lens inside dewar")

    # current lens 1
    ax1.annotate("current lens 1", (0,2), color="k")
    ax1.axvline(x=0, color="gray", linestyle="--")
    #ax1.annotate("current detect", (-5,116.05), color="k")
    #ax1.axhline(y=116.05, color="gray", linestyle="--")

    # cold shield
    ax1.annotate("cold shield", (44.35,2), color="k")
    ax1.axvline(x=loc_cold_shield-loc_R1_lens_current, color="gray", linestyle="--")
    #ax1.annotate("cold shield", (-5,44.35), color="k")
    #ax1.axhline(y=44.35, color="gray", linestyle="--")

    # dewar window
    ax1.annotate("dewar window", (98.95,2), color="k")
    ax1.axvline(x=loc_dewar_window-loc_R1_lens_current, color="gray", linestyle="--")
    #ax1.annotate("dewar window", (-5,98.95), color="k")
    #ax1.axhline(y=98.95, color="gray", linestyle="--")

    # current detector
    ax1.annotate("current detect", (116.05,2), color="k")
    ax1.axvline(x=loc_detector_current-loc_R1_lens_current, color="gray", linestyle="--")
    #ax1.annotate("current detect", (-5,116.05), color="k")
    #ax1.axhline(y=116.05, color="gray", linestyle="--")

    # add absolute x axis
    ax2 = ax1.twiny()
    ax2.set_xticks( ax1.get_xticks() )
    ax2.set_xbound(ax1.get_xbound())
    ax2.set_xticklabels([loc_R1_lens_current+x for x in ax1.get_xticks()])
    ax2.set_title("Absolute position (from mirror)")

    # add absolute y axis
    ax3 = ax1.twinx()
    ax3.set_yticks( ax1.get_yticks() )
    ax3.set_ybound(ax1.get_ybound())
    ax3.set_yticklabels([loc_detector_current+x for x in ax1.get_yticks()])
    ax3.set_ylabel("Absolute position (from mirror)")

    ax1.set_xlim([-20,150])

    plt.suptitle("lens 1 physical f = " + str(foc_lens_1_test[num_foc]) + " mm")

    string_foc = str(foc_lens_1_test[num_foc]).replace(".","_")
    string_full = "figs/" + string_foc + ".png"
    plt.tight_layout()
    plt.savefig(string_full, edgecolor="white")
    plt.close()
    print("Wrote " + string_full)
