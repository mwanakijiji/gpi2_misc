#!/usr/bin/env python
# coding: utf-8

# This is predecessor code for reading in FITS images and checking that illumination
# scales as expected given shorter integration times ith subarrays

# Made from parent on 2021 July 7 by E.S.

from astropy.io import fits
import matplotlib.pyplot as plt
import photutils
from photutils import DAOStarFinder
import numpy as np
import pandas as pd
import glob
import os
from itertools import combinations


stem = "./data/fpr_0845/"

dict_data = {"file_name": [], "x_mm": [],
                  "y_mm": [], "x_pix": [],
                  "y_pix": [], "temp": []}

# read in full 2048x2048 array
hdul_full = fits.open(stem + "S20210508E0001.fits")
image_array_full = hdul_full[1].data

# read in two frames that are the same subarray
hdul_sub1 = fits.open(stem + "S20210508E0002.fits")
image_array_sub1 = hdul_sub1[1].data
hdul_sub2 = fits.open(stem + "S20210508E0003.fits")
image_array_sub2 = hdul_sub2[1].data

# get integration times
int_sub1 = hdul_sub1[1].header["ITIME"]
int_sub2 = hdul_sub2[1].header["ITIME"]
int_full = hdul_full[1].header["ITIME"]

# determine subregion (should be same in subarrays 1 and 2)
start_x1 = hdul_sub1[1].header["DETSTRTX"] # subarray start column, x (1-based)
end_x1 = hdul_sub1[1].header["DETENDX"] # subarray end column, x (1-based)
start_y1 = hdul_sub1[1].header["DETSTRTY"] # subarray start row, x (1-based)
end_y1 = hdul_sub1[1].header["DETENDY"] # subarray end row, x (1-based)
print("Subarray 1 coords (1-based):")
print(start_x1)
print(end_x1)
print(start_y1)
print(end_y1)
print("Integration time:")
print(int_sub1)

start_x2 = hdul_sub2[1].header["DETSTRTX"] # subarray start column, x (1-based)
end_x2 = hdul_sub2[1].header["DETENDX"] # subarray end column, x (1-based)
start_y2 = hdul_sub2[1].header["DETSTRTY"] # subarray start row, x (1-based)
end_y2 = hdul_sub2[1].header["DETENDY"] # subarray end row, x (1-based)
print("Subarray 2 coords (1-based):")
print(start_x2)
print(end_x2)
print(start_y2)
print(end_y2)
print("Integration time:")
print(int_sub2)

print("----")
print("(The above sets of coords should be the same)")
print("----")

# select the corresponding subarray from the the full frame
image_array_full_subsec = image_array_full[start_y1-1:end_y1-1,start_x1-1:end_x1-1]

# print illuminations
sum_sub1 = np.nansum(image_array_sub1)
sum_sub2 = np.nansum(image_array_sub2)
sum_full_subsec = np.nansum(image_array_full_subsec)

# put data into arrays
int_array = np.array([int_sub1,int_sub2,int_full])
illum_array = np.array([sum_sub1,sum_sub2,sum_full_subsec])

# line of best fit
m, b = np.polyfit(int_array, illum_array, 1)
x_best = np.array([0,int_full])
y_best = np.add(np.multiply(m,x_best),b)

print("Best-fit counts at integration time of zero:")
print(y_best[0])

plt.plot(x_best,y_best,linestyle="--")
plt.scatter(int_array,illum_array)
plt.xlabel("Integration time (sec)")
plt.ylabel("Illumination (total counts)")
plt.savefig("test.png")
print("Saved figure")
'''
print(sum_sub1)
print(sum_sub2)
print(sum_full_subsec)
'''
# convert to DataFrame
#df_data = pd.DataFrame.from_dict(dict_data)
