#!/usr/bin/env python
# coding: utf-8

# This reads in reduced FITS frames of calibration lamps, extracts
# info from the header, and returns resolution

# Created 2021 Sept. 22 by E.S.

import os
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt

stem = "/Users/bandari/Documents/git.repos/gpi2_misc/notebooks_for_development/data/fpr_0620_ver2/"

# read in 281x281x5 wavelength calibration cubes, extract dispersion w (in um/pix)

file_H_xe = "H_band/xe_lamp/S20200118S0327_H_wavecal.fits"
image_H_xe = fits.open(stem + file_H_xe)

file_H_ar = "H_band/ar_lamp/S20200118S0355_H_wavecal.fits"
image_H_ar = fits.open(stem + file_H_ar)

file_Y_ar = "Y_band/ar_lamp/S20200118S0454_Y_wavecal.fits"
image_Y_ar = fits.open(stem + file_Y_ar)

file_J_ar = "J_band/ar_lamp/S20200118S0444_J_wavecal.fits"
image_J_ar = fits.open(stem + file_J_ar)

file_K1_xe = "K1_band/xe_lamp/S20140425S0481_K1_wavecal.fits"
image_K1_xe = fits.open(stem + file_K1_xe)

file_K2_xe = "K2_band/xe_lamp/S20140317S0035_K2_wavecal.fits"
image_K2_xe = fits.open(stem + file_K2_xe)


# mean filter wavelengths (in um)
# Source: SVO filter service

mean_Y = 1.047154
mean_J = 1.234411
mean_H = 1.647298
mean_K1 = 2.042490
mean_K2 = 2.251543

# resolution is found by using the dispersion w in the found wavelength solution
# conforming to the relation in Eqn. (1) in Woolf+ 2014 SPIE:
# x = x0 + sinθ((λ−λ0)/w) and y=y0 cosθ((λ−λ0)/w)

# wavecal FITS file headers say
'''
HISTORY  Wavelength solution File Format:
HISTORY  Dispersion for each spectrum is defined as
HISTORY  lambda=w * (sqrt((x-x0)^2+(y-y0)^2))+lambda0
HISTORY     Slice 1:  Y-positions (y0) of spectra (Y=spectral direction) at [lam
HISTORY bda0]
HISTORY     Slice 2:  X-positions (x0) of spectra at [lambda0]
HISTORY     Slice 3:  lambda0 [um]
HISTORY     Slice 4:  dispersion w [um/pixel]
HISTORY     Slice 5:  tilts of spectra [radians]
'''

# check dispersion in five locations: near corners of lenslet array, and in center
def print_res(wavel_mean, image_pass, fwhm_pass=2):
    '''
    Prints the average resolution, based on the mean wavelength of the filter and the dispersion

    INPUTS:
    wavel_mean: mean wavelength of filter
    image_pass: cube of wavelength calibration
    fwhm_pass: FWHM of spectra (around 2)
    '''

    # dispersions are in units of um/pixel

    w_top_left = image_pass[1].data[3,182,36]
    w_top_right = image_pass[1].data[3,248,180]
    w_bottom_left = image_pass[1].data[3,38,99]
    w_bottom_right = image_pass[1].data[3,99,247]
    w_center = image_pass[1].data[3,140,140]

    w_all = np.array([w_top_left,w_top_right,w_bottom_left,w_bottom_right,w_center])

    # average resolution is central wavelength divided by dispersion across a single pixel.
    R_avg = np.divide(np.divide(wavel_mean,w_all),2)

    print("w, Top left; Top right; Bottom left; Bottom right; Center")
    print(w_all)
    print("Resolution, Top left; Top right; Bottom left; Bottom right; Center")
    print(R_avg)
    print("------------")
    print("------------")

    return

# print everything to screen

# H, Xe
print("H, Xe, using file " + str(os.path.basename(file_H_xe)))
print_res(wavel_mean=mean_H, image_pass=image_H_xe)

# H, Ar
print("H, Ar, using file " + str(os.path.basename(file_H_ar)))
print_res(wavel_mean=mean_H, image_pass=image_H_ar)

# Y, Ar
print("Y, Ar, using file " + str(os.path.basename(file_Y_ar)))
print_res(wavel_mean=mean_Y, image_pass=image_Y_ar)

# J, Ar
print("J, Ar, using file " + str(os.path.basename(file_J_ar)))
print_res(wavel_mean=mean_J, image_pass=image_J_ar)

# K1, Xe
print("K1, Xe, using file " + str(os.path.basename(file_K1_xe)))
print_res(wavel_mean=mean_K1, image_pass=image_K1_xe)

# K2, Xe
print("K2, Xe, using file " + str(os.path.basename(file_K2_xe)))
print_res(wavel_mean=mean_K2, image_pass=image_K2_xe)
