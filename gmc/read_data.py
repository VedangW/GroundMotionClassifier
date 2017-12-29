#!usr/bin/python

""" This is a python module to process a particular event
	by creating a SeismicEvent type
	
	Author: VedangW
"""

import pe
import rsp
import sr
import complexity

import sys
from obspy import read

def process_stream(e_file, n_file, z_file):
	# Create stream three_channel
	three_channel = read(e_file)
	three_channel += read(n_file)
	three_channel += read(z_file)

	# Get name of event 
	# eg. 20160616035350SRSUR00BHZ
	eventname = e_file.split(".")
	eventname = eventname[5:]

	# Create a SeismicEvent with the three traces
	seismic_event = SeismicEvent(three_channel, filename)
	rsp = seismic_event.rsp()
	c = seismic_event.complexity()
	sr = seismic_event.sr()
	logpe = seismic_event.pe(rsp, c, sr)

	# If seismic event is to be accepted then 
	# return the data, otherwise return nan
	acc = seismic_event.get_acceptance()
	if acc:
		data = filename + " " + logpe + " " + c
	else:
		data = filename + "nan"

	return data

""" MAIN:
	args = [file with e trace, ...]
	e_file = path of file having e trace
"""
def main(e_file, n_file, z_file):
	e_file, n_file, z_file = sys.argv[1], sys.argv[2], sys.argv[3]
	data = process_stream(e_file, n_file, z_file)
	print data