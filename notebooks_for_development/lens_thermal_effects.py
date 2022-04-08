#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Finds rough focus changes due to thermal effects on lenses

# Created 2022 Mar. 15 by E.S.


# In[1]:


import numpy as np


# In[2]:


def del_f(f_init, del_t, T_const, alpha_H):
    '''
    f_init: focal length of system (assumed length of housing)
    del_t: change in temp
    T_const: thermal glass constant
    alpha_H: thermal expansion coefficient of housing
    '''
    
    return -f_init*del_t*(T_const + alpha_H)


# In[3]:


# thermal glass constants

T_BK7 = -1e-6 # VIS; p. 133
T_ZnS = 25e-6 # IR; p. 133
T_ZnSe = 36e-6 # IR; p. 133


# In[6]:


# CTE of Al is 21 to 24 (10-6 / °C))

CTE_Al = 22.5e-6


# In[10]:


# Cooling from room temp (293 K) to 77 K

test_BK7 = del_f(f_init = 100, del_t = 77-293, T_const=T_BK7, alpha_H=CTE_Al)
test_ZnS = del_f(f_init = 100, del_t = 77-293, T_const=T_ZnS, alpha_H=CTE_Al)

print("test_BK7", test_BK7)
print("test_ZnS", test_ZnS)


# In[ ]:




