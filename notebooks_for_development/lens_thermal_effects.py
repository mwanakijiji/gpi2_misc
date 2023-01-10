#!/usr/bin/env python
# coding: utf-8

# Finds rough focus changes due to thermal effects on lenses

# Created 2022 Mar. 15 by E.S.

import numpy as np

# focal length of system (assumed length of housing)
len_sys = 300. # (mm)

# thermo-optical coefficient, a.k.a. glass constant:
# gamma_thermopt = dndT/(N-1) + alpha, in Jamieson 1992, p. 134;
# (note 'thermo-optical coefficient' is sometimes used to refer to dn/dT)
T_BK7_Riedel = -1e-6 # VIS; ; Riedel 'Optical Design ... Systems,' p. 133
T_BK7_Jamieson = 1e-5 # Jamieson 1992, p. 134 (at unspecified temp)
T_ZnS = 25e-6 # IR; p. 133
T_ZnSe = 36e-6 # IR; p. 133

# index of refraction
n_BK7 = 1.5025 # at 1.4 um

# dn/dT
dndT_BK7 = -1.5e-6 # (/K); for 1.5 um at ~70K; but this does go to ~1e-6 at room temp (see Table 4 in Frey+ 2007)

# note Thorlabs' comment on N-BK7 substrate focus change: "the change in index per degree C is ~2.4 x 10-6 /°C." (email, 2022 Apr. 6)"

# CTEs
CTE_Al = 22.5e-6 #  (/K); CTE of Al is 21 to 24 (10-6 / °C)
CTE_NBK7 = 7.1e-6 # (/K) NBK7

# radii of curvature
R_T_LA1986C = 64.4 # (mm) for Thorlabs LA1986-C
R_T_LA1134C = 30.9 # (mm) for Thorlabs LA1134-C
R_T_LA1608C = 38.6 # (mm) for Thorlabs LA1608-C
R_N_KPX085AR18 = 32.507 # (mm) for Newport KPX085AR.18
R_N_KPX097AR16 = 64.600 # (mm) for Newport KPX097AR.16
R_N_KPX088AR18 = 32.507 # (mm) for Newport KPX088AR.18
R_E_67537 = 31.01 # (mm) for Edmund 67-537
R_E_67551 = 64.62 # (mm) for Edmund 67-551
R_E_67539 = 41.48 # (mm) for Edmund 67-539


# function describing entire system (1 lens)
def del_f_singlet(f_init, del_t, T_const, alpha_H):
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


# function describing entire system (2 lenses)
def del_f_doublet(f_init, f1_init, f2_init, del_t, T_const, alpha_H):
    '''
    INPUTS:
    f_init: focal length of system (assumed length of housing)
    f1_init: initial focal length of relay lens 1
    f2_init: initial focal length of relay lens 1
    del_t: change in temp
    T_const: thermal glass constant (assumed same for both lenses)
    alpha_H: thermal expansion coefficient of housing

    OUTPUT:
    del_f: change in focal length
    '''

    # term in square brackets in Eqn. 7.3, Chpt. 7
    term1 = f_init * (np.divide(T_const,f1_init) + np.divide(T_const,f2_init))  + alpha_H

    return -f_init * del_t * term1


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


print("------------------")
print("UNITS ALL IN MM")
print("------------------")

# Cooling from room temp (293 K) to 77 K
del_f_sys_singlet_BK7 = del_f_singlet(f_init = len_sys, del_t = 77-293, T_const=T_BK7_Riedel, alpha_H=CTE_Al)
print("del_f of an entire system with length", len_sys, "single NBK7 lens within an Al chamber:", del_f_sys_singlet_BK7)
del_f_sys_doublet_BK7 = del_f_doublet(f_init = len_sys, f1_init=120, f2_init=80, del_t = 77-293, T_const=T_BK7_Riedel, alpha_H=CTE_Al)
print("del_f of an entire system with length", len_sys, "doublet NBK7 lenses within an Al chamber:", del_f_sys_doublet_BK7)

f_orig = lensmakers_plane_convex(n_pass=n_BK7, R_pass=R_T_LA1986C)
R_new, n_new = parameters_change(R_in=R_T_LA1986C, n_in=n_BK7, CTE_pass=CTE_NBK7, dndT=dndT_BK7, del_T=77-293)
f_new = lensmakers_plane_convex(n_pass=n_new, R_pass=R_new)
print("Single lens, Thor LA1986C del_f:", f_new-f_orig)

