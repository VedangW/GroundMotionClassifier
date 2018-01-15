import config
import unittest
import math
import peakutils as pkt
import sys
sys.path.append('/home/vedang/Desktop/gmc/GMC')

from numpy import trapz
from obspy import read
from SeismicEvent import SeismicEvent

class TestSeismicEvent(unittest.TestCase):

	# Set up for tests

	def setUp(self):
		self.stream = self.set_stream()
		self.event = SeismicEvent(self.stream, "20150705132156.SR.SUR.00.BHZ")

	def set_stream(self):
		pof = config.project_home + "/data/SUR_eq/20150705132156.SR.SUR.00.BH"
		z_path = pof + "Z.sac"
		n_path = pof + "N.sac"
		e_path = pof + "E.sac"

		stream = read(e_path)
		stream += read(n_path)
		stream += read(z_path)

		return stream

	def process(self, trace):
		trace += 8400000
		bsl = pkt.baseline(trace)
		for i in range(len(trace)):
			trace[i] = trace[i] - bsl[i]
		return trace

	def get_rsp(self):
		ratio = self.event.ratio_sp()
		print (ratio)

	def test_sampling_rate(self):
		self.assertEqual(self.event.sampling_rate, 50.0)

	def test_get_traces(self):
		self.assertEqual(self.event.e_trace.all(), self.process(self.stream[0].data).all())
		self.assertEqual(self.event.n_trace.all(), self.process(self.stream[1].data).all())
		self.assertEqual(self.event.z_trace.all(), self.process(self.stream[2].data).all())

	def test_acceptance(self):
		self.assertEqual(self.event.acceptance, True)
		self.event.acceptance = False
		self.assertEqual(self.event.acceptance, False)

	def test_event_id(self):
		self.assertEqual(self.event.event_id, "20150705132156.SR.SUR.00.BHZ")

	def test_pe(self):
		self.assertEqual(self.event.log_pe(10, 5, 2), math.log10(2000))	

if __name__ == "__main__":
	unittest.main()