#!usr/bin/python

"""	This is a module to find the complexity of
	a particular seismogram.

	Author: VedangW
"""
import os
import sys
import rsp
import config
import SeismicEvent
from time import time

def complexity(event, limits_high, limits_low):
	""" 
	A function to calculate the complexity of the waveform.

	The complexity of a waveform is defined as the ratio of the 
	integrated square amplitudes over pre-defined periods of time.
	The integrals are calculated as the area between the squared function
	and the x-axis. The method for calculating this is available in
	the class Seismogram.

	Parameters
	----------
	event: SeismicEvent object
		Passed from find_c
	limits_high: list
		A list containing the values of t1 and t2, which
		are the limits of the integral in the numerator.
	limits_low: list
		A list containing the values of t0 and t1, which
		are the limits of the integral in the denominator.

	Returns
	-------
	ratio: float
		The complexity of the event
"""
	numerator = event.find_squared_area("n", limits_high)
	denominator = event.find_squared_area("n", limits_low)

	ratio = numerator / denominator
	return ratio

def get_station(eid):
	l = eid.split(".")
	return l[2]

def find_c(event, p_time):
	""" 
	A function to find the appropriate limits and call the complexity function.

	The limits are taken according to deduction based on the average distances
	of the stations from the epicenter.t0 is this taken as the start 
	of the P Wave, t1 and t2 are 3 and 7 secs from it.

	Parameters
	----------
	event: SeismicEvent object
		Passed to function from outside the module.
	p_time: int
		Index on the time axis which denotes the onset
		of the P wave.

	Returns
	-------
	c: float
		The complexity of the event.

	"""
	t0 = p_time
	stat = get_station(event.event_id)

	# High and low values from config
	if stat == 'KAV' or stat == 'BEL' or stat == 'BHI' or stat == 'BAN' or stat == 'BDR':
		low_val = config.cl_kachchh
		high_val = config.ch_kachchh
	elif stat == 'SUR':
		low_val = config.cl_sur
		high_val = config.ch_sur
		
	# low_val = config.comp_lv
	# high_val = config.comp_hv

	# Calculate high and low limits
	t1 = t0 + low_val * 50
	t2 = t0 + high_val * 50

	lh = [t1, t2]
	ll = [t0, t1]

	c = complexity(event, lh, ll)
	return c