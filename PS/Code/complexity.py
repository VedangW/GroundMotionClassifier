#!usr/bin/python

"""	This is a module to find the complexity of
	a particular seismogram.

	Author: VedangW
"""
import os
import sys
import rsp 
from time import time
from Seismogram import Seismogram

""" A function to calculate the complexity of the waveform.

	The complexity of a waveform is defined as the ratio of the 
	integrated square amplitudes over pre-defined periods of time.

	The integrals are calculated as the area between the squared function
	and the x-axis. The method for calculating this is available in
	the class Seismogram.

	### args: 
	# smg: A Seismogram object made in find_C()
	# limits_high: 	A list containing the values of t1 and t2, which
					are the limits of the integral in the numerator.
	# limits_low:	A list containing the values of t0 and t1, which
					are the limits of the integral in the denominator.

	### return:
	The function returns the complexity as a float type.
"""
def complexity(smg, limits_high, limits_low):
	numerator = smg.find_squared_area(limits_high)
	denominator = smg.find_squared_area(limits_low)

	ratio = numerator / denominator
	return ratio


""" A function to find the appropriate limits and call the complexity function.

	The limits are taken according to deduction based on the average distances
	of the stations from the epicenter.

	t0 is this taken as the start of the P Wave, t1 and t2 are 3 and 7 secs from it.

	### args:
	# path: Path of the file containing the seismogram data in ASCII format.
	# file: Name of the file.
	# acc_rights: Access rights to the file.
		Can be 'r', 'w', 'r+', 'w+' and so on.
		Typically, 'r' is given as the access rights.

	### return:
	void.
	The function prints the complexity.
"""
def find_C(path, file, acc_rights, rsp):
	t = time()
	smg = Seismogram(path, file, acc_rights)

	t0 = float(rsp)
	t1 = t0 + 3 * 50
	t2 = t0 + 7 * 50

	lh = [t1, t2]
	ll = [t0, t1]

	C = complexity(smg, lh, ll)
#	print "Time taken: ", time() - t
	print C


"""	MAIN:
	args = [path, filename, access rights]

	#Note:
	If S/P ratio is not calculated, then complexity is also not calculated.
"""
def main():
	if sys.argv[4] == "N/A":
		print "N/A"
	else:
		find_C(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

if __name__ == "__main__":
	main()