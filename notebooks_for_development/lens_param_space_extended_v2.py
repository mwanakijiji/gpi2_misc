#!/usr/bin/env python
# coding: utf-8

# This is for some trial-and-error to see what focal lengths we might need

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# si in terms of so and f
def si(so_pass,f_pass):

    si_result = np.divide(so_pass,np.subtract(np.divide(so_pass,f_pass),1.))

    return si_result


# try  moving lens and detector both out
del_x_lens = np.arange(-10., 130., step=3.0) # displacement of lens (might be bumping into walls and elements)

so_test = np.add(del_x_lens,106.7+21.3)

# choice of focal lengths
foc_test = np.linspace(50., 175., num=251)

#abs_mag_max = 0.738 # mag for 10 pixel buffer on each side
abs_mag_max = 0.6912 # mag for filling 90% of shortest dimension (buffer of 5% on top, 5% on bottom)
#abs_mag_max = 0.906640625 # GPI 1.0 req

# loop over possible focal lengths
for num_foc in range(0,len(foc_test)):

    # find the si array
    si_array = si(so_pass = so_test, f_pass = foc_test[num_foc])

    # find needed detector displacement
    del_x_detect = np.subtract(np.add(so_test,si_array),128.+116.05)

    # find (abs val of) magnifications
    mag_array = np.divide(si_array,so_test)

    # print FYI stuff
    print("-----------------")
    print("f = " + str(foc_test[num_foc]))
    #import ipdb; ipdb.set_trace()
    df = pd.DataFrame(del_x_lens, columns=["del_x_lens"])
    df["del_x_detect"] = del_x_detect
    df["mag_array"] = mag_array
    df["si"] = si_array
    df["so"] = so_test
    print(df)

    fig, ax1 = plt.subplots(1, 1, figsize=(15,5))

    # subplot for lens inside dewar
    for i, txt in enumerate(mag_array):
        if (np.round(txt,3) > abs_mag_max):
            # exceeds limit of magnification
            color_string = "r"
        else:
            color_string = "k"
        ax1.annotate(str(np.round(txt,3)), (del_x_lens[i], del_x_detect[i]), color=color_string)
    ax1.scatter(del_x_lens,del_x_detect)
    ax1.set_xlabel("lens displacement (mm)")
    ax1.set_ylabel("detector displacement (mm)")

    # indicate 1 focal length away from lens, where we expect FT{Lyot} to be
    #ft_pos_line = np.add(del_x_lens,foc_test[num_foc])
    #ax1.annotate("FT location", (del_x_lens[1],ft_pos_line[1]), color="k")
    #ax1.plot(del_x_lens, ft_pos_line, color="k", linestyle=":")
    #ax1.fill_between(del_x_lens, -100, 0, color="gray")
    ax1.set_ylim([0,200])
    ax1.set_title("Lens inside dewar")

    # cold shield
    ax1.annotate("cold shield", (44.35,2), color="k")
    ax1.axvline(x=44.35, color="gray", linestyle="--")
    #ax1.annotate("cold shield", (-5,44.35), color="k")
    #ax1.axhline(y=44.35, color="gray", linestyle="--")

    # dewar window
    ax1.annotate("dewar window", (98.95,2), color="k")
    ax1.axvline(x=98.95, color="gray", linestyle="--")
    #ax1.annotate("dewar window", (-5,98.95), color="k")
    #ax1.axhline(y=98.95, color="gray", linestyle="--")

    # current detector
    ax1.annotate("current detect", (116.05,2), color="k")
    ax1.axvline(x=116.05, color="gray", linestyle="--")
    #ax1.annotate("current detect", (-5,116.05), color="k")
    #ax1.axhline(y=116.05, color="gray", linestyle="--")
    plt.title("f = " + str(foc_test[num_foc]) + " mm")

    string_foc = str(foc_test[num_foc]).replace(".","_")
    string_full = "figs/" + string_foc + ".png"
    plt.savefig(string_full, edgecolor="white")
    print("Wrote " + string_full)
