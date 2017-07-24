#!usr/bin/python

""" Program to calculate the log of Power of Event from complexity, 
	S/P ratio and spectral ratio.
"""
import sys
import math

#Function to calculate the log of Pe
def find_pe(rsp, c, sr):
	rsp = float(rsp)
	c = float(c)
	sr = float(sr)

	pe = (rsp ** 2) * (c) * (sr ** 2)
	log_pe =  math.log10(pe)

	print log_pe
	return log_pe

#argv = [rsp, c, sr]
def main():
	if sys.argv[1] == "N/A" or sys.argv[2] == "N/A" or sys.argv[3] == "N/A":
		print "N/A"
	else:
		find_pe(sys.argv[1], sys.argv[2], sys.argv[3])

if __name__ == "__main__":
	main()


