#!usr/bin/python

"""	A module to calculate the spectral ratio of the dataset.
"""
import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack as fft
from Seismogram import Seismogram

#A function to calculate the spectral ratio given the limits
def spectral_ratio(smg, limits_high, limits_low):
	numerator = smg.find_area(limits_high)
	denominator = smg.find_area(limits_low)

	sr = numerator / denominator
	return sr

#A function to find the appropriate limits and call the spectral_ratio function
def find_sr(path, file, acc_rights):
	smg = Seismogram(path, file, acc_rights)
	"""
	T = 1.0 / 50.0
	y = np.abs(fft.fft(smg.get_amplitudes()))
	x = np.arange(0., smg.get_ndat() * 0.02, 0.02)
	fig = plt.figure()
	ax0 = fig.add_subplot(211)
	ax0.plot(x, y)
	ax1 = fig.add_subplot(212)
	ax1.plot(x, smg.get_amplitudes()) 
	plt.show()
	"""
	lh = []
	ll = []
#	sr = spectral_ratio(lh, ll)
	sr = 100
	print sr

def main():
	find_sr(sys.argv[1], sys.argv[2], sys.argv[3])

if __name__ == "__main__":
	main()
