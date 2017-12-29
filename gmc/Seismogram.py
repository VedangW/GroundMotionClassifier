#!usr/bin/python

"""	This is a custom made module containing the class definition 
	of an object of type 'Seismogram' which can be used to read a 
	particular file in a needed way, plot its graph and find the area.

	Author: VedangW
	Status: verified
"""

import os
import sys
import numpy as np
import peakutils as pkt
import pandas as pd
import matplotlib.pyplot as plt


class Seismogram:
	""" A class to play with the file. Enough said.
		It maps the data available in a text file with ASCII format to a list of 
		amplitudes with appropriate attributes for later data retrieval.
		

		### Attributes:
		Any instance of the class Seismogram has the following attributes:

		# path: Path to the file with the data.
				For eg. "~/Desktop/isrsvm/Datasets/Kachchh"

		# filename: Name of the file. Eg. "pitsa001.003"

		# access_rights: Access rights to the file, i.e. what the user can do
				with the file. For eg. "r" means "Read-only", "w" means "Write"
				and so on. Consistent with the Python 2 File IO specifications
				of access rights to a file. Try 'r', 'r+', 'w', 'w+' 
				for access_rights, 'r' is recommended.

		# dat_num: Number of data points in the file.

		# amplitudelist: The list containing the values of amplitudes in the 
				file, each at a time difference of 0.02 secs from the previous entry.

		# event_id: The event_id is like a key that will uniquely identify the
				event. See get_event_id() for more information.


		### Methods:
		Apart from the getter methods, there are methods to calculate the area
		under the squared curve, and plot the amplitude vs time graph. 
	"""
	def __init__(self, path, filename, access_rights):
		self.path = path
		self.filename = filename
		self.access_rights = access_rights
		self.dat_num = 0
		self.amplitudelist = []
		self.eventid = ""


	""" Getter method for number of data points.

		### args:
		self.

		### returns:
		The number of data points as an int type.
	"""
	def get_ndat(self):
		import os

		os.chdir(self.path)

		data_file = open(self.filename, self.access_rights)
		lines = data_file.readlines()
		self.dat_num = len(lines) - 5

		data_file.close()

		return self.dat_num


	""" Getter method for list of amplitudes.

	 	### Baseline Correction: 
	 	The baseline is a curve that joins the bases of any pulses in the graph.
		Baseline correction is a way of "flattening" the waveform by subtracting
		the baseline curve from the amplitude curve.

		Baseline correction is important in finding the S/P ratio. 

		### args:
		self.

		### returns:
		A python list containing the amplitudes with a time difference of 0.02 secs.
	"""
	def get_amplitudes(self):
		import os
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


	""" Getter method for path.

		### args:
		self.

		### returns:
		The path as a string.
	"""
	def get_path(self):
		return self.path


	""" Getter method for access rights.

		### args:
		self.

		### returns:
		The access rights as a string.
	"""
	def get_access_rights(self):
		return self.access_rights


	""" Getter method for name of the file.

		### args: 
		self.

		### returns:
		The name of the file as a string.
	""" 
	def get_filename(self):
		return self.filename


	""" Returns the event id
		##Format of event id is: "st.code yy mm dd hh min sec"
		sec is a float type.

		The timestamp and station code create a composite key for the
		event since it is unikely that two events are recorded at the 
		same time and place with exactly same timestamps.

		### args:
		self.

		### returns:
		A string, 'eventid'.
	""" 
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

		f.close()

		return self.eventid


	""" This function plots the Seismogram, i.e., the function S(t) vs t.
		This can be used to view the overall plot and get an idea of the
		nature of the event. 

		This cannot be used in feature calculations as the plot is explicitly
		shown, not given as a return value.

		### args:
		self.

		### return:
		void.
		Outputs a matplotlib.pyplot graph object.
	"""
	def plot_graph(self):
		import numpy as np
		import matplotlib.pyplot as plt

		x_range = np.arange(0.,self.get_ndat() * 0.02, 0.02)
		y_range = np.array(self.get_amplitudes())

		plt.figure('Seismogram')
		plt.plot(x_range, y_range, linewidth = 2.0)
		plt.ylabel('S(t) m/s')
		plt.xlabel('t (s)')


	""" This function finds the area between the squared value of the
		function S(t) and t. This can be used extensively in finding the 
		complexity of the waveform. This is actually the definite integral
		for S^2(t)dt between appropriate limits.

		### Trapezoidal method for calculating area:
		The total area is calculated as the sum of areas of thin trapeziums of
		width dx (dx = 0.02 secs or 1 unit on the x axis in this case). The parallel
		sides of this thin trapezium are the two adjacent values in the list, or
		the amplitude values before and after dx time, y1 and y2.

		So, area of trapezium, dA = 0.5 * (y1 + y2) * dx.
		And total area = sum(dA) over the curve from x0 to x1.

		This is implemented using a numpy function.

		### args:
		self, limits.
		# limits: A list containing the higher and lower limit of the definite
				integral as [x0, x1].
				x0 and x1 are the x0th and x1th instances, and not time in secs.

		### returns:
		The area as a float.
	"""
	def find_squared_area(self, limits):
		import numpy as np
		from numpy import trapz

		x0 = int(limits[0])
		x1 = int(limits[1])
		amps = self.get_amplitudes()
		for i in range(len(amps)):
			amps[i] = amps[i] ** 2
		
		Area = np.trapz(amps[x0:x1], dx=0.02)
		
		return Area
		

""" MAIN:
	### args: 
	# path: Enter only "Kachchh" or "Surendranagar" for now.
	# filename: Name of file.

	Access rights are 'r' by default. 

	Just as an example for how to use it. Run the program to know.
"""
def main():
	import sys
	import matplotlib.pyplot as plt

	if sys.argv[1] == "Kachchh":
		path = "/home/vedang/Desktop/isr_project/data/Kachchh"
	elif sys.argv[1] == "Surendranagar":
		path = "/home/vedang/Desktop/isr_project/data/Surendranagar"
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
#	print ("Area between x0 and x1: ", fd.find_area(limits)

	print "Plotting seismogram..."
	fd.plot_graph()
	plt.show()


if __name__ == "__main__":
	main()