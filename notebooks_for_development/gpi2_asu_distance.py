#!/usr/bin/env python
# coding: utf-8

# This computes necessary distances to move the ASU on GPI, given the entrance
# scale of the telescope

# Created 2021 May 28 by E.S.

import numpy as np

# input window plate scale
ps_input = 1.610 # arcsec/mm

# find needed motion (in mm) for N lambda/D

#N = 4 # lambda/D
#wavel_lambda = 1.6 # in um
D = 7.7701 # in m

def move_mm(N,wavel_lambda):

    lambda_D_rad = N*np.divide(np.divide(wavel_lambda,1e6),D) # rad
    lambda_D_asec = 206265.*lambda_D_rad

    return lambda_D_asec
