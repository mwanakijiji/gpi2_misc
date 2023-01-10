#!/usr/bin/env python
# coding: utf-8

# This is for reading in FITS images taken at different times, and checking
# differences between the PSFs (there shouldn't be any)

# Created 2021 June 29 by E.S.


from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import glob

stem = "./data/fpr_0972/"
data_1 = pd.read_csv(stem + "postship_cal_movement_20221102_1.csv", delim_whitespace=True)
data_2 = pd.read_csv(stem + "postship_cal_movement_20221102_2.csv", delim_whitespace=True)
data_3 = pd.read_csv(stem + "postship_cal_movement_20221102_3.csv", delim_whitespace=True)

# total ASU movement
data_1["asu_total"] = np.sqrt(np.power(np.subtract(data_1["x_asu_mm"],data_1["x_asu_mm"][0]),2)+np.power(np.subtract(data_1["y_asu_mm"],data_1["y_asu_mm"][0]),2))
data_2["asu_total"] = np.sqrt(np.power(np.subtract(data_2["x_asu_mm"],data_2["x_asu_mm"][0]),2)+np.power(np.subtract(data_2["y_asu_mm"],data_2["y_asu_mm"][0]),2))
data_3["asu_total"] = np.sqrt(np.power(np.subtract(data_3["x_asu_mm"],data_3["x_asu_mm"][0]),2)+np.power(np.subtract(data_3["y_asu_mm"],data_3["y_asu_mm"][0]),2))

# total TT
data_1["tt_total"] = np.sqrt(np.power(np.subtract(data_1["tip_avg_mas"],data_1["tip_avg_mas"][0]),2)+np.power(np.subtract(data_1["tilt_avg_mas"],data_1["tilt_avg_mas"][0]),2))
data_2["tt_total"] = np.sqrt(np.power(np.subtract(data_2["tip_avg_mas"],data_2["tip_avg_mas"][0]),2)+np.power(np.subtract(data_2["tilt_avg_mas"],data_2["tilt_avg_mas"][0]),2))
data_3["tt_total"] = np.sqrt(np.power(np.subtract(data_3["tip_avg_mas"],data_3["tip_avg_mas"][0]),2)+np.power(np.subtract(data_3["tilt_avg_mas"],data_3["tilt_avg_mas"][0]),2))

# plots (uncomment as needed)

'''
plt.clf()
plt.title("A1")
plt.scatter(data_1["asu_total"],data_1["tt_total"])
plt.show()
'''
plt.clf()
plt.title("Interrupted x-movements of ASU")
plt.scatter(data_1["x_asu_mm"],data_1["tip_avg_mas"])
plt.xlabel("ASU x (mm)")
plt.ylabel("tip (mas)")
plt.show() # (why is this not linear?)
'''
plt.clf()
plt.title("A2a")
plt.scatter(data_1["x_asu_mm"],data_1["tilt_avg_mas"])
plt.show() # (why is this not linear?)

plt.clf()
plt.title("A3a")
plt.scatter(data_1["y_asu_mm"],data_1["tip_avg_mas"])
plt.show() # (why is this not linear?)
'''
plt.clf()
plt.title("Interrupted y-movements of ASU")
plt.scatter(data_1["y_asu_mm"],data_1["tilt_avg_mas"])
plt.xlabel("ASU x (mm)")
plt.ylabel("tilt (mas)")
plt.show() # (why is this not linear?)
'''
plt.clf()
plt.title("A4")
plt.scatter(data_1["x_asu_mm"],data_1["tt_total"])
plt.show()

plt.clf()
plt.title("A5")
plt.scatter(data_1["y_asu_mm"],data_1["tt_total"])
plt.show()

#---

plt.clf()
plt.title("B1")
plt.scatter(data_2["asu_total"],data_2["tt_total"])
plt.show() # upside down parabola
'''
plt.clf()
plt.title("Continual x-movements of ASU")
plt.scatter(data_2["x_asu_mm"],data_2["tip_avg_mas"])
# find coefficients of most linear-looking realtions
asu_x_coeffs = np.polyfit(data_2["x_asu_mm"],data_2["tip_avg_mas"], 1)
plt.plot(data_2["x_asu_mm"],asu_x_coeffs[0]*data_2["x_asu_mm"] + asu_x_coeffs[1], linestyle="--")
plt.xlabel("ASU x (mm)")
plt.ylabel("tip (mas)")
plt.show() # linear
'''
plt.clf()
plt.title("B3")
plt.scatter(data_2["y_asu_mm"],data_2["tilt_avg_mas"])
plt.show()

plt.clf()
plt.title("B4")
plt.scatter(data_2["x_asu_mm"],data_2["tt_total"])
plt.show() # upside down parabola

plt.clf()
plt.title("B5")
plt.scatter(data_2["y_asu_mm"],data_2["tt_total"])
plt.show()

#---

plt.clf()
plt.title("C1")
plt.scatter(data_3["asu_total"],data_3["tt_total"])
plt.show() # upside down parabola

plt.clf()
plt.title("C2")
plt.scatter(data_3["x_asu_mm"],data_3["tip_avg_mas"])
plt.show()
'''
plt.clf()
plt.title("Continual y-movements of ASU")
plt.scatter(data_3["y_asu_mm"],data_3["tilt_avg_mas"])
asu_y_coeffs = np.polyfit(data_3["y_asu_mm"],data_3["tilt_avg_mas"], 1)
plt.plot(data_3["y_asu_mm"],asu_y_coeffs[0]*data_3["y_asu_mm"] + asu_y_coeffs[1], linestyle="--")
plt.xlabel("ASU y (mm)")
plt.ylabel("tilt (mas)")
plt.show() # linear
'''
plt.clf()
plt.title("C4")
plt.scatter(data_3["x_asu_mm"],data_3["tt_total"])
plt.show()

plt.clf()
plt.title("C5")
plt.scatter(data_3["y_asu_mm"],data_3["tt_total"])
plt.show() # upside down parabola
'''
#---

# find residuals when moving ASU in one direction only



#

asu_x_resids = np.subtract(data_2["tip_avg_mas"], asu_x_coeffs[0]*data_2["x_asu_mm"] + asu_x_coeffs[1])
asu_y_resids = np.subtract(data_3["tilt_avg_mas"], asu_y_coeffs[0]*data_3["y_asu_mm"] + asu_y_coeffs[1])

print("Tip residuals (mas): ", np.std(asu_x_resids))
print("Tilt residuals (mas): ", np.std(asu_y_resids))
