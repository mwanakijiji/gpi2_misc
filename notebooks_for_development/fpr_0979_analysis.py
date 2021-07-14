#!/usr/bin/env python
# coding: utf-8

# In[7]:


# This reads in FITS-format files of the GPI1 filter transmission curves, then fits them
# to spectra of corresponding bands in IFS images to determine approximate spectral resolution.

# The IFS illuminations are simply a broadband source as seen through a particular filter. They
# are not of calibration lamps, which are not available to us---so this procedure finds resolution
# only in this makeshift, approximate way.

# Created 2021 July 14 by E.S.


# In[1]:


from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import glob
from photutils import DAOStarFinder
import pandas as pd
from scipy import signal
import os

get_ipython().run_line_magic('matplotlib', 'qt')


# In[17]:


stem_ifs_data = "/Users/bandari/Documents/git.repos/gpi2_misc/notebooks_for_development/data/fpr_0979/"

file_list_direct = glob.glob(stem_ifs_data + "direct_images/*fits")
file_list_nrm = glob.glob(stem_ifs_data + "nrm/*fits")


# In[18]:


file_list_direct = np.sort(file_list_direct)
file_list_nrm = np.sort(file_list_nrm)


# In[19]:


# Part 1: Read in images of ASU (direct) and compare movements to those of PnC mirrors

# initialize dict
dict_direct = {"file_name":[],"x_coord":[],"y_coord":[]}

for file_num in range(0,len(file_list_direct)):
    
    print("---------")
    print(file_num)
    print(file_list_direct[file_num])
    
    hdul = fits.open(file_list_direct[file_num])
    
    image_array = hdul[1].data[10]
    
    # blank off some of the image (to remove false peaks)
    image_array[:,:140] = 0
    print("NOTE PART OF THE ARRAY IS BEING BLANKED OFF")
    
    # check PnC movements
    #####
    
    daofind = DAOStarFinder(fwhm=10, threshold=3900, exclude_border=True)
    sources = daofind(image_array)

    # put the x,y coordinates into an array
    ptsEmpiricalPass = np.transpose(np.concatenate(([sources['xcentroid']], [sources['ycentroid']]),axis=0))
    print(ptsEmpiricalPass)
    
    # append values
    dict_direct["file_name"].append(os.path.basename(file_list_direct[file_num])) 
    dict_direct["x_coord"].append(ptsEmpiricalPass[0][0])
    dict_direct["y_coord"].append(ptsEmpiricalPass[0][1])


# In[32]:


# convert to dataframe
df_direct = pd.DataFrame.from_dict(dict_direct)

# add columns for mas from origin
PS = 14.1 # mas/pix
x_coord_origin = df_direct["x_coord"][0]
y_coord_origin = df_direct["y_coord"][0]
df_direct["x_mas_rel"] = np.multiply(PS,np.subtract(df_direct["x_coord"],x_coord_origin))
df_direct["y_mas_rel"] = np.multiply(PS,np.subtract(df_direct["y_coord"],y_coord_origin))

# do comparison


# In[33]:


print("Dataframe of direct images:")
print(df_direct)


# In[22]:


'''
plt.scatter(df_direct["x_coord"],df_direct["y_coord"])
plt.show()
'''


# In[12]:


# Part 2: Read in PUPIL images of ASU (NRM) and cross-correlate and compare movements to PnC mirrors

## ## MAY NEED TO AVERAGE ACROSS MULTIPLE SLICES

## ## NOTE ALSO THIS IS ONLY TO PIXEL-LEVEL PRECISION WITH CORRELATE2D

# read in first file
hdul_0 = fits.open(file_list_nrm[0])
image_array_0 = hdul_0[1].data[10]
image_array_0 = np.nan_to_num(image_array_0, copy=True, nan=0.0) # replace nans

for file_num in range(0,len(file_list_nrm)):
    
    print("---------")
    print(file_num)
    print(file_list_nrm[file_num])
    
    hdul = fits.open(file_list_nrm[file_num])
    
    image_array_this = hdul[1].data[10]
    image_array_this = np.nan_to_num(image_array_this, copy=True, nan=0.0) # replace nans
    
    # check PnC movements
    #####
    
    ## ## CROSS-CORRELATE WITH 1ST IMAGE
    corr = signal.correlate2d(image_array_this, image_array_0, boundary='symm', mode='same')
    y, x = np.unravel_index(np.argmax(corr), corr.shape)  # find the match
    print("Match (THIS IS ONLY TO PIXEL-LEVEL PRECISION WITH CORRELATE2D):")
    print(y,x)
    '''
    ## APPEND VALUES HERE
    dict_direct["file_name"].append(os.path.basename(file_list_nrm[file_num])) 
    dict_direct["x_coord"].append(x)
    dict_direct["y_coord"].append(y)
    '''


# In[ ]:


# convert to dataframe
df_direct = pd.DataFrame.from_dict(dict_direct)

# do comparison

