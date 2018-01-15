#!usr/bin/python

""" A module to define the SeismicEvent class

	Author: VedangW
"""

import rsp
import sr
import complexity
import pe
import peakutils as pkt
from numpy import trapz, floor


class SeismicEvent:
	""" 
	A class that defines a seismic event.

	A seismic event is seen as a combination of its z, n and e
	components, along with its id. Acceptance tells if the event
	is to be accepted or not. Sampling rate is the inverse of
	the frequency of reading of each amplitude value.

	Parameters
	----------
	stream: Obspy Stream object
		An object of the Obspy Stream class. Contains z, n and e
		traces of the event along with metadata.
	event_id: str
		The filename (without extension) of the z component of the
		event used to uniquely identify the event.
		Eg. of event_id: "20150705132156.SR.SUR.00.BHZ"

	Returns
	-------
	SeismicEvent object.
	
	"""

	def __init__(self, stream, event_id):
		""" Constructor for class. """
		self.event_id = event_id
		self.acceptance = True
		self.e_trace = stream[0].data
		self.n_trace = stream[1].data
		self.z_trace = stream[2].data
		self.sampling_rate = stream[0].stats.sampling_rate

	@property
	def event_id(self):
		""" Getter for event_id """

		return self.__event_id

	@event_id.setter
	def event_id(self, ev_id):
		""" Setter for event_id """

		self.__event_id = ev_id

	@property
	def acceptance(self):
		""" Getter for acceptance """

		return self.__acceptance

	@acceptance.setter
	def acceptance(self, val):
		""" Setter for acceptance """

		if val == True or val == False:
			self.__acceptance = val
		else:	
			raise TypeError("Value of acceptance not boolean")

	@property
	def e_trace(self):
		""" Getter for the e_trace """

		return self.__e_trace

	@e_trace.setter
	def e_trace(self, trace):
		""" Setter for the e_trace """

		# Baseline correct the amplitudes
		trace += 8400000
		bsl = pkt.baseline(trace)
		for i in range(len(trace)):
			trace[i] = trace[i] - bsl[i]
		self.__e_trace = trace

	@property
	def n_trace(self):
		""" Getter for the n_trace """

		return self.__n_trace

	@n_trace.setter
	def n_trace(self, trace):
		""" Setter for the n_trace """

		# Baseline correct the amplitudes
		trace += 8400000
		bsl = pkt.baseline(trace)
		for i in range(len(trace)):
			trace[i] = trace[i] - bsl[i]
		self.__n_trace = trace

	@property
	def z_trace(self):
		""" Getter for the z_trace """

		return self.__z_trace

	@z_trace.setter
	def z_trace(self, trace):
		""" Setter for the z_trace """

		# Baseline correct the amplitudes
		trace += 8400000
		bsl = pkt.baseline(trace)
		for i in range(len(trace)):
			trace[i] = trace[i] - bsl[i]
		self.__z_trace = trace

	@property
	def sampling_rate(self):
		""" Getter for the sampling rate """

		return self.__sampling_rate	

	@sampling_rate.setter
	def sampling_rate(self, srate):
		""" Setter for the sampling rate """

		self.__sampling_rate = srate

	## Methods

	def find_squared_area(self, tracename, limits):
		""" Finds the area under a squared curve """

		if tracename == "e":
			amps = self.e_trace[limits[0]:limits[1]]
		elif tracename == "n":
			amps = self.n_trace[limits[0]:limits[1]]
		elif tracename == "z":
			amps = self.z_trace[limits[0]:limits[1]]
		else:
			raise TypeError("Invalid value for tracename")

		amps = [i ** 2 for i in amps]
		area = trapz(amps, dx=0.02)
		return area

	def ratio_sp(self):
		""" Finds the S/P ratio of the event """

		# Phases = [p_time, p_amp, s_time, s_amp]
		phases_n = rsp.find_ps(self.n_trace.data)
		phases_z = rsp.find_ps(self.z_trace.data)

		# Take p_wave parameters from the z_trace
		p_wave_time = phases_z[0]
		p_wave_amp = phases_z[1]

		# Take s_wave parameters from the n_trace
		s_wave_time = phases_n[0]
		s_wave_amp = phases_n[1]

		# Calculate ratio of the S wave and P wave amps
		try:
			ratio = s_wave_amp / p_wave_amp
		except ZeroDivisionError:
			ratio = "nan"
			self.acceptance = False

		return ratio, p_wave_time

	def spec_ratio(self):
		""" Finds the spectral ratio of the event """

		spectral_ratio = sr.find_sr(self)
		return spectral_ratio

	def comp(self, p_time):
		""" Finds the complexity of the event """

		c = complexity.find_c(self, p_time)
		return c

	def log_pe(self, ratio, comp, spectral):
		""" Finds the log of the power of event """

		power_of_event = pe.find_pe(ratio, comp, spectral)
		return power_of_event