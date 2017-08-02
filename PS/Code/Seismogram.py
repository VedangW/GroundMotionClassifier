#!usr/bin/python

"""	This is a custom made module containing the class definition 
	of an object of type 'Seismogram' which can be used to read a 
	particular file in a needed way, plot its graph and find the area.

	Author: VedangW
"""

class Seismogram:
	""" A class to play with the file. Enough said."""

	#Try 'r', 'r+', 'w', 'w+' for access_rights, 'r' is recommended.
	#Specify all three parameters in double quotes
	def __init__(self, path, filename, access_rights):
		self.path = path
		self.filename = filename
		self.access_rights = access_rights
		self.dat_num = 0
		self.amplitudelist = []
		self.eventid = ""

	#Returns number of data points
	def get_ndat(self):
		import os
		os.chdir(self.path)

		data_file = open(self.filename, self.access_rights)
		lines = data_file.readlines()
		self.dat_num = len(lines) - 5

		return self.dat_num

	#Returns list of amplitudes
	def get_amplitudes(self):
		import os
		import pandas as pd
		import peakutils as pkt

		os.chdir(self.path)

		self.amplitudelist = []
		self.amplitudelist = pd.read_csv(self.filename, skiprows=5, header=None).values

		#Baseline correction
		for a in self.amplitudelist:
			a += 10000000
		baseline = pkt.baseline(self.amplitudelist)
		self.amplitudelist = self.amplitudelist - baseline

		amps = self.amplitudelist
		flat_list = [item for sublist in amps for item in sublist]
		self.amplitudelist = flat_list

		return self.amplitudelist

	#Returns path to file
	def get_path(self):
		return self.path

	#Returns given access rightsbas
	def get_access_rights(self):
		return self.access_rights

	#Returns name of file 
	def get_filename(self):
		return self.filename

	#Returns the event id
	#Format of event id is: "st.code yy mm dd hh min sec" 
	def get_event_id(self):
		import os
		os.chdir(self.path)

		self.eventid = ""

		f = open(self.filename)
		lines = f.readlines()
		data = lines[3].split()
		stationcode = data[1]

		data = lines[0].split()
		data.pop(0)

		self.eventid += stationcode + " "
		for i in data:
			self.eventid += i + " "

		return self.eventid

	#Plots the seismogram as S(t) vs t
	def plot_graph(self):
		import numpy as np
		import matplotlib.pyplot as plt

		x_range = np.arange(0.,self.get_ndat() * 0.02, 0.02)
		y_range = np.array(self.get_amplitudes())

		plt.figure('Seismogram')
		plt.plot(x_range, y_range, linewidth = 2.0)
		plt.ylabel('S(t) m/s')
		plt.xlabel('t (s)')

	#Finda area of seismogram within given limits
	def find_squared_area(self, limits):
		import numpy as np
		from numpy import trapz

		x0 = int(limits[0])
		x1 = int(limits[1])
		amps = self.get_amplitudes()
		for i in range(len(amps)):
			amps[i] = amps[i] ** 2
		
		Area = trapz(amps[x0:x1], dx=0.02)
		
		return Area


#Just as an example for how to use it. Run the program to know.
def main():
	import sys
	import matplotlib.pyplot as plt

	if sys.argv[1] == "Kachchh":
		path = "/home/vedang/Desktop/PS/Datasets/Kachchh"
	elif sys.argv[1] == "Surendranagar":
		path = "/home/vedang/Desktop/PS/Datasets/Surendranagar"
	else:
		print "Check path again."
		return 

	fd = Seismogram(path, sys.argv[2], "r")
#	print "List of amplitudes: ", fd.get_amplitudes()
#	print "Number of data points: ", fd.get_ndat()
#	print "Filename: ", fd.get_filename()
#	print "Path to file: ", fd.get_path()
#	print "Access rights given: ", fd.get_access_rights()
	print "Event is: ", fd.get_event_id()

#	limits = [10, 575]
#	print "Area between x0 and x1: ", fd.find_area(limits)

	print "Plotting seismogram..."
	fd.plot_graph()
	plt.show()


if __name__ == "__main__":
	main()