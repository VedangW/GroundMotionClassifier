#!usr/bin/python

import config
import numpy as np
import matplotlib.pyplot as plt
from obspy import read
from peakutils.baseline import baseline, envelope

def main():
	ph = config.project_home
	st = read(ph + "/data/SUR_eq/20160624134017.SR.SUR.00.BHZ.sac")
	arr = st[0].data
	print ("Original data = ", arr)

	bsl = baseline(np.array(arr))
	print ("Baseline = ", bsl)

if __name__ == "__main__":
	main()