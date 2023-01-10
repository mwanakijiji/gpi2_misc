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


stem = "/Users/bandari/Documents/postdoc_notre_dame/gpi2_testing/post_ship_tests/FPR_0845_detector_saturation/raw_data/"

file_list = glob.glob(stem + "*.fits")

# read in arrays, print integration times and subarray sizes
# (illumination useless, since CAL exit shutter was stuck)

for i in range(0,len(file_list)):

    hdul_full = fits.open(file_list[i])
    itime = hdul_full[1].header["ITIME"]

    start_x2 = hdul_full[1].header["DETSTRTX"] # subarray start column, x (1-based)
    end_x2 = hdul_full[1].header["DETENDX"] # subarray end column, x (1-based)
    start_y2 = hdul_full[1].header["DETSTRTY"] # subarray start row, x (1-based)
    end_y2 = hdul_full[1].header["DETENDY"] # subarray end row, x (1-based)

    ps = 14.16 # plate scale (mas/pix)

    print("------")
    print("ITIME", itime)
    print("X_SIZE (asec)", (1e-3)*ps*np.subtract(end_x2,start_x2))
    print("Y_SIZE (asec)", (1e-3)*ps*np.subtract(end_y2,start_y2))
