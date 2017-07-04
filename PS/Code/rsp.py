#!usr/bin/python

"""	This is a python module to calculate the P/S ratio of
	the given data by STA / LTA method.
	
	SNR(Signal to Noise Ratio) = STA / LTA 
	Limiting Ratio = 3
"""
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import peakutils as pkt
from scipy.signal import hilbert
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


#Function to return position and amplitude of P Wave
def findp(smg):
	lim_ratio = 3
	STA = 0
	index = 0
	P = []
	amps = smg.get_amplitudes()
	
	#Hilbert transformation and envelope function
	analytic_function = hilbert(amps)
	envelope = np.abs(analytic_function)

	#Cascading and comparing the SNR in the wave 
	for a in amps:
		STA = sta(envelope, index)
		LTA = lta(envelope, index)

		index += 1

		if STA != False and LTA != False and STA / LTA >= lim_ratio:
			P.append(index)
			P.append(a)
			P.append(envelope)
			break

	return P

def main():
	t0 = time()

	smg = Seismogram(sys.argv[1], sys.argv[2], sys.argv[3])

	P = findp(smg)
	ndat = smg.get_ndat()

	try:
		if (P == False):
			print "P wave not found"
		else:
			print P[0]
			print P[1]

			x_coord = 0.02 * (P[0] - 1)
			y_coord = P[1]

			x = np.arange(0., ndat * 0.02, 0.02)
			envelope = P[2]

			line_y = x_coord

#			print "Time taken: ", time() - t0, " s"
			"""
			#Plotting the figure
			fig = plt.figure('P Wave Location')

			ax0 = fig.add_subplot(211)
			ax0.plot(x, envelope, label='envelope')
#			plt.plot(x_coord, y_coord, 'rx')
			ax0.axvline(x=x_coord, color='r', linestyle='dashed', label='P wave')
			ax0.set_xlabel('t')
			ax0.set_ylabel('S(t)')
			ax0.legend()

			ax1 = fig.add_subplot(212)
			ax1.plot(x, smg.get_amplitudes(), label='signal', color='c')
			ax1.axvline(x=x_coord, color='r', linestyle='dashed', label='P wave')
			ax1.set_xlabel('t')
			ax1.set_ylabel('S(t)')
			ax1.legend()

			plt.show()
			"""
	except IndexError as e:		#Index error means SNR was always < limiting ratio
		if e.message == "list index out of range":
			print "N/A"


if __name__ == "__main__":
	main()