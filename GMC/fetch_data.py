#!usr/bin/python

""" A module to fetch all data from 'store.txt' and convert it 
	into the train and test sets.

	Author: VedangW
"""

import config
import pandas as pd
import pickle
from random import shuffle
from sklearn.model_selection import train_test_split

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

def divide_dataset_custom(X):
	""" 
	Function to divide dataset into train and test in 
	manner such that they receive instances of both 
	classes in a proportionate manner.

	Ratio of division into train and test set is
	predefined as a hyperparameter in gmc/config.py. 
	Using this ratio, we divide the set in a proportionate manner
	into train and test. The dataset is shuffled first.It 
	is recommended to use this in case of skewed data.
	
	Parameters
	----------
	X: list of lists
		The dataset to be divided.

	Returns
	-------
	X_train: list of lists
		Feature vector of the training set.
	X_test: list of lists
		Feature vector of the test set.
	y_train: list
		Label vector of the training set 
	y_test: list
		Label vector of the test set.

	"""
	print ("Custom division selected.")

	# Get number of events of each type in dataset
	one_count = 0
	for i in X:
		if i[5] == 1:
			one_count += 1
	zero_count = len(X) - one_count

	# Randomize the dataset 
	shuffle(X)

	# Put exactly 0.2 * no. of ones ones into test set
	# Put exactly 0.2 * no. of zeros zeros into test set
	# Everything else goes into training set
	X_test = []
	X_train = []

	test_one_count = 0
	test_zero_count = 0
	for a in X:
		if a[5] == 1 and test_one_count <= one_count * config.test_ratio:
			X_test.append(a)
			test_one_count += 1
		elif a[5] == 0 and test_zero_count <= zero_count * config.test_ratio:
			X_test.append(a)
			test_zero_count += 1
		else:
			X_train.append(a)

	# Split training set into features and labels
	y_train = []
	for i in range(len(X_train)):
		y_train.append(X_train[i].pop())

	# Split test set into features and labels
	y_test = []
	for i in range(len(X_test)):
		y_test.append(X_test[i].pop())

	return X_train, X_test, y_train, y_test

def divide_dataset_random(X):
	""" 
	Function to randomly divide dataset into train and test

	Random division into train and test is done by using
	the train_test_split() function available in
	Scikit-Learn. Can use this in case of non-skewed data.

	Parameters
	----------
	X: list of lists
		The dataset to be divided.

	Returns
	-------
	X_train: list of lists
		Feature vector of the training set.
	X_test: list of lists
		Feature vector of the test set.
	y_train: list
		Label vector of the training set 
	y_test: list
		Label vector of the test set.

	"""
	print ("Random division selected.")

	# Separate features and labels
	y = []
	for i in range(len(X)):
		y.append(X[i].pop())

	# Split according to sklearn's function
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=config.test_ratio)
	return X_train, X_test, y_train, y_test

def fetch_data():
	""" 
	Function to read 'store.txt' and create the test and train sets.

	The test and train sets are saved in pickle files in gmc/data/.

	Parameters
	----------
	None

	Returns
	-------
	None

	"""
	print ("Reading store...")

	data_home = config.project_home + "/data/"
	data = pd.read_csv(data_home + "store.txt", header=None).values

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

	no_of_instances = len(data)
	print ("Number of instances left = ", no_of_instances)

	# Call a divide function to divide the data properly
	print ("Dividing data into train and test...")
	X_train, X_test, y_train, y_test = divide_dataset_custom(data)

	# Store each into a pickle file
	print ("Storing train and test...")

	# Store X_train
	X_train_out = open(data_home + "x_train.pkl", "wb")
	pickle.dump(X_train, X_train_out)
	X_train_out.close()

	# store X_test
	X_test_out = open(data_home + "x_test.pkl", "wb")
	pickle.dump(X_test, X_test_out)
	X_test_out.close()

	# store y_train
	y_train_out = open(data_home + "y_train.pkl", "wb")
	pickle.dump(y_train, y_train_out)
	y_train_out.close()

	# store y_test
	y_test_out = open(data_home + "y_test.pkl", "wb")
	pickle.dump(y_test, y_test_out)
	y_test_out.close()

	print ("Done.")

def main():
	fetch_data()

if __name__ == "__main__":
	main()