f_orig = lensmakers_plane_convex(n_pass=n_BK7, R_pass=R_T_LA1134C)
R_new, n_new = parameters_change(R_in=R_T_LA1134C, n_in=n_BK7, CTE_pass=CTE_NBK7, dndT=dndT_BK7, del_T=77-293)
f_new = lensmakers_plane_convex(n_pass=n_new, R_pass=R_new)
print("Single lens, Thor LA1134C del_f:", f_new-f_orig)

f_orig = lensmakers_plane_convex(n_pass=n_BK7, R_pass=R_T_LA1608C)
R_new, n_new = parameters_change(R_in=R_T_LA1608C, n_in=n_BK7, CTE_pass=CTE_NBK7, dndT=dndT_BK7, del_T=77-293)
f_new = lensmakers_plane_convex(n_pass=n_new, R_pass=R_new)
print("Single lens, Thor LA1608C del_f:", f_new-f_orig)

f_orig = lensmakers_plane_convex(n_pass=n_BK7, R_pass=R_N_KPX085AR18)
R_new, n_new = parameters_change(R_in=R_N_KPX085AR18, n_in=n_BK7, CTE_pass=CTE_NBK7, dndT=dndT_BK7, del_T=77-293)
f_new = lensmakers_plane_convex(n_pass=n_new, R_pass=R_new)
print("Single lens, Newport KPX085AR18 del_f:", f_new-f_orig)

f_orig = lensmakers_plane_convex(n_pass=n_BK7, R_pass=R_N_KPX097AR16)
R_new, n_new = parameters_change(R_in=R_N_KPX097AR16, n_in=n_BK7, CTE_pass=CTE_NBK7, dndT=dndT_BK7, del_T=77-293)
f_new = lensmakers_plane_convex(n_pass=n_new, R_pass=R_new)
print("Single lens, Newport KPX097AR16 del_f:", f_new-f_orig)

f_orig = lensmakers_plane_convex(n_pass=n_BK7, R_pass=R_N_KPX088AR18)
R_new, n_new = parameters_change(R_in=R_N_KPX088AR18, n_in=n_BK7, CTE_pass=CTE_NBK7, dndT=dndT_BK7, del_T=77-293)
f_new = lensmakers_plane_convex(n_pass=n_new, R_pass=R_new)
print("Single lens, Newport KPX088AR18 del_f:", f_new-f_orig)

f_orig = lensmakers_plane_convex(n_pass=n_BK7, R_pass=R_E_67537)
R_new, n_new = parameters_change(R_in=R_E_67537, n_in=n_BK7, CTE_pass=CTE_NBK7, dndT=dndT_BK7, del_T=77-293)
f_new = lensmakers_plane_convex(n_pass=n_new, R_pass=R_new)
print("Single lens, Edmund 67537 del_f:", f_new-f_orig)

f_orig = lensmakers_plane_convex(n_pass=n_BK7, R_pass=R_E_67551)
R_new, n_new = parameters_change(R_in=R_E_67551, n_in=n_BK7, CTE_pass=CTE_NBK7, dndT=dndT_BK7, del_T=77-293)
f_new = lensmakers_plane_convex(n_pass=n_new, R_pass=R_new)
print("Single lens, Edmund 67551 del_f:", f_new-f_orig)

f_orig = lensmakers_plane_convex(n_pass=n_BK7, R_pass=R_E_67539)
R_new, n_new = parameters_change(R_in=R_E_67539, n_in=n_BK7, CTE_pass=CTE_NBK7, dndT=dndT_BK7, del_T=77-293)
f_new = lensmakers_plane_convex(n_pass=n_new, R_pass=R_new)
print("Single lens, Edmund 67539 del_f:", f_new-f_orig)

'''
f_orig = lensmakers_plane_convex(n_pass=n_BK7, R_pass=R_LA1134C)
print("f_orig", f_orig)
f_orig = lensmakers_plane_convex(n_pass=n_BK7, R_pass=R_LA1608C)
print("f_orig", f_orig)
'''

#test_ZnS = del_f_singlet(f_init = len_sys, del_t = 77-293, T_const=T_ZnS, alpha_H=CTE_Al)


#print("test_ZnS, within an Al chamber", test_ZnS)
