#!usr/bin/python

import rsp
import sr
import complexity
import pe

class SeismicEvent:
	def __init__(self, stream):
		self.acceptance = True
		self.e_trace = stream[0]
		self.n_trace = stream[1]
		self.z_trace = stream[2]
		self.sampling_rate = stream[0].stats.sampling_rate

	def get_acceptance(self,):
		return self.acceptance

	def get_e_trace(self,):
		return self.e_trace

	def get_n_trace(self,):
		return self.n_trace

	def get_z_trace(self,):
		return self.z_trace

	def get_sampling_rate(self,):
		return self.sampling_rate

	def plot_spectrogram(self,):
		self.spectrogram()

	def rsp(self,):
		e_p, e_s = find_ps(self.e_trace.data)
		n_p, n_s = find_ps(self.n_trace.data)
		z_p, z_s = find_ps(self.z_trace.data)

		p_wave = z_p
		if (n_s > e_s):
			s_wave = n_s
		else:
			s_wave = e_s

		try:
			rsp = s_wave / p_wave
		except ZeroDivisionError:
			rsp = "nan"
			self.acceptance = False

		return rsp

	def sr(self,):
		e_sr = find_sr(self.e_trace.data)
		n_sr = find_sr(self.n_trace.data)
		z_sr = find_sr(self.z_trace.data)

		return e_sr, n_sr, z_sr

	def complexity(self,):
		e_c = find_c(self.e_trace.data)
		n_c = find_c(self.n_trace.data)
		z_c = find_c(self.z_trace.data)

		return e_c, n_c, z_c

	def pe(self, ratio, comp, spectral):
		power_of_event = find_pe(ratio, comp, spectral)
		return power_of_event