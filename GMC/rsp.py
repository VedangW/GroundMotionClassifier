#!usr/bin/python

"""	This is a python module to calculate the P/S ratio of
	the given data by STA / LTA method.
	
	SNR(Signal to Noise Ratio) = STA / LTA 
	Limiting Ratios are defined in config

	Author: VedangW
"""
import os
import sys
import config
import numpy as np
import matplotlib.pyplot as plt
import peakutils as pkt
from scipy.signal import hilbert, lfilter, butter
from time import time

def lta(amps, pos):
	""" 
	Function to calculate Long-term average of the data.

	Long-term Average (LTA):
	The arithmetic mean of the amplitude readings over a 
	relatively larger period. This large period for this particular
	implementation is taken as 500 consecutive readings,
	or 500 * 0.02 = 10 secs.
	The start of these readings is 10 secs (500 readings) from the
	beginning of the seismogram's time-frame.

	Parameters
	----------
	amps: list
		List of amplitudes.
	pos: int 
		Current position in the list.

	Returns
	-------
	mean: float
		The arithmetic mean. 
	"""

	ndat = len(amps)
	if pos - 500 >= 0:
		list_splice = amps[pos - 500: pos]
	else:
		return False

	mean = sum(list_splice) / 500
	return mean	

def sta(amps, pos):
	""" 
	Function to calculate Short-term average of the data.

	Short-term Average (LTA):
	The arithmetic mean of the amplitude readings over a 
	relatively smaller period. This small period for this particular
	implementation is taken as 50 consecutive readings,
	or 50 * 0.02 = 1 sec.
	The start of these readings is 10 sec (500 readings) from the
	beginning of the seismogram's time-frame.

	Parameters
	----------
	amps: list
		List of amplitudes.
	pos: int 
		Current position in the list.

	Returns
	-------
	mean: float
		The arithmetic mean.
	"""

	ndat = len(amps)
	if pos - 500 >= 0:
		list_splice = amps[pos - 50: pos]
	else:
		return False

	mean = sum(list_splice) / 50
	return mean	

def find_snr(amps):
	""" 
	Function to return envelope function and SNR vector.

	# Envelope function:
	The envelope function is a function whose graph roughly encapsulates
	the S(t) curve. This is achieved by first obtaining the Hilbert 
	Transform of the seismogram curve (F(t)) as H(t).
	The function A(t) = F(t) + j.H(t) is analytic in the complex plane
	in the needed region, and the modulus of this, |A(t)|, gives us
	the envelope function, say E(t). The STA / LTA filter is then
	applied over this function E(t).
	# Signal To Noise Ratio (SNR):
	The ratio of STA to LTA is called SNR for pre-determined earthquakes.
	Here it is more casually used to denote the STA / LTA for all
	ground motion waveforms.

	Parameters
	----------
	amps: list 
		List of amplitudes.

	Returns
	-------
	P: list
		A python list P containing the envelope function and the SNR.
	"""

	P = []
	index = 0
	
	# Hilbert transformation and envelope function
	analytic_function = hilbert(amps)
	envelope = np.abs(analytic_function)
	P.append(envelope)

	# Returning the SNR vector
	array = []
	for a in amps:
		STA = sta(envelope, index)
		LTA = lta(envelope, index)
		if STA != False and LTA != False:
			SNR = STA / LTA
			array.append(SNR)
		else:
			array.append(0)

		index += 1

	P.append(array)
	return P

def butter_bandpass(lowcut, highcut, fs, order=2):
	""" 
	Function to design the Butterworth Bandpass.

	Butterworth filter: 
	The Butterworth filter is a type of signal processing filter designed
	to have as flat a frequency response as possible in the passband. 
	It is also referred to as a maximally flat magnitude filter.

	Parameters
	----------
	lowcut: 
	highcut:
	fs:
	order: int
		= 2

	Returns
	-------
	b, a: float	
		A designed bandpass as two variables.
"""
	nyq = 0.5 * fs
	low = lowcut / nyq
	high = highcut / nyq
	b, a = butter(order, [low, high], btype='band')
	return b, a

def butter_filter(data, lowcut, highcut, fs, order=2):
	""" 
	Function to apply the Butterworth filter to the Seismogram.
	This function applies the filter to the data already present
	in the Seismogram object.

	Parameters
	----------
	data: list
		The list of amplitudes.
	lowcut:
	highcut:
	fs:
	order:

	Returns
	-------
	y: list
		A modified list containing the values after applying the
		Butterworth Filter.

	"""

	b, a = butter_bandpass(lowcut, highcut, fs, order)
	y = lfilter(b, a, data)
	return y

