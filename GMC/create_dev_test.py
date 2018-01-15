#!usr/bin/python

import config
import pickle
import pandas as pd
import matplotlib.pyplot as plt
from time import time

def get_station(eid):
	l = eid.split(".")
	return l[2]

def scrub(X):
	"""	
	Function to remove "nan" type entries

	If any of the elements of the instance is nan, which
	is not the float conversion of itself, then remove it.
	The function is of type void because X is mutable.
	
	Parameters
	----------
	X: list of lists
		Each list in list contains [event_id, rsp, comp, sr, pe]

	Returns
	-------
	void

	"""
	for i in X:
		if i[1] != float(i[1]) or i[2] != float(i[2]) or i[3] != float(i[3]) or i[4] != float(i[4]):
			X.remove(i)

def make_sets(events, labels):
	# parameters
	ban = 43
	bdr = 43
	bel = 43
	bhi = 43
	kav = 43
	sur_eq = 43
	sur_bl = 122

	ban_, bdr_, bel_, bhi_, kav_, sur_eq_, sur_bl_ = 0, 0, 0, 0, 0, 0, 0
	dev_events, dev_labels = [], []
	for i in range(len(events)):
		print ("Checking ", events[i].event_id, "...")
		stat = get_station(events[i].event_id)
		if stat == 'BAN' and ban_ < ban:
			ban_ += 1
			dev_events.append(events[i])
			dev_labels.append(labels[i])
		elif stat == 'BDR' and bdr_ < bdr:
			bdr_ += 1
			dev_events.append(events[i])
			dev_labels.append(labels[i])
		elif stat == 'BEL' and bel_ < bel:
			bel_ += 1
			dev_events.append(events[i])
			dev_labels.append(labels[i])
		elif stat == 'BHI' and bhi_ < bhi:
			bhi_ += 1
			dev_events.append(events[i])
			dev_labels.append(labels[i])
		elif stat == 'KAV' and kav_ < kav:
			kav_ += 1
			dev_events.append(events[i])
			dev_labels.append(labels[i])
		elif stat == 'SUR' and labels[i] == 0 and sur_eq_ < sur_eq:
			sur_eq_ += 1
			dev_events.append(events[i])
			dev_labels.append(labels[i])
		elif stat == 'SUR' and labels[i] == 1 and sur_bl_ < sur_bl:
			sur_bl_ += 1
			dev_events.append(events[i])
			dev_labels.append(labels[i])
		else:
			continue

	print ("Done.")
	return dev_events, dev_labels

def make_features(dev_events, dev_labels):
	data_home = config.project_home + "/data/"
	print ("Writing to store...", "\n")

	# Open file store.txt for appending
	store = open(data_home + "dev_store.txt", "w")
	# Count is the number of events which were skipped.
	count = 0

	# For each element in dev_events and labels,
	# 1) Calculate rsp, comp, sr, logpe in that order
	# 2) Convert them all to string and concatenate them and
	# 3) Write to file store.txt

	for i in range(len(dev_events)):
		t = time()
		try:
			event_id = dev_events[i].event_id
			print ("Writing ", event_id)
			rsp, ptime = dev_events[i].ratio_sp()
			complexity = dev_events[i].comp(ptime)
			sr = dev_events[i].spec_ratio()
			logpe = dev_events[i].log_pe(rsp, complexity, sr)
			label = dev_labels[i]

			write_line = event_id + " " + str(rsp) + " " + str(complexity) + " " + str(sr) + " " + str(logpe) + " " + str(label) + "\n"
			store.write(write_line)
		except:
			# Possible exceptions are TypeError and DivideByZeroError among others
			# TypeError comes if one of the features couldn't be calculated
			# and returns 'nan'
			count += 1
			print ("All features couldn't be calculated. Skipping.")
			print("Time = ", time() - t)
			continue
		print("Time = ", time() - t)

	store.close()

