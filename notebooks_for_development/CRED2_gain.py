#!/usr/bin/env python
# coding: utf-8

# This reads in cubes of dark-subtracted frames (where the slices of a given cube are
# at different fps), and uses both cubes to calculate gain

# (Generate cubes with CRED2_analysis_eckhart.ipynb)

import os
from os import listdir
from os.path import isfile,join
import numpy as np
import matplotlib.pyplot as plt
import glob
from astropy.io import fits

# This is just setting up my filepaths; you should replace them with wherever your folders are
# note that the gain should be the same for these
stem = "/Users/bandari/Documents/git.repos/gpi2_misc/notebooks_for_development/data/"
file_name_cube_0 = stem + "linearity_subt_Low_gain_0.fits"
file_name_cube_1 = stem + "linearity_subt_Low_gain_1.fits"
array_fps = np.array([ 35,  45,  55,  65,  75,  85,  95, 105, 115, 125, 135, 145, 155,
       165, 175, 185, 195, 205, 215, 225])

# Ref. McLean, chpt. 9, p. 322; or http://spiff.rit.edu/classes/phys445/lectures/gain/gain.html

'''
flat_files = glob.glob(path_gain_flats + "*.raw")
dirs_darks_list = glob.glob(path_gain_darks + "*[0-9]")
darks_folders = [os.path.basename(i) for i in dirs_darks_list]

# sorted list of integration times
cadence_array = np.sort(np.array(darks_folders).astype(int))
exp_time_array = np.divide(1.,cadence_array)
'''

# Read in cubes of dark-subtracted flats (which have not been normalized) and find gain
# (one cube per integration time; note cubes are generated by CRED2_analysis_eckhart.ipynb)

dir_flat_subt = "/Users/bandari/Documents/git.repos/gpi2_misc/notebooks_for_development/"

file_names_flat_subt_cube = glob.glob(dir_flat_subt + "junk_flat_subt_*fits")

# loop over cubes (one cube per integration time) and find gain
# Ref. McLean, chpt. 9, p. 322; or http://spiff.rit.edu/classes/phys445/lectures/gain/gain.html
print("---------------------")
print("------- GAIN --------")

# open 1st of 2 cubes
hdul_0 = fits.open(file_name_cube_0)
cube_0 = hdul_0[0].data

# open 2nd of 2 cubes
hdul_1 = fits.open(file_name_cube_1)
cube_1 = hdul_1[0].data

var_adu_equiv_one_array = np.zeros(np.shape(cube_0)[0])
avg_adu_array = np.zeros(np.shape(cube_0)[0])

# loop through slices, each of which represents a different fps
for num_slice in range(0,np.shape(cube_0)[0]):

    # find the difference between the slices
    diff_slice = np.subtract(cube_0[num_slice,:,:],cube_1[num_slice,:,:])

    # find variance equivalent to that of one slice: var = (stdev_diff**2)/2
    rms = np.std(diff_slice)
    var_adu_equiv_one = np.divide(rms**2.,2.)

    # find average count level (actually median here, to remove bad pix; and of just one of the two cubes)
    avg_adu = np.median(cube_0[num_slice,:,:])

    # update arrays
    var_adu_equiv_one_array[num_slice] = var_adu_equiv_one
    avg_adu_array[num_slice] = avg_adu

coeffs_array = np.polyfit(x=avg_adu_array, y=var_adu_equiv_one_array, deg=1)
gain = np.divide(1.,coeffs_array[0])

plt.scatter(avg_adu_array,var_adu_equiv_one_array)
plt.ylabel("Variance [ADU]")
plt.xlabel("Avg [ADU]")
plt.show()

print("Gain:",gain)