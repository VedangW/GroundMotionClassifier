#!usr/bin/python

"""	Module to fetch data from store.txt and labels.txt
	and create the feature vector and labels vector.
	It is meant to be imported as separate functions to
	classifier.py.

	Author: VedangW
"""

import pandas

#To fetch feature vector from store.txt
def fetch_feature_vector():
	vector = pandas.read_csv('store.txt', header=None).values

	flat_list = [item for sublist in vector for item in sublist]
	vector = flat_list

	features_train = []
	for x in vector:
		x = [float(i) for i in x.split()]
		features_train.append(x)

	return features_train

# To fetch labels vector from labels.txt
def fetch_labels_vector():
	#index1.txt stores indices from Kachchh whose features have been taken as valid
	index1 = pandas.read_csv('index1.txt', header=None).values

	flat_list = [item for sublist in index1 for item in sublist]
	index1 = flat_list

	#index2.txt stores indices from Surendranagar whose features have been taken as valid
	index2 = pandas.read_csv('index2.txt', header=None).values

	flat_list = [item for sublist in index2 for item in sublist]
	index2 = flat_list

	#Pulling them together in a list of 0s and 1s
	labels = pandas.read_csv('labels.txt', header=None).values

	flat_list = [item for sublist in labels for item in sublist]
	labels = flat_list

	labels_train = []
	for i in index1:
		labels_train.append(i - 1)

	for i in index2:
		labels_train.append(56 + i)

	return labels_train

def main():
	print fetch_feature_vector()
	print fetch_labels_vector()

if __name__ == "__main__":
	main()