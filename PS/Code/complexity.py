#!usr/bin/python

"""	This is a module to find the complexity of
	a particular seismogram.
"""
import os
import sys
import rsp 
from Seismogram import Seismogram

#A function to calculate the complexity given the limits
def complexity(smg, limits_high, limits_low):
	numerator = smg.find_area(limits_high)
	denominator = smg.find_area(limits_low)

	ratio = numerator / denominator
	return ratio

#A function to find the appropriate limits and call the complexity function
def find_C(path, file, acc_rights, rsp):
	smg = Seismogram(path, file, acc_rights)

	#t0 is the start of the P wave, t1 and t2 at 3 and 7 secs from it
	t0 = float(rsp)
	t1 = t0 + 3 * 50
	t2 = t0 + 7 * 50

	#Lower and higher limits
	lh = [t1, t2]
	ll = [t0, t1]

	C = complexity(smg, lh, ll)
	print C

#args = [path, filename, access rights]
def main():
	if sys.argv[4] == "N/A":
		print "N/A"
	else:
		find_C(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

if __name__ == "__main__":
	main()