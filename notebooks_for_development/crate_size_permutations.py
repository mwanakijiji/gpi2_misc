#!/usr/bin/env python
# coding: utf-8

# This is to calculate the volumes which will be needed for storing GPI2 crates

# Created 2021 July 22 by E.S.

import numpy as np
import itertools
import pandas as pd

# dimensions of crate exteriors (in)
dims_by_crate = {"Crate 1":[111,87,63],"Crate 2":[74,58,44],"Crate 3":[73,58,44],"Crate 4":[118,72,39],
                "Crate 5":[65,45,32],"Crate 6":[26,61,24],"Crate 7":[57,43,48],"Crate 8":[84,54,43]}

# thickness of crate wall (in)
slab_thick = 6

print("------")
print("Crate exterior dims (in): ")
print(dims_by_crate)
print("------")
print("Thickness of each slab (6 slabs for each crate) (in): ")
print(slab_thick)

# do permutations and add thickness to get dims of all the slabs, and put into another dict

# initialize dictionary with same keys as before
dims_by_slab = {key: [] for key in list(dims_by_crate.keys())}

# loop over each crate and append arrays with dimensions of each slab
for string_crate in list(dims_by_crate.keys()):
    perms_2_this_crate = itertools.combinations(dims_by_crate[string_crate],2)
    for perm_this in perms_2_this_crate:
        perm_array = np.array(list(perm_this))
        perm_array = np.append(perm_array,slab_thick)
        dims_by_slab[string_crate].append(perm_array)
        dims_by_slab[string_crate].append(perm_array) # a second time, for 2 faces

# convert to dataframe
df_dims_by_slab = pd.DataFrame.from_dict(dims_by_slab)

# rearrange
df_sep_dims_of_each_slab = pd.DataFrame(df_dims_by_slab.stack())
df_sep_dims_of_each_slab = df_sep_dims_of_each_slab.reset_index(level=-1, inplace=False)
df_sep_dims_of_each_slab.columns = ["parent_crate","dims"]

# split dims
df_sep_dims_of_each_slab[["slab_l","slab_w","slab_h"]] = pd.DataFrame(df_sep_dims_of_each_slab.dims.tolist(),
                                                       index= df_sep_dims_of_each_slab.index)

# sort
df_sep_dims_of_each_slab = df_sep_dims_of_each_slab.sort_values(by="slab_l")
df_sep_dims_of_each_slab = df_sep_dims_of_each_slab.reset_index(drop=True)

print("------")
print("All slabs:")
print(df_sep_dims_of_each_slab)

import ipdb; ipdb.set_trace()