def fetch_dev():
	print ("Reading store...")

	data_home = config.project_home + "/data/"
	data = pd.read_csv(data_home + "dev_store.txt", header=None).values

	# Converts list of lists to a flat list
	flat_list = [item for sublist in data for item in sublist]
	data = flat_list

	# Convert to list to needed format
	temp = []
	for x in data:
		x = [i for i in x.split()]
		y = []
		for i in range(6):
			y.append((x.pop(0)))
		string = ""
		for c in x:
			string = string + c + " "
		y.append(string)
		temp.append(y)
	data = temp

	# Convert needed features to float or int
	for i in data:
		# Pop newline character
		i.pop()
		i[1] = float(i[1])
		i[2] = float(i[2])
		i[3] = float(i[3])
		i[4] = float(i[4])
		i[5] = int(i[5])

	print ("Cleaning data...")

	# Remove invalid instances
	for i in data:
		if len(i) != 6:
			data.remove(i)

	# Remove "nan" instances
		scrub(data)

	labels = []
	for a in data:
		x = a.pop()
		labels.append(x)
		a.pop(0)

	for a in data:
		if len(a) != 4:
			data.remove(a)

	no_of_instances = len(data)
	print ("Number of instances left = ", no_of_instances)
	# print (data)
	# print (labels)
	return data, labels

def plot_graphs(data, labels):
	eq_x, eq_y, bl_x, bl_y = [], [], [], []
	for i in range(len(data)):
		if labels[i] == 0:
			eq_x.append(data[i][1])
			eq_y.append(data[i][3])
		elif labels[i] == 1:
			bl_x.append(data[i][1])
			bl_y.append(data[i][3])
		else:
			print ("Not happening.")
			break

	fig = plt.figure('Eq vs bl for dev/test set')

	ax0 = fig.add_subplot(311)
	ax0.scatter(eq_x, eq_y, c='b', label='Earthquake')
	ax0.scatter(bl_x, bl_y, c='r', label='Blast')
	ax0.set_xlabel('Complexity (C)')
	ax0.set_ylabel('log(pe)')
	plt.legend()

	eq_x, eq_y, bl_x, bl_y = [], [], [], []
	for i in range(len(data)):
		if labels[i] == 0:
			eq_x.append(data[i][2])
			eq_y.append(data[i][3])
		elif labels[i] == 1:
			bl_x.append(data[i][2])
			bl_y.append(data[i][3])
		else:
			print ("Not happening.")
			break

	ax1 = fig.add_subplot(312)
	ax1.scatter(eq_x, eq_y, c='b', label='Earthquake')
	ax1.scatter(bl_x, bl_y, c='r', label='Blast')
	ax1.set_xlabel('Spectral Ratio (sr)')
	ax1.set_ylabel('log(pe)')
	plt.legend()

	eq_x, eq_y, bl_x, bl_y = [], [], [], []
	for i in range(len(data)):
		if labels[i] == 0:
			eq_x.append(data[i][1])
			eq_y.append(data[i][2])
		elif labels[i] == 1:
			bl_x.append(data[i][1])
			bl_y.append(data[i][2])
		else:
			print ("Not happening.")
			break

	ax2 = fig.add_subplot(313)
	ax2.scatter(eq_x, eq_y, c='b', label='Earthquake')
	ax2.scatter(bl_x, bl_y, c='r', label='Blast')
	ax2.set_xlabel('Complexity (C)')
	ax2.set_ylabel('Spectral Ratio (sr)')
	plt.legend()

	plt.show()

def create_dev_test():
	data_home = config.project_home + "/data/"
	print ("Loading stored events and labels...")

	# Load all_events from pickled file
	events_in = open(data_home + "events.pkl", "rb")
	events = pickle.load(events_in)
	events_in.close()

	# Load all_labels from pickled file
	labels_in = open(data_home + "labels.pkl", "rb")
	labels = pickle.load(labels_in)
	labels_in.close()

	dev_events, dev_labels = make_sets(events, labels)

	print ("Storing...")

	events_in = open(data_home + "dev_events.pkl", "wb")
	pickle.dump(dev_events, events_in)
	events_in.close()

	events_in = open(data_home + "dev_labels.pkl", "wb")
	pickle.dump(dev_labels, events_in)
	events_in.close()

	print ("Done.")

	make_features(dev_events, dev_labels)

	data, labels = fetch_dev()
	plot_graphs(data, labels)

	print ("Done.")

def main():
	create_dev_test()

if __name__ == "__main__":
	main()