#!usr/bin/python

"""	This is a python module to calculate the P/S ratio of
	the given data by STA / LTA method.
	
	SNR(Signal to Noise Ratio) = STA / LTA 
	Limiting Ratio = 3

	Author: VedangW
"""
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import peakutils as pkt
from scipy.signal import hilbert, lfilter, butter
from time import time
from Seismogram import Seismogram

#Function to calculate Long-term average of the data
def lta(amps, pos):
	ndat = len(amps)
	if pos - 500 >= 0:
		list_splice = amps[pos - 500: pos]
	else:
		return False

	mean = sum(list_splice) / 500
	return mean	

#Function to calculate Short-term average of the data
def sta(amps, pos):
	ndat = len(amps)
	if pos - 500 >= 0:
		list_splice = amps[pos - 50: pos]
	else:
		return False

	mean = sum(list_splice) / 50
	return mean	


#Function to return envelope function and SNR vector
def find_snr(smg, amps):
	P = []
	index = 0
	
	#Hilbert transformation and envelope function
	analytic_function = hilbert(amps)
	envelope = np.abs(analytic_function)
	P.append(envelope)

	#Returning the SNR vector
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

#Function to design the Butterworth Bandpass
def butter_bandpass(lowcut, highcut, fs, order=2):
	nyq = 0.5 * fs
	low = lowcut / nyq
	high = highcut / nyq
	b, a = butter(order, [low, high], btype='band')
	return b, a

#Function to apply the Butterworth filter to the Seismogram
def butter_filter(data, lowcut, highcut, fs, order=2):
	b, a = butter_bandpass(lowcut, highcut, fs, order)
	y = lfilter(b, a, data)
	return y

#Function to return the time of P wave detection
def find_phase_times(snr):
	p_lim_ratio = 2.5
	s_lim_ratio = 3.58

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

#Function to apply the Hanning filter to the SNR vector
def smooth(x, window_len=11, window='hanning'):
    s = np.r_[x[window_len-1:0:-1],x,x[-2:-window_len-1:-1]]
    #print(len(s))
    if window == 'flat': #moving average
        w = np.ones(window_len,'d')
    else:
        w = eval('np.'+window+'(window_len)')

    y = np.convolve(w/w.sum(),s,mode='valid')
    return y

#Function to actually calculate the locations of the P wave
#by applying filters and plotting the graphs
def find_rsp(path, file, acc_rights):
	t0 = time()

	#Storing and filtering the list of amplitudes
	smg = Seismogram(path, file, acc_rights)
	data = smg.get_amplitudes()
	amps = butter_filter(data, 1, 10, 50, 2)

	#Storing the envelope function
	P = find_snr(smg, amps)
	envelope = P[0]

	#Storing and filtering the SNR vector
	snr = P[1]
	snr = smooth(snr, 11, 'hanning').tolist()
	for a in range(len(snr) - smg.get_ndat()):
		snr.pop()

	ndat = smg.get_ndat()
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
		rsp = "N/A"

	try:
		if (P == False):
			print "P wave not found"
		else:
			px_coord = 0.02 * ptime
			sx_coord = 0.02 * stime
			x = np.arange(0., ndat * 0.02, 0.02)
			"""
			print "Time taken: ", time() - t0, " s"

			#Plotting the graphs
			fig = plt.figure('P Wave Location')

			#Dataset with Butterworth filter
			ax0 = fig.add_subplot(311)
			ax0.plot(x, amps, label='signal', color='cornflowerblue')
			ax0.axvline(x=px_coord, color='r', linestyle='dashed', label='P wave')
			ax0.axvline(x=sx_coord, color='k', linestyle='dashed', label='S wave')
			ax0.set_xlabel('t (s)')
			ax0.set_ylabel('S(t) m/s')
			ax0.legend()

			#Envelope function
			ax1 = fig.add_subplot(312)
			ax1.plot(x, envelope, label='envelope')
			ax1.axvline(x=px_coord, color='r', linestyle='dashed', label='P wave')
			ax1.axvline(x=sx_coord, color='k', linestyle='dashed', label='S wave')
			ax1.set_xlabel('t (s)')
			ax1.set_ylabel('S(t) m/s')
			ax1.legend()

			#SNR with Hanning filter
			ax2 = fig.add_subplot(313)
			ax2.plot(x, snr, label='STA/LTA', color='g')
			ax2.axvline(x=px_coord, color='r', linestyle='dashed', label='P wave')
			ax2.axvline(x=sx_coord, color='k', linestyle='dashed', label='S wave')
			ax2.set_xlabel('t (s)')
			ax2.set_ylabel('SNR')
			ax2.legend()


			plt.show()
			"""
			print rsp

	except IndexError as e:		#Index error means SNR was always < limiting ratio
		if e.message == "list index out of range":
			print "N/A"

			return False

def main():
	find_rsp(sys.argv[1], sys.argv[2], sys.argv[3])

if __name__ == "__main__":
	main()