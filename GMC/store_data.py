#!usr/bin/python

""" A module to preprocess and store all data related to each
	event read by read_event.py into a file 'store.txt'

	Author: VedangW
"""

import os
import config
import pickle
from SeismicEvent import SeismicEvent

def store_in_file(data_home):
	""" 
	Function to preprocess and store each instance in a file

	This function first loads the events and labels from
	their respective pickled files. It then creates / wipes
	the file 'store.txt' in gmc/data/ clean. Each event is then
	preprocessed and its label retrieved. These are then
	written back to 'store.txt'.
	
	parameters
	----------
	data_home: str
		Path to the data folder
	
	Returns
	-------
	count: int
		Number of files skipped
	init_size: int
		Number of files initially

	"""
	print ("Loading stored events and labels...")

	# Load all_events from pickled file
	events_in = open(data_home + "events.pkl", "rb")
	list_of_events = pickle.load(events_in)
	events_in.close()

	# Load all_labels from pickled file
	labels_in = open(data_home + "labels.pkl", "rb")
	labels = pickle.load(labels_in)
	labels_in.close()

	# Wipe all contents of the file
	open(data_home + "store.txt", "w").close()

	# Assert that no. of events = no. of labels
	try:
		assert len(list_of_events) == len(labels)
	except AssertionError:
		# If not, terminate the program
		print ("Number of events and labels are different.")
		print ("Check again.")
		return 

	# Get initial size of the list_of_events
	init_size = len(list_of_events)

	print ("Writing to store...", "\n")

	# Open file store.txt for appending
	store = open(data_home + "store.txt", "a")
	# Count is the number of events which were skipped.
	count = 0

	# For each element in list_of_events and labels,
	# 1) Calculate rsp, comp, sr, logpe in that order
	# 2) Convert them all to string and concatenate them and
	# 3) Write to file store.txt

	for i in range(len(list_of_events)):
		try:
			event_id = list_of_events[i].event_id
			print ("Writing ", event_id)
			rsp, ptime = list_of_events[i].ratio_sp()
			complexity = list_of_events[i].comp(ptime)
			sr = list_of_events[i].spec_ratio()
			logpe = list_of_events[i].log_pe(rsp, complexity, sr)
			label = labels[i]

			write_line = event_id + " " + str(rsp) + " " + str(complexity) + " " + str(sr) + " " + str(logpe) + " " + str(label) + "\n"
			store.write(write_line)
		except:
			# Possible exceptions are TypeError and DivideByZeroError among others
			# TypeError comes if one of the features couldn't be calculated
			# and returns 'nan'
			count += 1
			print ("All features couldn't be calculated. Skipping.")
			continue
	store.close()

	print ("Feature vector stored.")
	return count, init_size

def store_data():
	"""
	This function calls store_in_file to store all instances in file.
	It then calculates the final number of instances 
	left after preprocessing.

	data_home = gmc/data/
	
	parameters
	----------
	None

	returns
	-------
	None

	"""

	data_home = config.project_home + "/data/"
	sf, init_size = store_in_file(data_home)

	final_count = init_size - sf
	print ("\n" + "Number of instances preprocessed = ", final_count)
	print ("Done.")

def main():
	store_data()

if __name__ == "__main__":
	main()