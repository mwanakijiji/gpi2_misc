#!/usr/bin/env python
# coding: utf-8

# This reads in data about the IFS PSF centers (as measured by the GPI DPL), and commanded and
# sensed CAL-IFS PnC mirrors

# Created from parent 2021 July 26 by E.S.

from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# read in data on PnC mirror positions, PSF center, etc.
# ref: Google Sheet "Log FPR 0979: IFS Optical Feed"
df_dither = pd.read_csv("./data/fpr_0979/direct_image_data.txt", delim_whitespace=True)

print("Images made with PnC movements: ")
print(df_dither)

# convert PSF centroid pixels on detector to mas
PS = 14.1 # plate scale 14.1 mas/pix
# note there are two different zero points being subtracted off here
df_dither["x_mas"] = np.multiply(PS,np.subtract(df_dither["x_dpl"],df_dither["x_dpl"][0]))
df_dither["y_mas"] = np.multiply(PS,np.subtract(df_dither["y_dpl"],df_dither["y_dpl"][13]))

# find best-fit lines: x commands (note units are all in mas here)
idx_skip_7 = [0,1,2,3,4,5,6,8,9,10,11,12,13] # skip index 7, because it looks like a bad centroid
x_move_m, x_move_b = np.polyfit(df_dither["x_cmd"][idx_skip_7],df_dither["x_mas"][idx_skip_7], deg=1)
# find best-fit lines: y commands
y_move_m, y_move_b = np.polyfit(df_dither["y_cmd"][13:],df_dither["y_mas"][13:], deg=1)

# find scatter between measured PSF centers and best-fit
best_fit_trend_x = np.add(np.multiply(df_dither["x_cmd"][idx_skip_7],x_move_m),x_move_b)
resids_x = np.subtract(df_dither["x_mas"][idx_skip_7],best_fit_trend_x)
best_fit_trend_y = np.add(np.multiply(df_dither["y_cmd"][13:],y_move_m),y_move_b)
resids_y = np.subtract(df_dither["y_mas"][13:],best_fit_trend_y)

# print scatter
print("--------")
print("Stdev of scatter in x movements around best-fit line (in mas):")
print(np.std(resids_x))
print("--------")
print("Stdev of scatter in y movements around best-fit line (in mas):")
print(np.std(resids_y))

# movements in x, pixels
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
file_name_x = "junk_pnc_x.png"
plt.savefig(file_name_x, dpi=300, bbox_inches='tight')
print("Wrote out " + file_name_x)

# movements in y, pixels
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
file_name_y = "junk_pnc_y.png"
plt.savefig(file_name_y, dpi=300, bbox_inches='tight')
print("Wrote out " + file_name_y)
