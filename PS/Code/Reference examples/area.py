#!usr/bin/python

"""	Module for calculating the area beneath a curve
	which will be used in calculating the Spectral Ratio
	and the Complexity
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from numpy import trapz
import scipy
from scipy.integrate import simps
from time import time

def findArea(amplitudes, limits):
	x0 = limits[0]
	x1 = limits[1]

	area = 0
	for i in range(x0, x1):
		area = area + 0.02 * amplitudes[i]
	return area

def main():
	os.chdir("/home/vedang/Desktop/PS/Datasets")

	data_file = open("sample.txt", "r")
	position = data_file.seek(62, 0)
	ndat = data_file.read(2)
	ndat = int(ndat)

	amplitudes = []

	#Read the amplitudes and put them in a list
	i = 114	#This is fixed
	seek_limit = 113 + 13*ndat

	while (i <= seek_limit):
		position = data_file.seek(i, 0)
		dat = data_file.read(5)
		dat = int(dat) + 10000
		amplitudes.append(dat)
		i = i + 13

#	print amplitudes

	x_range = np.arange(0.,ndat * 0.02, 0.02)
	y_range = np.array(amplitudes)	
	limits = [0, 42]	

	Area = findArea(amplitudes, limits)
	print "Area under curve by findArea: ", Area

	t0 = time()
	Area = trapz(y_range, dx = 0.02)
	print "Area under curve by trapz: ", Area
	print "Time taken: ", time() - t0, " s"

	print '\n'

	t1 = time()
	Area = simps(y_range, dx = 0.02)
	print "Area under curve by simps: ", Area
	print "Time taken: ", time() - t1, " s" 

	plt.plot(x_range, y_range, linewidth = 2.0)
	plt.show()

if __name__ == "__main__":
	main()
