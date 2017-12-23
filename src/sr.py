#!usr/bin/python

"""	A module to calculate the spectral ratio of the dataset.

	Sampling Rate = 50
	Nyquist frequency = 25 Hz

	Author: VedangW
	status: verified
"""
import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack as fft
from time import time
from Seismogram import Seismogram

# A function to calculate the spectral ratio given the limits
def spectral_ratio(y, limits_high, limits_low, df):
	numerator = integrate(y, limits_high, df)
	denominator = integrate(y, limits_low, df)

	sr = numerator / denominator
	return sr

# A function to integrate the FFT graph within the given domains
def integrate(y, limits, df):
	x0 = int(limits[0])
	x1 = int(limits[1])
		
	integral = np.trapz(y[x0:x1], dx=df)
	return integral

# A function to find the appropriate limits and call the spectral_ratio function
def find_sr(path, file, acc_rights):
	t0 = time()
	smg = Seismogram(path, file, acc_rights)
	
	T = 1.0 / 50.0	#Sampling interval
	x = np.arange(0., smg.get_ndat() * 0.02, 0.02)

	# Calculating the FFT
	amps = smg.get_amplitudes()
	y = np.abs(fft.fft(amps))
	y = y[0:smg.get_ndat()/ 2]
	df = 50.0 / smg.get_ndat()
	f = np.arange(0., smg.get_ndat()/2) * df
	
	print "Time taken: ", time() - t0

	# Plotting the graphs
	fig = plt.figure('Signal and its Fast Fourier Transform')

	ax0 = fig.add_subplot(211)
	ax0.plot(x, smg.get_amplitudes(), label='Signal')
	ax0.set_xlabel('t (s)')
	ax0.set_ylabel('A(t) m/s')
	ax0.legend() 

	ax1 = fig.add_subplot(212)
	ax1.plot(f, y, label='FFT', color='cornflowerblue')
	ax1.set_xlabel('Frequency (Hz)')
	ax1.set_ylabel('A(f) m/s')
	ax1.legend()

	plt.show()
	
	# High and low limits are defined for integration
	lh = [1, 10]
	ll = [11, 20]
	sr = spectral_ratio(y, lh, ll, df)
	print sr

""" MAIN:
	args = [path, filename, access_rights]
"""
def main():
	find_sr(sys.argv[1], sys.argv[2], sys.argv[3])

if __name__ == "__main__":
	main()

