#!usr/bin/python

import warnings
warnings.filterwarnings("ignore")

import config
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from plot import plot_heatmap
from train_model import split_ids
from analyze import measure_accuracy
from sklearn.svm import SVC

def maximize_by_accuracy(accs):
	"""
	A function to return the C and gamma by 
	maximizing the accuracy metric.

	Parameters
	---------
	accs: list of lists
		A 2D representation of the accuracies with
		different values of C and gamma.

	Returns
	-------
	r: int
		j index of the 2D array
	s: int
		i index of the 2D array
	maximum: float
		Maximum accuracy in the matrix

	"""
	maximum = 0
	for i in accs:
		m = max(i)
		if m > maximum:
			maximum = m
			r = i.index(m)
			s = accs.index(i)

	return r, s, maximum

def maximize_by_f1score(f1s):
	"""
	A function to return the C and gamma by 
	maximizing the F1 score metric.

	Parameters
	---------
	f1s: list of lists
		A 2D representation of the accuracies with
		different values of C and gamma.

	Returns
	-------
	r: int
		j index of the 2D array
	s: int
		i index of the 2D array
	maximum: float
		Maximum F1 Score in the matrix
		
	"""
	maximum = 0
	for i in f1s:
		m = max(i)
		if m > maximum:
			maximum = m
			r = i.index(m)
			s = f1s.index(i)

	return r, s, maximum


def train_val_split(X_train, y_train):
	""" 
	A customized function to split the training set into
	train and validation according to the ratios defined 
	in the config file.

	Parameters
	----------
	X_train: list of lists
		The training dataset with all the features
	y_train: list
		The list of labels

	Returns
	-------
	x_tr: list of lists
		List of all instances in the final training set
	y_tr: list
		List of labels of the training set
	x_val: list of lists
		List of all instances in the validation set
	y_val: list
		List of labels of the validation set

	"""

	# Get number of 0s and 1s in the training set
	one_count, zero_count = 0, 0
	for i in y_train:
		if i == 0:
			zero_count += 1
		else:
			one_count += 1

	# Retrive training and validation ratios from config
	tr_ratio = config.train_ratio
	val_ratio = config.validation_ratio

	# Calculate the relative ratio
	v = val_ratio/(tr_ratio + val_ratio)

	# Initialize the new training and validation sets
	x_tr, y_tr, x_val, y_val = [], [], [], []

	# Proportionately divide each label into the training
	# and validation sets
	val_one_count = 0
	val_zero_count = 0
	for i in range(len(X_train)):
		if y_train[i] == 0 and val_zero_count <= v * zero_count:
			x_val.append(X_train[i])
			y_val.append(y_train[i])
			val_zero_count += 1
		elif y_train[i] == 1 and val_one_count <= v * one_count:
			x_val.append(X_train[i])
			y_val.append(y_train[i])
			val_one_count += 1
		else:
			x_tr.append(X_train[i])
			y_tr.append(y_train[i])

	return x_tr, y_tr, x_val, y_val

def plot_validation_data(accs, f1s, cs):
	"""
	Function to plot the validation set according to the Cs

	Parameters
	----------
	accs: list of lists
		A 2D representation of the accuracies with
		different values of C and gamma.
	f1s: list of lists
		A 2D representation of the accuracies with
		different values of C and gamma.
	cs: list
		List of Cs

	Returns
	-------
	None

	"""
	fig = plt.figure('Analysis on Validation set')

	# Plot analysis of the validation set
	ax0 = fig.add_subplot(111)
	ax0.plot(cs, accs, label='acc on val')
	ax0.plot(cs, f1s, label='f1_score on val')
	ax0.set_xlabel('Value of C')
	ax0.set_ylabel('Metrics')
	ax0.legend()

	plt.show()

def cross_validation(X_train, y_train):
	"""
	A function to carry out the cross validation on the
	training set by selecting a wide range of Cs and gammas

	Parameters
	----------
	X_train: list of lists
		Feature vector of the training set.
	y_train: list
		Label vector of the training set

	Returns
	-------
	C: float
		The optimal value of C found
	gamma: float
		The optimal value of gamma found

	"""

	# Split training set into test and validation set
	print ("Performing cross validation...")
	x_tr, y_tr, x_val, y_val = train_val_split(X_train, y_train)

	# Generate a range of Cs anf gammas
	cs, gammas = [], []
	i = -5
	while i <= 4:
		cs. append(10 ** i)
		gammas.append(10 ** i)
		i += 2

	# Calculate the accuracy and F1 score for each combination
	# of C and gamma
	accs, f1s = [], []
	for c in cs:
		acc_ = []
		f1_ = []
		for g in gammas:
			print ("C = ", c, ", gamma = ", g)
			clf = SVC(kernel='rbf', C=c, gamma=g)
			clf.fit(x_tr, y_tr)
			pred = clf.predict(x_val)
			metrics = measure_accuracy(pred, y_val)
			acc_.append(metrics[0])
			f1_.append(metrics[1])
		accs.append(acc_)
		f1s.append(f1_)

	# Get the index with maximum accuracy
	i, j, val = maximize_by_accuracy(accs)

	# Plot the validation data and heatmaps
	plot_validation_data(accs, f1s, cs)
	plot_heatmap(accs, 'Accuracy heatmap', ['C', 'gamma'])
	plot_heatmap(f1s, 'F1 Score heatmap', ['C', 'gamma'])

	# Returns C and gamma for which the accuracy is optimal
	C = cs[j]
	gamma = gammas[i]
	print ("")
	print ("Hyperparamters chosen: C = ", C, ", gamma = ", gamma)
	print ("Cross validation done.")
	print ("")

	return C, gamma