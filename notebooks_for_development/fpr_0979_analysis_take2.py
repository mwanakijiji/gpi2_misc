#!/usr/bin/env python
# coding: utf-8

# In[7]:


# This reads in data about the IFS PSF centers (as measured by the GPI DPL), and commanded and 
# sensed CAL-IFS PnC mirrors 

# Created from parent 2021 July 26 by E.S.


# In[1]:


from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

get_ipython().run_line_magic('matplotlib', 'inline')


# In[3]:


# read in data on PnC mirror positions, PSF center, etc.

df_dither = pd.read_csv("./data/fpr_0979/direct_image_data.txt", delim_whitespace=True)


# In[4]:


print("Images made with PnC movements: ")
print(df_dither)


# In[20]:


# movements in x

fig, axs = plt.subplots(1, 2, figsize=(13, 6), sharey=False)

axs[0].scatter(df_dither["x_cmd"][0:13],df_dither["x_dpl"][0:13])
axs[0].set_xlabel("Commanded movement, PnC (mas, x)")
axs[0].set_ylabel("PSF center (x, pixels)")
axs[0].ticklabel_format(useOffset=False)

axs[1].scatter(df_dither["x_cmd"][0:13],df_dither["y_dpl"][0:13])
axs[1].set_xlabel("Commanded movement, PnC (mas, x)")
axs[1].set_ylabel("PSF center (y, pixels)")
axs[1].ticklabel_format(useOffset=False)

plt.tight_layout()
fig.suptitle("DPL-measured centers of PSF\nafter PnC movements in x", y=1.08)
plt.savefig("junk_pnc_x.png", dpi=300)


# In[19]:


# movements in y

fig, axs = plt.subplots(1, 2, figsize=(13, 6), sharey=False)

axs[0].scatter(df_dither["y_cmd"][13:],df_dither["x_dpl"][13:])
axs[0].set_xlabel("Commanded movement, PnC (mas, x)")
axs[0].set_ylabel("PSF center (x, pixels)")
axs[0].ticklabel_format(useOffset=False)

axs[1].scatter(df_dither["y_cmd"][13:],df_dither["y_dpl"][13:])
axs[1].set_xlabel("Commanded movement, PnC (mas, x)")
axs[1].set_ylabel("PSF center (y, pixels)")
axs[1].ticklabel_format(useOffset=False)

plt.tight_layout()
fig.suptitle("DPL-measured centers of PSF\nafter PnC movements in y", y=1.08)
plt.savefig("junk_pnc_y.png", dpi=300)

