#!usr/bin/python

"""	A module to calculate the spectral ratio of the dataset.
"""
import sys
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
	lh = []
	ll = []
#	sr = spectral_ratio(lh, ll)
	sr = 100
	print sr

def main():
	find_sr(sys.argv[1], sys.argv[2], sys.argv[3])

if __name__ == "__main__":
	main()
