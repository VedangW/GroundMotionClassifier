import config
import unittest
import math
import sys
sys.path.append('/home/vedang/Desktop/gmc/GMC')

from obspy import read
from SeismicEvent import SeismicEvent

def setup():
	pof = config.project_home + "/data/SUR_eq/20150705132156.SR.SUR.00.BH"
	z_path = pof + "Z.sac"
	n_path = pof + "N.sac"
	e_path = pof + "E.sac"

	stream = read(e_path)
	stream += read(n_path)
	stream += read(z_path)

	event = SeismicEvent(stream, "20150705132156.SR.SUR.00.BHZ")
	return event

def get_rsp(event):
	return event.ratio_sp()

def get_comp(event, ptime):
	return event.comp(ptime)

def get_sr(event):
	return event.spec_ratio()

def main():
	event = setup()

	ratio, ptime = get_rsp(event)
	c = get_comp(event, ptime)
	sr = get_sr(event)

	print ("Ratio of S by P = ", ratio)
	print ("Complexity = ", c)
	print ("Spectral ratio = ", sr)

if __name__ == "__main__":
	main()