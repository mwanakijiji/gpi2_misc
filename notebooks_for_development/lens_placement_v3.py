#!/usr/bin/env python
# coding: utf-8

# This calculates where a lens should go in GPI to re-image the Lyot stop
# in the new PupilCam

# Created 2021 Dec 6 by E.S

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import product

# input parameter grids
n_l_array = [1.43,1.45,2.47] # np.linspace(1.2, 3.0, num=50, endpoint=True)
R1_array = np.linspace(1., 500., num=200, endpoint=True)
R1_array = np.append(R1_array,[1e8]) # to approximate at inf
R2_array = -np.linspace(1., 500., num=20, endpoint=True) # note negative
R2_array = np.append(R2_array,[-1e8]) # to approximate at inf
d_l_array = np.linspace(0.5, 15., num=40, endpoint=True)
alpha_array = np.linspace(10., 60., num=101, endpoint=True)
#M_array = np.linspace(-0.384,-0.9, num=200, endpoint=True)
#
def thick_lens(n_l_pass, R1_pass, R2_pass, d_l_pass):
    '''
    returns focal length, using Thick lensmaker's formula

    1/f = A * [B + C]
    '''

    A = np.subtract(n_l_pass,1.)

    B = np.subtract(1./R1_pass,1./R2_pass)

    C = np.divide(np.multiply(A,d_l_pass),np.multiply(d_l_pass,np.multiply(R1_pass,R2_pass)))

    f_inv = np.multiply(A,np.add(B,C))

    return 1./f_inv

# make DataFrame holding permutations of lens parameters
df = pd.DataFrame(product(n_l_array, R1_array, R2_array, d_l_array, alpha_array),
                  columns=["n_l","R1","R2","d_l","alpha"])

# find effective focal length for each combination
df["f"] = thick_lens(n_l_pass=df["n_l"],
                     R1_pass=df["R1"],
                     R2_pass=df["R2"],
                     d_l_pass=df["d_l"])

# find si and so based on the position of the lens from the mirror (alpha)
# find principal plane distances first
df["h1"] = -np.divide(
                    np.multiply(np.multiply(df["f"],np.subtract(df["n_l"],1.)),df["d_l"]),
                    np.multiply(df["R2"],df["n_l"])
                    )
df["h2"] = -np.divide(
                    np.multiply(np.multiply(df["f"],np.subtract(df["n_l"],1.)),df["d_l"]),
                    np.multiply(df["R1"],df["n_l"])
                    )
# note alpha is to the first FACE of the lens, not to h1
df["s_o"] = np.add(np.add(106.7,df["alpha"]),df["h1"])
#df["s_i"] = np.add(np.subtract(np.subtract(137.35,df["alpha"]),df["d_l"]),df["h2"]) # approximate, for now

# si depends on f (intrinsic to the lens) and sO (restriction of the experiment)
df["s_i"] = np.divide(np.multiply(df["s_o"],df["f"]),np.subtract(df["s_o"],df["f"]))

# get magnification, for later
df["M_mag"] = np.divide(-df["s_i"],df["s_o"])
# FYI, in terms of magnification,
# s_i = f*(1-M)
# s_o = f*(M-1)/M

df_physical0 = df.copy() # vestigial

# apply cut such that focal length is < 65 mm (focal point will be forced to be inside
# dewar in a later step)
#df_physical1 = df_physical0.where(df_physical0["f"] < 65).dropna()
df_physical1 = df_physical0.copy()

# apply cut such that si+so is close to (106.7+137.35) mm
df_physical2 = df_physical1.where(np.logical_and(
                                        np.add(df_physical1["s_i"],df_physical1["s_o"]) > 106.7+137.35-10,
                                        np.add(df_physical1["s_i"],df_physical1["s_o"]) < 106.7+137.35+10)).dropna()
# add a column to show residuals of si+so with needed
#df_physical2["siso_resid"] = np.subtract(np.add(df_physical2["s_i"],df_physical2["s_o"]),106.7+137.35)
#df_physical2["siso_sum"] = np.add(df_physical2["s_i"],df_physical2["s_o"])


# where is focal point inside dewar?
cond_compact = np.subtract(np.add(df_physical2["s_o"],df_physical2["f"]),106.7) < 65
df_physical3 = df_physical2.where(cond_compact).dropna()

# where is lens movement from current position small?
# add column to show important values (or residuals)
df_physical3["movement_resid"] = np.subtract(df_physical3["s_o"], 106.7 + 21.3)
#cond_siso = np.abs(df_physical2["siso_resid"]) < 2. # redundant
cond_movement = np.abs(df_physical3["movement_resid"]) < 30.
#df_physical3 = df_physical2.where(np.logical_and(cond_movement,cond_siso)).dropna()
df_physical4 = df_physical3.where(cond_movement).dropna()

# apply magnification constraint to fit image on detector: M_mag = -0.384 ideally,
# but we'll just settle with the smallest abs value of the magnification
df_physical5 = df_physical4.where(df_physical4["M_mag"]== np.max(df_physical4["M_mag"])).dropna()

print("---------------------------")
print("Number of remaining permutations: ")
print("Cut 0: " + str(len(df_physical0)))
print("Cut 1: " + str(len(df_physical1)))
print("Cut 2: " + str(len(df_physical2)))
print("Cut 3: " + str(len(df_physical3)))
print("Cut 4: " + str(len(df_physical4)))
print("Cut 5: " + str(len(df_physical5)))
import ipdb; ipdb.set_trace()
