#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This determines the path of rays in simple geometrical ray traces,
# relative to apertures; and also finds errors

# Created 2022 Apr. 25 by E.S.


# In[1]:


import matplotlib.pyplot as plt
import numpy as np


# In[2]:


# locations of elements (all mm) are relative to the flat fold mirror

loc_obj = -106.7
loc_lens = 40.
rad_lens = 5.25 # radius of lens

# sizes of elements (all mm) are ito radii from center path

names_apertures_array = ["pupil",
                         "r4: cold shield", 
                         "r5: dewar window", 
                         "detector"]

radii_apertures_array = np.array([5., 11.,8.,4.72])

locs_apertures_array = np.array([loc_obj, 65.65, 120.25, 137.35])


# In[5]:


# path of ray 1: from top of image, optically parallel until lens; then focus at center path
# path of ray 2: same origin, but going in single path through center of lens to 'top' of image

# radial extent of ray 1 from center path
def rays_radial_extent(x_pos):
    
    if (x_pos < loc_lens):
        
        # distance between object and lens
        dist_obj_lens = np.subtract(loc_lens,loc_obj)
        
        y_extent_1 = radii_apertures_array[0] # ray is at the height of the object height
        y_extent_2 = np.divide(radii_apertures_array[0],dist_obj_lens) * np.subtract(loc_lens, x_pos)
        
    elif (x_pos > loc_lens):
        
        # distance between lens and detector
        dist_lens_detec = locs_apertures_array[-1] - loc_lens
        
        y_extent_1 = np.divide(rad_lens,dist_lens_detec) * np.subtract(locs_apertures_array[-1],x_pos)
        y_extent_2 = np.subtract(x_pos,loc_lens) * np.divide(radii_apertures_array[-1],dist_lens_detec)
        
    return y_extent_1, y_extent_2


# In[8]:


for t in range(0,len(radii_apertures_array)):

    abs_extent_1, abs_extent_2 = rays_radial_extent(locs_apertures_array[t])
    margin_extent_1 = np.subtract(radii_apertures_array,abs_extent_1)
    margin_extent_2 = np.subtract(radii_apertures_array,abs_extent_2)
    
    print("-----")
    print("APERTURE: ", names_apertures_array[t])
    print("Ray 1: Absolute extent of ray from parallel:", abs_extent_1)
    print("Ray 1: Aperture extent of aperture beyond rays:", margin_extent_1[t])
    print("Ray 2: Absolute extent of ray from parallel:", abs_extent_2)
    print("Ray 2: Aperture extent of aperture beyond rays:", margin_extent_2[t])
    if (margin_extent_1[t] < 0):
        print("VIGNETTING OF RAY 1 !!")
    if (margin_extent_2[t] < 0):
        print("VIGNETTING OF RAY 2 !!")


# In[ ]:





# In[ ]:




