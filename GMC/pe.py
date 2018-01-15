#!usr/bin/python

""" Program to calculate the log of Power of Event from complexity, 
	S/P ratio and spectral ratio.

	Author: VedangW
"""
import sys
import math

def find_pe(rsp, c, sr):
	""" 
	Function to calculate log of power of event.

	Power of event is defined as pe = rsp^2 * c * sr^2.

	Parameters
	----------
	rsp: float
		S/P ratio of the event.
	c: float
		Complexity of the event.
	sr: float
		Spectral ratio of the event.

	Returns
	-------
	log_pe: float
		log10 of the power_of_event

	"""
	rsp = float(rsp)
	c = float(c)
	sr = float(sr)

	pe = (rsp ** 2) * (c) * (sr ** 2)
	log_pe =  math.log10(pe)

	return log_pe