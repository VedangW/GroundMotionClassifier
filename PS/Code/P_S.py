#!usr/bin/python

"""	This is a python module to calculate the P/S ratio of
	the given data by STA / LTA method. 
	Limiting Ratio = 1
"""
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from time import time
from Seismogram import Seismogram

#Function to calculate Long-term average of the data
def lta(smg, pos):
	amps = smg.get_amplitudes()
	ndat = smg.get_ndat()
	if (pos + 500 < ndat):
		list_splice = amps[pos:pos + 500]
#		print list_splice
	else:
		return False

	mean = sum(list_splice) / 500
	return mean	

def sta(smg, pos):
	amps = smg.get_amplitudes()
	ndat = smg.get_ndat()
	if (pos + 50 < ndat):
		list_splice = amps[pos:pos + 50]
#		print list_splice
	else:
		return False

	mean = sum(list_splice) / 50
	return mean	


#Function to return position and amplitude of P Wave
def findp(smg):
	lim_ratio = 1
	STA = 0
	pre = 0
	P = []
	amps = smg.get_amplitudes()

	for a in amps:
		STA = sta(smg, pre)
		LTA = lta(smg, pre)

		pre = pre + 1

		if STA != False and LTA != False and STA / LTA >= lim_ratio:
			P.append(pre)
			P.append(a)
			break

	return P

def main():
	t0 = time()

	smg = Seismogram(sys.argv[1], sys.argv[2], sys.argv[3])

	P = findp(smg)

	if (P == False):
		print "P wave not found"
	else:
		print P[0]
		print P[1]

		x_coord = 0.02 * (P[0] - 1)
		y_coord = P[1]

#		print "Time taken: ", time() - t0, " s"

"""		smg.plot_graph()
		plt.plot(x_coord, y_coord, 'rx')
		plt.show()
"""
if __name__ == "__main__":
	main()