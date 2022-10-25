#!/usr/bin/env python
# coding: utf-8

# This reads in engineering FITS files from GPI and makes plots for the
# instrument test FPR 0852

# Created 2021 June 16 by E.S.

from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import glob

stem = "/Users/bandari/Documents/git.repos/gpi2_misc/notebooks_for_development/fpr_0852_integration_times/data/"

file_list_unsorted = glob.glob(stem + "*fits")
file_list = np.sort(file_list_unsorted)

# initialize pandas dataframe, and consituent arrays/lists
df = pd.DataFrame()

itime_array = np.nan*np.ones(len(file_list))
atten_array = np.nan*np.ones(len(file_list))
mean_flux_array = np.nan*np.ones(len(file_list))
median_flux_array = np.nan*np.ones(len(file_list))
data_sec_list = [""] * len(file_list) # subarray regions
file_name_list = [""] * len(file_list)

# Read in FITS files
for file_num in range(0,len(file_list)):

    hdu = fits.open(file_list[file_num])

    # mask bad pixels
    ifs_array = hdu[1].data

    # true integration time
    itime = hdu[1].header["ITIME"]
    # ASU attenuation (CORRECT?)
    atten = hdu[0].header["ARTINT"]
    # subarray
    data_sec = hdu[1].header["DATASEC"]

    # Subtract dark (?)

    # Measure flux
    mean_flux_val = np.nanmean(ifs_array)
    median_flux_val = np.nanmedian(ifs_array)

    # Populate arrays, lists
    itime_array[file_num] = itime
    atten_array[file_num] = atten
    median_flux_array[file_num] = median_flux_val
    mean_flux_array[file_num] = mean_flux_val
    data_sec_list[file_num] = data_sec
    file_name_list[file_num] = os.path.basename(file_list[file_num])

# put into DataFrame
df["file_name"] = file_name_list
df["itime"] = itime_array
df["atten"] = atten_array
df["mean_flux"] = mean_flux_array
df["median_flux"] = median_flux_array


# plot median fluxes as-is
plt.clf()
p0, p1 = np.polyfit(df["itime"], df["median_flux"], 1)
y_expect = np.add(np.multiply(p0,df["itime"]),p1)
plt.plot([np.min(df["itime"]),np.max(df["itime"])],
                 [np.min(y_expect),np.max(y_expect)], color="k", linestyle="--", alpha = 0.5, marker="")

plt.plot(df["itime"],df["median_flux"], marker='o', linestyle='')

plt.xlabel("True integration time (sec)")
plt.ylabel("Median flux (ADU/pixel)")
#plt.legend()
plt.savefig("test.png")

import ipdb; ipdb.set_trace()
df["commanded"] = np.linspace(0,900,num=21,endpoint=True)
# check commanded integration times
plt.clf()
plt.plot([0.,900.], [0.,900.], color="k", linestyle="--", alpha = 0.5, marker="")
plt.plot(df["commanded"],df["itime"], marker='o', linestyle='')
plt.xlabel("Commanded integration time (sec)")
plt.ylabel("True integration time (sec)")
#plt.legend()
plt.savefig("test_2.png")
