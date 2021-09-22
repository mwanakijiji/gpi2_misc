#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This reads in reduced FITS frames of calibration lamps, extracts 
# info from the header, and returns resolution

# Created 2021 Sept. 22 by E.S.


# In[39]:


import os
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt


# In[40]:


stem = "/Users/bandari/Documents/git.repos/gpi2_misc/notebooks_for_development/data/fpr_0620_ver2/"


# In[47]:


# read in 281x281x5 wavelength calibration cube, extract dispersion w (in um/pix)

file_H_xe = "H_band/xe_lamp/S20131208S0151_H_wavecal.fits"
image_H_xe = fits.open(stem + file_H_xe)

file_H_ar = "H_band/ar_lamp/---"
image_H_ar = fits.open(stem + file_H_xe)

file_Y_xe = "Y_band/xe_lamp/"
image_Y_xe = fits.open(stem + file_Y_xe)

file_Y_ar = "H_band/ar_lamp/---"
image_Y_ar = fits.open(stem + file_Y_xe)

file_J_xe = "H_band/xe_lamp/---"
image_J_xe = fits.open(stem + file_J_xe)

file_J_ar = "H_band/ar_lamp/---"
image_J_ar = fits.open(stem + file_H_xe)

file_K1_xe = "H_band/xe_lamp/---"
image_K1_xe = fits.open(stem + file_H_xe)

file_K1_ar = "H_band/ar_lamp/---"
image_K1_ar = fits.open(stem + file_H_xe)

file_K2_xe = "H_band/xe_lamp/---"
image_K2_xe = fits.open(stem + file_H_xe)

file_K2_ar = "H_band/ar_lamp/---"
image_K2_ar = fits.open(stem + file_H_xe)


# In[44]:


# mean wavelengths (in um) 
# Source: SVO filter service

mean_Y = 1.047154
mean_J = 1.234411
mean_H = 1.647298
mean_K1 = 2.042490
mean_K2 = 2.251543


# In[42]:


# Eqn. (1) in Woolf+ 2014:
# x = x0 + sinθ((λ−λ0)/w) and y=y0 cosθ((λ−λ0)/w)


# In[43]:


# FITS file headers say

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


# In[52]:


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
    
    print("Resolution, Top left; Top right; Bottom left; Bottom right; Center")
    print(R_avg)
    print("------------")
    
    return


# In[ ]:


# NOTE SOME OF THE BELOW WILL BE INAPPLICABLE DUE TO BAD WAVELENGTH SOLUTIONS WITH CERTAIN LAMPS


# In[53]:


# H, Xe
print("H, Xe, using file " + str(os.path.basename(file_H_xe)))
print_res(wavel_mean=mean_H, image_pass=image_H_xe)

# H, Ar
print("H, Ar, using file " + str(os.path.basename(file_H_ar)))
print_res(wavel_mean=mean_H, image_pass=image_H_ar)


# In[53]:


# Y, Xe
print("Y, Xe, using file " + str(os.path.basename(file_Y_xe)))
print_res(wavel_mean=mean_Y, image_pass=image_Y_xe)

# Y, Ar
print("Y, Ar, using file " + str(os.path.basename(file_Y_ar)))
print_res(wavel_mean=mean_Y, image_pass=image_Y_ar)


# In[53]:


# J, Xe
print("J, Xe, using file " + str(os.path.basename(file_J_xe)))
print_res(wavel_mean=mean_J, image_pass=image_J_xe)

# J, Ar
print("J, Ar, using file " + str(os.path.basename(file_J_ar)))
print_res(wavel_mean=mean_J, image_pass=image_J_ar)


# In[53]:


# K1, Xe
print("K1, Xe, using file " + str(os.path.basename(file_K1_xe)))
print_res(wavel_mean=mean_K1, image_pass=image_K1_xe)

# K1, Ar
print("K1, Ar, using file " + str(os.path.basename(file_K1_ar)))
print_res(wavel_mean=mean_K1, image_pass=image_K1_ar)


# In[53]:


# K2, Xe
print("K2, Xe, using file " + str(os.path.basename(file_K2_xe)))
print_res(wavel_mean=mean_K2, image_pass=image_K2_xe)

# K2, Ar
print("K2, Ar, using file " + str(os.path.basename(file_K2_ar)))
print_res(wavel_mean=mean_K2, image_pass=image_K2_ar)

