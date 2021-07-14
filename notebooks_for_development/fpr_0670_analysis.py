#!/usr/bin/env python
# coding: utf-8

# This is predecessor code for reading in FITS images, finding centers of PSFs,
# and calculating the image scales, pairwise

# Made from parent fpr_0390_analysis.py on 2021 July 7 by E.S.

from astropy.io import fits
import matplotlib.pyplot as plt
import photutils
from photutils import DAOStarFinder
import numpy as np
import pandas as pd
import glob
import os
from itertools import combinations


def find_psf_centers(imagePass,fwhmPass,thresholdPass):
    '''
    Employ DAOPhot to find PSF coordinates

    RETURNS:
    ptsEmpiricalPass: empirically-found points
    '''
    daofind = DAOStarFinder(fwhm=fwhmPass, threshold=thresholdPass, exclude_border=True)
    sources = daofind(imagePass)

    # put the x,y coordinates into an array
    ptsEmpiricalPass = np.transpose(np.concatenate(([sources['xcentroid']], [sources['ycentroid']]),axis=0))

    return ptsEmpiricalPass


stem = "./data/fpr_0670/"
epochs_list = ["epoch_1/"]

for epoch_num in epochs_list:

    file_list = np.sort(glob.glob(stem + epoch_num + "*"))

    # initialize dictionary
    '''
    dict_data = {"file_name": [], "x_pix": [],
                      "y_pix": []}
    '''

    dict_data = {"file_name": [], "x_mm": [],
                      "y_mm": [], "x_pix": [],
                      "y_pix": [], "temp": []}

    for fits_num in range(0,len(file_list)):

        # read in reduced FITS file
        hdul = fits.open(file_list[fits_num])
        image_array = hdul[1].data
        temp = hdul[0].header["OMSATEMP"]

        asu_x_motor = hdul[0].header["TSRCPOSX"] # ASU source motor position, x
        asu_y_motor = hdul[0].header["TSRCPOSY"] # ASU source motor position, y

        #asu_x_motor=0
        #asu_y_motor=0


        # choose slice 10 (kind of arbitrary, but is bright)
        array_to_examine = image_array[10,:,:]

        # find centers of PSFs
        pt_centers = find_psf_centers(array_to_examine,fwhmPass=3,thresholdPass=1000)
        pt_centers = np.squeeze(pt_centers)

        print("Found PSF center:")
        print(pt_centers)
        print("ASU motor position (x,y; from FITS headers):")
        print(str([asu_x_motor,asu_y_motor]))

        # append
        dict_data["file_name"].append(os.path.basename(file_list[fits_num]))
        dict_data["x_pix"].append(pt_centers[0])
        dict_data["y_pix"].append(pt_centers[1])
        dict_data["x_mm"].append(asu_x_motor)
        dict_data["y_mm"].append(asu_y_motor)
        dict_data["temp"].append(temp)

    # convert to DataFrame
    df_data = pd.DataFrame.from_dict(dict_data)

    # prompt user for ASU positions in mm
    for elem_num in range(0,len(dict_data["file_name"])):

        print("Filename " + str(dict_data["file_name"][elem_num]))

        '''
        x_mm_input = input("Input ASU x_mm: ")
        dict_data["x_mm"][elem_num] = float(x_mm_input)
        y_mm_input = input("Input ASU y_mm: ")
        dict_data["y_mm"][elem_num] = float(y_mm_input)
        '''

    '''
    dict_data = {"file_name": ["yada1","yada2","yada3","daya4"],
                 "x_mm": [1.6,8.5,4.3,5.5],
                 "y_mm": [5.3,2.7,7.8,9.7],
                 "x_pix": [43,67,76,45],
                 "y_pix": [76,45,76,56],}
    '''
    df_data = pd.DataFrame.from_dict(dict_data)

    print("---------------")
    print("Data to be baselined: ")
    print(df_data)
    print("Avg. temp: ")
    print(np.mean(df_data["temp"]))
    print("Stdev. temp: ")
    print(np.std(df_data["temp"]))

    # find all baselines and put into new dataframe

    # get all combinations of endpoints, in sets of 2
    perm = combinations(np.arange(len(df_data)), 2)

    dict_baselines = {}

    dict_baselines = {"pt_1_name": [], "pt_2_name": [],
                      "pt_1_x_pix": [], "pt_1_y_pix": [],
                      "pt_2_x_pix": [], "pt_2_y_pix": [],
                      "pt_1_x_mm": [], "pt_1_y_mm": [],
                      "pt_2_x_mm": [], "pt_2_y_mm": []}

    # append names to dict
    for i in list(perm):

        dict_baselines["pt_1_name"].append(df_data["file_name"].iloc[i[0]])
        dict_baselines["pt_2_name"].append(df_data["file_name"].iloc[i[1]])
        dict_baselines["pt_1_x_pix"].append(df_data["x_pix"].iloc[i[0]])
        dict_baselines["pt_2_x_pix"].append(df_data["x_pix"].iloc[i[1]])
        dict_baselines["pt_1_y_pix"].append(df_data["y_pix"].iloc[i[0]])
        dict_baselines["pt_2_y_pix"].append(df_data["y_pix"].iloc[i[1]])
        dict_baselines["pt_1_x_mm"].append(df_data["x_mm"].iloc[i[0]])
        dict_baselines["pt_2_x_mm"].append(df_data["x_mm"].iloc[i[1]])
        dict_baselines["pt_1_y_mm"].append(df_data["y_mm"].iloc[i[0]])
        dict_baselines["pt_2_y_mm"].append(df_data["y_mm"].iloc[i[1]])

    df_baselines = pd.DataFrame.from_dict(dict_baselines)

    print("---------------")
    print("Baselines: ")
    print(df_baselines)

    # find distances in pixels, and in ASU movements in mm

    dict_baselines["piece_x_pix"] = np.power(np.subtract(dict_baselines["pt_1_x_pix"],dict_baselines["pt_2_x_pix"]),2.)
    dict_baselines["piece_y_pix"] = np.power(np.subtract(dict_baselines["pt_1_y_pix"],dict_baselines["pt_2_y_pix"]),2.)
    dict_baselines["d_pix"] = np.sqrt(np.add(dict_baselines["piece_x_pix"],dict_baselines["piece_y_pix"]))

    dict_baselines["piece_x_mm"] = np.power(np.subtract(dict_baselines["pt_1_x_mm"],dict_baselines["pt_2_x_mm"]),2.)
    dict_baselines["piece_y_mm"] = np.power(np.subtract(dict_baselines["pt_1_y_mm"],dict_baselines["pt_2_y_mm"]),2.)
    dict_baselines["d_mm"] = np.sqrt(np.add(dict_baselines["piece_x_mm"],dict_baselines["piece_y_mm"]))


    # convert mm distances to asec
    # GPI input window is 1.610 arcsec/mm

    dict_baselines["d_asec"] = np.multiply(1.610,dict_baselines["d_mm"]) # Gemini input image scale


    # add image scales

    dict_baselines["image_scale"] = np.divide(dict_baselines["d_asec"],dict_baselines["d_pix"]) # units asec/pix


    # average the plate scales

    ps_avg = np.mean(dict_baselines["image_scale"])
    ps_std = np.std(dict_baselines["image_scale"])

    print("For " + epoch_num + ",")
    print("PS avg (asec/pix): " + str(ps_avg))
    print("PS std (asec/pix): " + str(ps_std))
    print("--------------------")
    print("--------------------")
