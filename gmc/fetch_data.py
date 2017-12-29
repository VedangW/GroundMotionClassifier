#!usr/bin/python

"""	Module to fetch data from store.txt and labels.txt
	and create the feature vector and labels vector.
	It is meant to be imported as separate functions to
	classifier.py.

	Author: VedangW
"""

import pandas

"""	To fetch feature vector from store.txt.
	
	The feature vector is created in this function, which is called
	by classifier to retrieve data in store.txt.

	### args:
	None.

	### returns:
	A python list of features for all instances. 
"""
def fetch_feature_vector():
	vector = pandas.read_csv('store.txt', header=None).values

	flat_list = [item for sublist in vector for item in sublist]
	vector = flat_list

	features_train = []
	for x in vector:
		x = [i for i in x.split()]
		y = []
		y.append(float(x.pop(0)))
		y.append(float(x.pop(0)))
		string = ""
		for c in x:
			string = string + c + " "
		y.append(string)
		features_train.append(y)

	return features_train


"""	To fetch label vector from labels.txt.
	
	The label vector is created in this function, which is called
	by classifier to retrieve data in labels.txt.

	### args:
	None.

	### returns:
	A python list of labels for all instances. 
"""
def fetch_labels_vector():
	#index1.txt stores indices from Kachchh whose features have been taken as valid
	index1 = pandas.read_csv('index1.txt', header=None).values

	flat_list = [item for sublist in index1 for item in sublist]
	index1 = flat_list

#	print index1

	#index2.txt stores indices from Surendranagar whose features have been taken as valid
	index2 = pandas.read_csv('index2.txt', header=None).values

	flat_list = [item for sublist in index2 for item in sublist]
	index2 = flat_list

#	print index2

	#Pulling them together in a list of 0s and 1s
	labels = pandas.read_csv('labels.txt', header=None).values

	flat_list = [item for sublist in labels for item in sublist]
	labels = flat_list

#	print labels

	labels_train = []
	for i in index1:
		labels_train.append(labels[i - 1])

	for i in index2:
		labels_train.append(labels[56 + i])

	return labels_train


""" MAIN:
	For analysis of features and labels.
	Prints the feature and label vectors.
"""
def main():
	print fetch_feature_vector()
	print fetch_labels_vector()

if __name__ == "__main__":
	main()