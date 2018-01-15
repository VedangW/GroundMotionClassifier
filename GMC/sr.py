#!usr/bin/python

"""	A module to calculate the spectral ratio of the dataset.

	Sampling Rate = 50
	Nyquist frequency = 25 Hz

	Author: VedangW
"""
import sys
import config
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack as fft
import SeismicEvent
from time import time

def spectral_ratio(y, limits_high, limits_low, df):
	"""
	A function to calculate the spectral ratio given the limits.

	Parameters
	----------
	y: list
		Fast fourier transform of the amplitudes
	limits_high: list
		A list containing the lower and upper high limits
	limit_low: list
		A list containing the lower and upper low limits
	df: float
		Interval for integration.

	Returns
	-------
	sr: float
		The spectral ratio of the waveform y.

	"""
	numerator = integrate(y, limits_high, df)
	denominator = integrate(y, limits_low, df)

	sr = numerator / denominator
	return sr

def integrate(y, limits, df):
	"""
	A function to integrate the FFT within the given domains

	Parameters
	----------
	y: list
		FFT of the input curve
	limits: list
		The high and low limit indices for integration
	df: float
		The interval for integration

	Returns
	-------
	integral: float
		Value of the definite integral within the given limits

	"""

	x0 = int(limits[0])
	x1 = int(limits[1])
		
	integral = np.trapz(y[x0:x1], dx=df)
	return integral

def find_sr(event):
	""" 
	A function to find the appropriate limits and 
	call the spectral_ratio function

	Parameters
	----------
	event: SeismicEvent object
		The event whose spectral ratio we need to find

	Returns
	-------
	sr: float
		The spectral ratio of the event

	"""

	# If event is not to be accepted, then return "nan"
	if event.acceptance == False:
		return "nan"

	# amps = the list of amplitudes in the n-trace
	amps = event.n_trace
	# ndat = number of data points
	ndat = len(amps)

	T = 1.0 / 50.0	# Sampling interval
	x = np.arange(0., ndat * 0.02, 0.02)

	# Calculating the FFT
	y = np.abs(fft.fft(amps))
	y = y[0: int(ndat/ 2)]
	df = 50.0 / ndat
	f = np.arange(0., ndat/2) * df

	# High and low limits are defined for integration
	lh = config.sr_lh
	ll = config.sr_ll
	sr = spectral_ratio(y, lh, ll, df)

	# Plotting the graphs
	# fig = plt.figure('Signal and its Fast Fourier Transform')

	# ax0 = fig.add_subplot(211)
	# ax0.plot(x, smg.get_amplitudes(), label='Signal')
	# ax0.set_xlabel('t (s)')
	# ax0.set_ylabel('A(t) m/s')
	# ax0.legend() 

	# ax1 = fig.add_subplot(212)
	# ax1.plot(f, y, label='FFT', color='cornflowerblue')
	# ax1.set_xlabel('Frequency (Hz)')
	# ax1.set_ylabel('A(f) m/s')
	# ax1.legend()

	# plt.show()

	return sr