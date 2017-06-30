#!usr/bin/python

"""	This is a custom made module containing the class definition 
	of an object of type 'Seismogram' which can be used to read a 
	particular file in a needed way, plot its graph and find the area.
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
		self.stationcode = ""

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
		os.chdir(self.path)

		self.amplitudelist = []
		with open(self.filename) as f:
			lines = f.readlines()
			for ln in lines[5:self.get_ndat() + 5]:
				data = ln.split()
				self.amplitudelist.append(int(data[0]))
		
		return self.amplitudelist

	#Returns path to file
	def get_path(self):
		return self.path

	#Returns given access rights
	def get_access_rights(self):
		return self.access_rights

	#Returns name of file 
	def get_filename(self):
		return self.filename

	#Returns the station code
	def get_stationcode(self):
		import os
		os.chdir(self.path)

		f = open(self.filename)
		lines = f.readlines()
		data = lines[3].split()
		self.stationcode = data[1]

		return self.stationcode

	#Plots the seismogram as S(t) vs t
	def plot_graph(self):
		import numpy as np
		import matplotlib.pyplot as plt

		x_range = np.arange(0.,self.get_ndat() * 0.02, 0.02)
		y_range = np.array(self.get_amplitudes())

		plt.figure('Seismogram')
		plt.plot(x_range, y_range, linewidth = 2.0)
		plt.ylabel('S(t)')
		plt.xlabel('t')

	#Finda area of seismogram within given limits
	def find_area(self, limits):
		import numpy as np
		from numpy import trapz

		x0 = limits[0]
		x1 = limits[1]
		amps = self.get_amplitudes()
		
		y_range = np.array(amps[x0:x1])
		Area = trapz(y_range, dx = 0.02)

		return Area


#Just as an example for how to use it. Run the program to know.
def main():
	import matplotlib.pyplot as plt

	fd = Seismogram("/home/vedang/Desktop/PS/Datasets/Kachchh", "pitsa001.048", "r")
#	print "List of amplitudes: ", fd.get_amplitudes()
#	print "Number of data points: ", fd.get_ndat()
#	print "Filename: ", fd.get_filename()
#	print "Path to file: ", fd.get_path()
#	print "Access rights given: ", fd.get_access_rights()
	print "Station code is: ", fd.get_stationcode()

#	limits = [10, 575]
#	print "Area between x0 and x1: ", fd.find_area(limits)

#	print "Plotting seismogram..."
	fd.plot_graph()
	plt.show()

if __name__ == "__main__":
	main()