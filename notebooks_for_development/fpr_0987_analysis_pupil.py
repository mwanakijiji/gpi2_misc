#!/usr/bin/env python
# coding: utf-8

# This reduces the Pupil images for FPR 0987

# Created 2021 Aug. 18 by E.S.

from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import glob
import os
import scipy.signal
from itertools import combinations
from skimage import data
from skimage.feature import register_translation
from skimage.feature.register_translation import _upsampled_dft
from scipy.ndimage import fourier_shift

stem = "./data/fpr_0987/pupil_shift_images/"

file_list_pupil = np.sort(glob.glob(stem + "*fits"))

def bad_pix(input_array):
    # a really crude bad pixel masking

    output_array = np.copy(input_array)
    # define bad pixels as anything higher than 22k
    bool_ind = input_array > 22000
    output_array[bool_ind] = np.median(input_array)

    return output_array

# read in first image as a baseline
hdul = fits.open(file_list_pupil[0])
baseline_image = bad_pix(hdul[0].data)

# initialize dictionary
keyDict = {"file_name","x_off_pix","y_off_pix","error_pix"}
dict_offsets = dict([(key, []) for key in keyDict])

# loop over pupil images and find their displacements relative to the baseline image
for i in range(0,len(file_list_pupil)):

    hdul = fits.open(file_list_pupil[i])
    comparison_image = hdul[0].data

    offset_image = comparison_image

    # Code below shamelessly cribbed from
    # https://scikit-image.org/docs/0.13.x/auto_examples/transform/plot_register_translation.html

    # subpixel precision
    shift, error, diffphase = register_translation(baseline_image, offset_image, 100)

    fig = plt.figure(figsize=(8, 3))
    ax1 = plt.subplot(1, 3, 1)
    ax2 = plt.subplot(1, 3, 2, sharex=ax1, sharey=ax1)
    ax3 = plt.subplot(1, 3, 3)

    ax1.imshow(baseline_image, cmap='gray')
    ax1.set_axis_off()
    ax1.set_title('Reference image')

    ax2.imshow(offset_image.real, cmap='gray')
    ax2.set_axis_off()
    ax2.set_title('Offset image')

    # Calculate the upsampled DFT, again to show what the algorithm is doing
    # behind the scenes.  Constants correspond to calculated values in routine.
    # See source code for details.
    image_product = np.fft.fft2(baseline_image) * np.fft.fft2(offset_image).conj()
    cc_image = _upsampled_dft(image_product, 150, 100, (shift*100)+75).conj()
    ax3.imshow(cc_image.real)
    ax3.set_axis_off()
    ax3.set_title("Supersampled XC sub-area")
    plt.suptitle(os.path.basename(file_list_pupil[i])+"\nDetected subpixel offset (y, x): {}".format(shift))

    # save plot
    plt.savefig("pupil_shift_"+str(int(i))+".png", dpi=400)

    # update the dictionary
    dict_offsets["file_name"].append(os.path.basename(file_list_pupil[i]))
    dict_offsets["x_off_pix"].append(shift[1])
    dict_offsets["y_off_pix"].append(shift[0])
    dict_offsets["error_pix"].append(error)

# convert to DataFrame
df_offsets = pd.DataFrame.from_dict(dict_offsets)

# calculate micron offsets
# pixel scale is 14.1 mas/pix
# plate scale is 1.610 arcsec/mm
conv_factor = 14.1*np.divide(1.,10**3)*np.divide(1.,1.61)*10**3
df_offsets["x_off_um"] = np.multiply(df_offsets["x_off_pix"],conv_factor)
df_offsets["y_off_um"] = np.multiply(df_offsets["y_off_pix"],conv_factor)
df_offsets["error_um"] = np.multiply(df_offsets["error_pix"],conv_factor)

# make plot of all displacements
fig = plt.figure(figsize=(10,5))
plt.plot(df_offsets["x_off_um"], marker="o", label="x offset")
plt.plot(df_offsets["y_off_um"], marker="o", label="y offset")
plt.plot(df_offsets["error_um"], marker="o", label="error")
plt.plot(np.sqrt(np.power(df_offsets["x_off_um"],2)+np.power(df_offsets["y_off_um"],2)), marker="o", label="total offset")
plt.xlabel("Trial number")
plt.ylabel("Shift (microns)")
plt.legend()
plt.savefig("junk_plot.png", dpi=400)
