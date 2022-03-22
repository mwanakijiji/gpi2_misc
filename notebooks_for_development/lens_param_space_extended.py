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

    string_foc = str(foc_lens_1_test[num_foc]).replace(".","_")

    # find the si array (distance of image from lens)
    si_1_array = si(so_pass = so_1_array, f_pass = foc_lens_1_test[num_foc])

    # find needed detector displacement from current
    del_x_detect = np.subtract(
                                np.add(so_1_array,si_1_array),
                                loc_R1_lens_current+dist_lyot_to_mirror+dist_lens_to_si_current
                                )

    # find (abs val of) magnifications
    mag_1_array = np.divide(si_1_array,so_1_array)

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
    so_2 = -upstr_Barlow_dist
    # second image distance is that of the new detector location minus the Barlow location
    si_2 = np.subtract(del_x_detect+loc_detector_current,loc_Barlow_abs)
    foc_lens2_Barlow = f_needed(so_pass=so_2,
                        si_pass=si_2)
    mag_2_array = -np.divide(si_2,so_2) # magnification effect of Barlow alone
    #import ipdb; ipdb.set_trace()
    # calculate plate scale at FT{Lyot} plane IF the Barlow is in
    #PS_w_Barlow = np.divide(1.,np.multiply(foc_lens_1_test,mag_2_array))

    # absolute location of second image
    si_2_abs = np.add(loc_lens1_fpt_abs,np.add(foc_lens2_Barlow,si_2))

    # absolute location of detector
    loc_det_abs = np.add(del_x_detect,loc_detector_current)

    # consider a two-positive-lens solution (without a Barlow lens) and
    # find the distance between the focal point of lens 1 and the detector;
    # then any positive lens 2 that is inserted needs to have a positive focal
    # length less than this; this info is printed, but not plotted
    dist_focpt1_det = np.subtract(loc_det_abs,loc_lens1_fpt_abs)

    # absolute location of lens 1
    loc_lens1_abs = np.add(del_x_lens,loc_R1_lens_current)

    # plate scale of FT{Lyot} image on final detector: 1/(M2*f1); then convert to asec/mm
    PS_FTlyot = np.divide(1.,np.multiply(foc_lens_1_test[num_foc],mag_2_array)) * (3600.*360./(2.*np.pi))

    # print FYI stuff
    print("-----------------")
    print("f = " + str(foc_lens_1_test[num_foc]))
    #import ipdb; ipdb.set_trace()
    df = pd.DataFrame(del_x_lens, columns=["del_x_lens"])
    df["del_x_detect"] = del_x_detect
    df["loc_detect_abs"] = loc_det_abs
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

    plt.clf()
    fig, ax1 = plt.subplots(1, 1, figsize=(15,10))

    # annotate magnifications
    for i, txt in enumerate(mag_1_array):
        if (np.round(txt,3) > abs_mag_max):
            # exceeds limit of magnification
            color_string = "r"
        else:
            color_string = "k"
        ax1.annotate("M_1 = "+str(np.round(txt,3)) + ", ", (loc_lens1_abs[i], 7+loc_det_abs[i]), color=color_string, rotation=90)
    # annotate Barlow focal lengths
    for i, txt2 in enumerate(foc_lens2_Barlow):
        ax1.annotate("f_B = "+str(np.round(txt2,3)), (loc_lens1_abs[i], 107+loc_det_abs[i]), color="k", rotation=90)

    # new locations of detector
    ax1.scatter(loc_lens1_abs, loc_det_abs, color="b")

    # indicate locations of FT{Lyot}
    # (the y here is just to point the datapoint in a visually OK place)
    ax1.scatter(loc_lens1_fpt_abs, loc_det_abs, color="r")

    # indicate locations of Barlow lens (note subtraction, because x-axis is relative to current lens 1)
    # (the y here is just to point the datapoint in a visually OK place)
    ax1.scatter(loc_Barlow_abs, loc_det_abs, color="k")
    ax1.set_ylabel("Blue: absolute detector position (from mirror)")


    # indicate 1 focal length away from lens, where we expect FT{Lyot} to be
    #ft_pos_line = np.add(del_x_lens,foc_lens_1_test[num_foc])
    #ax1.annotate("FT location", (del_x_lens[1],ft_pos_line[1]), color="k")
    #ax1.plot(del_x_lens, ft_pos_line, color="k", linestyle=":")
    #ax1.fill_between(del_x_lens, -100, 0, color="gray")
    ax1.set_ylim([0,500])
    #ax1.set_title("Lens inside dewar")

    # current lens 1
    ax1.annotate("current lens 1", (loc_R1_lens_current,100), color="k")
    ax1.axvline(x=loc_R1_lens_current, color="gray", linestyle="--")
    #ax1.annotate("current detect", (-5,116.05), color="k")
    #ax1.axhline(y=116.05, color="gray", linestyle="--")

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

    # indicate new detector location
    #ax1.axvline(x=loc_det_abs

    # current detector
    ax1.annotate("current detect", (loc_detector_current,100), color="k")
    ax1.axvline(x=loc_detector_current, color="gray", linestyle="--")
    ax1.annotate("current detect", (0,loc_detector_current), color="k")
    ax1.axhline(y=loc_detector_current, color="gray", linestyle="--")
    ax1.set_xlabel("Absolute position of lens, etc. (from mirror)\nblue: lens 1 (mm)\nred: focus of lens 1 FT{Lyot} plane\nblack: Barlow lens")
    #ax1.annotate("current detect", (-5,116.05), color="k")
    #ax1.axhline(y=116.05, color="gray", linestyle="--")

    # add absolute x axis
    '''
    ax2 = ax1.twiny()
    ax2.set_title("lens 1 displacement (mm)")
    ax2.set_xticks( ax1.get_xticks() )
    ax2.set_xbound(ax1.get_xbound())
    ax2.set_xticklabels([x-loc_R1_lens_current for x in ax1.get_xticks()])


    # add absolute y axis
    ax3 = ax1.twinx()
    ax3.set_yticks( ax1.get_yticks() )
    ax3.set_ybound(ax1.get_ybound())
    ax3.set_yticklabels([x-loc_detector_current for x in ax1.get_yticks()])
    '''

    ax1.set_xlim([-20,150])

    plt.suptitle("lens 1 physical f = " + str(foc_lens_1_test[num_foc]) + " mm")

    string_full = "figs/" + string_foc + ".png"
    plt.tight_layout()
    plt.savefig(string_full, edgecolor="white")
    plt.close()
    print("Wrote " + string_full)
