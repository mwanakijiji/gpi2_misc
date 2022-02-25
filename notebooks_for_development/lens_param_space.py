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
del_x_lens = np.linspace(-10., 50., num=16) # displacement of lens
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

    fig, ax = plt.subplots()
    for i, txt in enumerate(mag_array):
        if (np.round(txt,3) > abs_mag_max):
            # exceeds limit of magnification
            color_string = "r"
        else:
            color_string = "k"
        ax.annotate(str(np.round(txt,3)), (del_x_lens[i], del_x_detect[i]), color=color_string)
    ax.scatter(del_x_lens,del_x_detect)
    ax.set_xlabel("lens displacement (mm)")
    ax.set_ylabel("detector displacement (mm)")
    ax.axhline(y=foc_test[num_foc], color="k", linestyle="--")
    #ax.fill_between(del_x_lens, -100, 0, color="gray")
    ax.set_ylim([0,200])
    plt.title("f = " + str(foc_test[num_foc]) + " mm")

    string_foc = str(foc_test[num_foc]).replace(".","_")
    string_full = "figs/" + string_foc + ".png"
    plt.savefig(string_full, edgecolor="white")
    print("Wrote " + string_full)
