#!/usr/bin/env python
# coding: utf-8

# This is reading in FITS images and doing other stuff
# for analysis pertinent to test FPR 0987

# Created 2021 July 6 by E.S.

from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import glob

# # Part 1: Read in series of raw IFS images and see if opening and closing the OMSS shutter causes a change in the illumination
stem = "./data/fpr_0987/"

# # Plot changing illumination of AOWFS filter and "Show that the flux reduces for each successively narrower filter"

# set up data on AOWFS illumination
dict_aowfs = {"filter":["OPEN","600nm","700nm","800nm","900nm","910_to_900nm"],"counts":[2650,2600,2610,2325,810,225]}
df_aowfs = pd.DataFrame.from_dict(dict_aowfs)

plt.clf()
plt.plot(dict_aowfs["counts"],marker="o")
for t in range(0,len(dict_aowfs["counts"])):
    plt.annotate(dict_aowfs["filter"][t],xy=[t,dict_aowfs["counts"][t]])
plt.ylabel("AOWFS counts")
plt.xlabel("(unitless)")
plt.show()
#plt.savefig("junk_aowfs.png", dpi=300)
