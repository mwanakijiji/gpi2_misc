import numpy as np
import matplotlib.pyplot as plt

# Load TT data
stem = "/Users/bandari/Documents/postdoc_notre_dame/gpi2_testing/post_ship_tests/FPR_0970_tt_update_rates_precision/raw_data/" # this stem for post-ship
time, tip, tilt = np.loadtxt(stem + 'tt_sample_data.dat', delimiter=',', skiprows=1, dtype='float', unpack=True)

tiltlist = []
tiplist = []
timelist = []

tiplist.append(tip[0])
tiltlist.append(tilt[0])
timelist.append(time[0])

# remove repeat measurements of Tip and Tilt
for i in range(1,len(tip),1):

	if tip[i] == tiplist[-1]:
		pass
	else:
		tiplist.append(tip[i])
		tiltlist.append(tilt[i])
		timelist.append(time[i])

tipf = np.array(tiplist[:-1])
tiltf = np.array(tiltlist[:-1])
timef = np.array(timelist[:-1])

# print Std of TT and max time it took to update the data
print('Mean of tip and tilt (mas): ', np.mean(tipf), np.mean(tiltf))
print('Std of tip and tilt (mas): ', np.std(tipf), np.std(tiltf))
print('Std of normalised tip and tilt (mas): ', np.std(tipf/np.mean(tipf)), np.std(tiltf/np.mean(tiltf)))
print('Mean time to update: ', np.mean(np.diff(timef)))
print('Max time to update: ', np.max(np.diff(timef)))

# plot histogram of time taken
plt.hist(tipf, bins=10, density=True, label='Tip')
plt.hist(tiltf, bins=10, density=True, label='Tilt')
plt.xlabel('Tip / Tilt [mas]')
plt.ylabel('Normalised Number of Occurances')
plt.legend(loc=1)
plt.show()