def find_phase_times(snr):
	"""	
	Function to return the times of P and S wave detection.

	p_time: Time at which the P Wave is found.	
	s_time: Time at which the S Wave is found.	
	p_found: If P Wave is found or not.			
	s_found: If S Wave is found or not.		
	# Limiting Ratios:
	p_lim_ratio: The first point at which the SNR function
			goes above this is named the P Wave.
	s_lim_ratio: The first point at which the SNR function
			goes above this after detecting P Wave is called 
			the S Wave.

	Parameters
	----------
	snr: list 
		The list containing the values of STA / LTA after
		every 0.02 secs.

	Returns
	-------
	phases: list
		[p_time, s_time, p_found, s_found]

	"""
	p_lim_ratio = config.p_lim_ratio
	s_lim_ratio = config.s_lim_ratio

	phases = []
	p_found = False
	s_found = False

	for i in snr:
		if i >= p_lim_ratio:
			p_time = snr.index(i)
			phases.append(p_time)
			p_found = True
			break

	if p_found:
		for i in range(p_time, len(snr)):
			if snr[i] >= s_lim_ratio:
				s_time = i
				phases.append(s_time)
				s_found = True
				break

	if p_found == False:
		return False
	else:
		phases.append(p_found)
		phases.append(s_found)

	return phases

def smooth(x, window_len=11, window='hanning'):
	""" 
	Function to apply the Hanning filter to the SNR vector.

	Hanning Filter:
	The Hann function is typically used as a window function in 
	digital signal processing to select a subset of a 
	series of samples in order to perform a Fourier transform 
	or other calculations. The advantage of the Hann window is 
	very low aliasing, and the tradeoff slightly is a decreased 
	resolution (widening of the main lobe).

	Parameters
	----------
	x: list
		The data to be Hanned.
	window_len: int
		The number of values to be taken into the window at a time.
	window: str 
		Type of window. In this case, 'hanning'.

	Returns
	-------
	y: list
		A Hanned version of the input data.

	"""
	s = np.r_[x[window_len-1:0:-1],x,x[-2:-window_len-1:-1]]
	if window == 'flat': #moving average
		w = np.ones(window_len,'d')
	else:
		w = eval('np.'+window+'(window_len)')

	y = np.convolve(w/w.sum(),s,mode='valid')
	return y

def find_ps(data):
	""" 
	Function to actually calculate the locations of the P wave
	by applying filters and plotting the graphs

	Parameters
	----------
	data: list
		Data to process

	Returns
	-------
	phases_P_S: list
		A list consisting of:[ptime, p_amp, stime, s_amp]
		where
		ptime is the onset time of the P wave
		p_amp is the amplitude of the P wave at ptime
		stime is the onset time of the S wave
		s_amp is the amplitude of the S wave
	
	"""

	amps = butter_filter(data, 1, 10, 50, 2)

	# Storing the envelope function
	P = find_snr(amps)
	envelope = P[0]

	# Storing and filtering the SNR vector
	snr = P[1]
	snr = smooth(snr, 11, 'hanning').tolist()
	for a in range(len(snr) - len(data)):
		snr.pop()

	ndat = len(data)
	phases = find_phase_times(snr)
	
	if phases == False:
		ptime = False
		stime = False
		p_found = False
		s_found = False
	elif len(phases) == 3:
		ptime = phases[0]
		stime = False
		p_found = phases[1]
		s_found = phases[2]
	else:
		ptime = phases[0]
		stime = phases[1]
		p_found = phases[2]
		s_found = phases[3]

	if p_found == True and s_found == True:
		p_amp = snr[ptime]
		s_amp = snr[stime]
		rsp = p_amp / s_amp
	else:
		return "nan"

	try:
		if (P == False):
			return ("nan")
		else:
			px_coord = 0.02 * ptime
			sx_coord = 0.02 * stime
			x = np.arange(0., ndat * 0.02, 0.02)
			
			# print "Time taken: ", time() - t0, " s"
			
			# Plotting the graphs
			# fig = plt.figure('P Wave Location')

			# # Dataset with Butterworth filter
			# ax0 = fig.add_subplot(311)
			# ax0.plot(x, amps, label='signal', color='cornflowerblue')
			# ax0.axvline(x=px_coord, color='r', linestyle='dashed', label='P wave')
			# ax0.axvline(x=sx_coord, color='k', linestyle='dashed', label='S wave')
			# ax0.set_xlabel('t (s)')
			# ax0.set_ylabel('S(t) m/s')
			# ax0.legend()

			# # Envelope function
			# ax1 = fig.add_subplot(312)
			# ax1.plot(x, envelope, label='envelope')
			# ax1.axvline(x=px_coord, color='r', linestyle='dashed', label='P wave')
			# ax1.axvline(x=sx_coord, color='k', linestyle='dashed', label='S wave')
			# ax1.set_xlabel('t (s)')
			# ax1.set_ylabel('S(t) m/s')
			# ax1.legend()

			# # SNR with Hanning filter
			# ax2 = fig.add_subplot(313)
			# ax2.plot(x, snr, label='STA/LTA', color='g')
			# ax2.axvline(x=px_coord, color='r', linestyle='dashed', label='P wave')
			# ax2.axvline(x=sx_coord, color='k', linestyle='dashed', label='S wave')
			# ax2.set_xlabel('t (s)')
			# ax2.set_ylabel('SNR')
			# ax2.legend()

			# plt.show()

			phases_P_S = [ptime, p_amp, stime, s_amp]
			
			return phases_P_S

	except IndexError as e:		# Index error means SNR was always < limiting ratio
		print (e.message)