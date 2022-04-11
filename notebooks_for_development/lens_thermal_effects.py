#!/usr/bin/env python
# coding: utf-8

# Finds rough focus changes due to thermal effects on lenses

# Created 2022 Mar. 15 by E.S.

import numpy as np

# focal length of system (assumed length of housing)
len_sys = 300. # (mm)

# thermal glass constants
T_BK7 = -1e-6 # VIS; p. 133
T_ZnS = 25e-6 # IR; p. 133
T_ZnSe = 36e-6 # IR; p. 133

# index of refraction
n_BK7 = 1.5025 # at 1.4 um

# note Thorlabs' comment on N-BK7 substrate focus change: "the change in index per degree C is ~2.4 x 10-6 /°C." (email, 2022 Apr. 6)"

# CTEs
CTE_Al = 22.5e-6 #  (/K); CTE of Al is 21 to 24 (10-6 / °C)
CTE_NBK7 = 7.1e-6 # (/K) NBK7

# radii of curvature
R_LA1986C = 64.4 # (mm) for Thorlabs LA1986-C
R_LA1134C = 30.9 # (mm) for Thorlabs LA1134-C
R_LA1608C = 38.6 # (mm) for LA1608-C

# function describing entire system
def del_f(f_init, del_t, T_const, alpha_H):
    '''
    INPUTS:
    f_init: focal length of system (assumed length of housing)
    del_t: change in temp
    T_const: thermal glass constant
    alpha_H: thermal expansion coefficient of housing

    OUTPUT:
    del_f: change in focal length
    '''

    return -f_init*del_t*(T_const + alpha_H)


# Lensmaker's Equation, for tweaking parameters individually
def lensmakers_plane_convex(n_pass, R_pass):
    '''
    INPUTS:
    n_pass: index of refraction of glass at that wavelength
    R_pass: radius of curved face of lens (note other face is flat) (mm)

    OUTPUT:
    f: focal length (note this is not inverse)
    '''

    inv_f = np.divide((n_pass - 1.),R_pass)

    return np.divide(1.,inv_f)


def parameters_change(R_in, n_in, CTE_pass, dndT, del_T):
    '''
    Returns changes of parameters as a function of temp

    INPUTS:
    R_in: original radius of lens face
    n_in: original index of refraction
    CTE_pass: CTE of lens substrate
    dndT: dn/dT for lens substrate
    del_T: change in temp
    '''

    R_out = R_in*(1. + CTE_pass*del_T)
    n_out = n_in + dndT*del_T

    return R_out, n_out


# Cooling from room temp (293 K) to 77 K
test_BK7 = del_f(f_init = len_sys, del_t = 77-293, T_const=T_BK7, alpha_H=CTE_Al)
print("test_BK7, within an Al chamber", test_BK7)

f_orig = lensmakers_plane_convex(n_pass=n_BK7, R_pass=R_LA1986C)
print("f_orig", f_orig)

R_new, n_new = parameters_change(R_in=R_LA1986C, n_in=n_BK7, CTE_pass=CTE_NBK7, dndT=0, del_T=77-293)
f_new = lensmakers_plane_convex(n_pass=n_new, R_pass=R_new)
print("f_new", f_new)
print("del_f", f_new-f_orig)

'''
f_orig = lensmakers_plane_convex(n_pass=n_BK7, R_pass=R_LA1134C)
print("f_orig", f_orig)
f_orig = lensmakers_plane_convex(n_pass=n_BK7, R_pass=R_LA1608C)
print("f_orig", f_orig)
'''

#test_ZnS = del_f(f_init = len_sys, del_t = 77-293, T_const=T_ZnS, alpha_H=CTE_Al)


#print("test_ZnS, within an Al chamber", test_ZnS)
