#!usr/bin/python

""" A module to read all events and labels from the data
	into two lists and store them on disk.

	Author: VedangW
"""

import os
import sys
import config
import fnmatch
import pickle
from SeismicEvent import SeismicEvent
from obspy import read

def read_directory(home, folder):
	""" 
	Function to group files in a folder into SeismicEvents.

	This function groups files by finding all files ending 
	with 'Z.sac' and finding their other components.
	It then adds them all to a list and the labels to a 
	different list and returns them.
	
	Parameters
	----------
	home: str
		Path to the data folder
	folder: str
		Name of the folder to process

	Returns
	-------
	list_of_events: list
		A list of SeismicEvents 
	labels: list
		A list of labels

	"""

	# For calculating label
	lbl = folder.split('_')[1]

	# Get list of files in folder ending with 'Z.sac'
	list_z = []
	for file in os.listdir(home + folder):
		if fnmatch.fnmatch(file, '*Z.sac'):
			list_z.append(file)

	# For each 'Z.sac', do:
	list_of_events = []
	for a in list_z:
		print ("Processing ", a, "...")
		event = []
		event.append(a)

		# Replace Z with N in name of file
		l = a.split('.')
		l4 = list(l[4])
		l4[2] = 'N'
		l[4] = ''.join(l4)
		name = '.'.join(l)
		event.append(name)

		# Replace Z with E in name of file
		l = a.split('.')
		l4 = list(l[4])
		l4[2] = 'E'
		l[4] = ''.join(l4)
		name = '.'.join(l)
		event.append(name)

		# Calculate event_id by removing '.sac'
		ev_id = list(event[0])
		for i in range(4):
			ev_id.pop()
		ev_id = ''.join(ev_id)

		# Read the each event into a stream
		# If 1 or 2 of the files are not found then
		# skip the event.
		try:
			st = read(home + folder + '/' + event[0])
		except FileNotFoundError:
			print (event[0] + " not found. Skipping.")
			continue
		try:
			st += read(home + folder + '/' + event[1])
		except FileNotFoundError:
			print (event[1] + " not found. Skipping.")
			continue
		try:
			st += read(home + folder + '/' + event[2])
		except FileNotFoundError:
			print (event[2] + " not found. Skipping.")
			continue

		# Convert the stream to a SeismicEvent object and add it.
		list_of_events.append(SeismicEvent(st, ev_id))

	# Earthquake is 0, blast is 1

	# If folder name ends with eq then label = 0
	# otherwise label = 1
	labels = []
	length = len(list_of_events)
	if lbl == "eq":
		for i in range(length):
			labels.append(0)
	elif lbl == "bl":
		for i in range(length):
			labels.append(1)
	else:
		# If label name doesn't end with either 0 or 1
		raise StandardError("Not a valid directory.")

	return list_of_events, labels

""" args: []
	returns: None

	This function looks at each sub-directory in the data
	directory and returns relevant SeismicEvents in it.
	It then pickles them as a list and stores the events 
	in 'events.pkl' and labels in 'labels.pkl'
"""

def read_events():
	"""
	Function to enter each directory in data folder and
	locate and read events into a list of SeismicEvents

	Parameters
	----------
	None

	Returns
	-------
	None
	
	"""
	print ("Locating events in the data directory...")

	data_home = config.project_home + "/data/"
	sub_dirs = next(os.walk(data_home))[1]

	all_events = []
	all_labels = []

	# Enter each directory and retrieve its events and labels
	for d in sub_dirs:
		print("Entering directory ", d, "...")
		loe, labels = read_directory(data_home, d)
		all_events += loe
		all_labels += labels

	print ("\n" + "All instances collected.")
	print ("Number of instances detected = ", len(all_events), "\n")

	# Store all_events in 'events.pkl'
	events_out = open(data_home + "events.pkl", "wb")
	pickle.dump(all_events, events_out)
	events_out.close()

	# Store all_labels in 'labels.pkl'
	labels_out = open(data_home + "labels.pkl", "wb")
	pickle.dump(all_labels, labels_out)
	labels_out.close()

	print ("Events and labels stored on disk.")

def main():
	read_events()

if __name__ == "__main__":
	main()