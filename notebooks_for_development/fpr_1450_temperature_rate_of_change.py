#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#%matplotlib qt


# In[2]:


stem = "/Users/bandari/Documents/git.repos/gpi2_misc/notebooks_for_development/data/"


# In[3]:


file_name = stem + "20220912_temperature.log"


# In[4]:


df = pd.read_csv(file_name, skiprows=7, names=["day","time","molyblock","tita_det_head","intermed_opt_bench",
                                               "intermed_block_ccr1","cold_tip_ccr2",
                                               "intermed_block_ccr2","cold_tip_ccr1","asic_strap",
                                               "opt_bench","cold_shield","output_a","output_b"])


# In[5]:


# get rid of non-numeric strings

molyblock = df["molyblock"].apply(pd.to_numeric, errors='coerce')
opt_bench = df["intermed_opt_bench"].apply(pd.to_numeric, errors='coerce')


# In[6]:


# turn time strings to time objects

df["full_time"] = pd.to_datetime(df['day'] + "T" + df['time'], format="%y/%m/%dT%H:%M:%S")


# In[7]:


# convert to cumulative mins

df["delta_t"] = df["full_time"] - df["full_time"][0]


# In[8]:


# find time and temp intervals (note one element at end will be bogus)

## MOLYBLOCK TEMPS ARE ERRONEOUS! BAD SENSOR

df["interval_t"] = np.subtract(df["delta_t"].dt.total_seconds(),np.roll(df["delta_t"].dt.total_seconds(),1))
opt_bench_dK = np.subtract(opt_bench,np.roll(opt_bench,1))
molyblock_dK = np.subtract(molyblock,np.roll(molyblock,1))


# In[9]:


# find rate of change of temp [K/min]

df["bench_dKdt"] = np.divide(opt_bench_dK,df["interval_t"]) * 60
df["molyblock_dKdt"] = np.divide(molyblock_dK,df["interval_t"]) * 60


# In[28]:


# plot absolute temps

plt.clf()
plt.plot(df["delta_t"][10:-10], molyblock[10:-10], label="Molyblock")
plt.plot(df["delta_t"][10:-10], opt_bench[10:-10], label="Bench")
#plt.plot(df["delta_t"][10:-10], df["intermed_block_ccr1"][10:-10].values, label="test")
plt.xlabel("Elapsed seconds")
plt.ylabel("Temp [K]")
plt.legend()
plt.savefig("junk_abs_temp.png")

'''
"molyblock","tita_det_head","intermed_opt_bench",
                                               "intermed_block_ccr1","cold_tip_ccr2",
                                               "intermed_block_ccr2","cold_tip_ccr1","asic_strap",
                                               "opt_bench","cold_shield","output_a","output_b"])
'''


# In[29]:


# plot change in temps

plt.clf()
plt.plot(df["delta_t"][10:-10],df["bench_dKdt"][10:-10], label="Bench")
plt.axhline(y=0.25, linestyle=":", color="gray")
plt.axhline(y=-0.25, linestyle=":", color="gray")
plt.legend()
plt.xlabel("Elapsed seconds")
plt.ylabel("dK/dt [K/min]")
plt.savefig("junk_change_temp.png")


# In[10]:


print("Stdev of Bench dKdt [K/min]", np.std(df["bench_dKdt"][10:-10]))
print("Stdev of Molyblock dKdt [K/min]; ERRONEOUS", np.std(df["molyblock_dKdt"][10:-10]))

