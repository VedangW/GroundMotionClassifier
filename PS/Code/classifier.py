#!usr/bin/python

"""
	This is the script code to implementing an SVM
	in the earthquake-blasting differentiation project.

	Earthquake has label 0
	Not Earthquake has label 1

	Author: VedangW
"""

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from time import time
from sklearn.svm import SVC
from fetch_data import fetch_feature_vector, fetch_labels_vector

import plotly
import plotly.graph_objs as go

def ask_for_data():
	test_data = []
	while 1:
		cmpl = float(raw_input("Enter complexity: "))
		logpoe = float(raw_input("Enter log of Pe: "))
		inter = [cmpl, logpoe]
		test_data.append(inter)
		ans = raw_input("More data? (y/n): ")
		if ans == 'n':
			break
	return test_data

def main():
	#creating classifier
	clf = SVC(kernel='linear')

	features_train = fetch_feature_vector()
	labels_train = fetch_labels_vector()

	t0 = time()
	clf.fit(features_train, labels_train)
	print "Training time: ", time() - t0, " secs"

	X1 = []
	Y1 = []
	X2 = []
	Y2 = []	
	for i in range(0, len(features_train) - 1):
		if labels_train[i] == 0:
			X1.append(features_train[i][0])
			Y1.append(features_train[i][1])
		elif labels_train[i] == 1:
			X2.append(features_train[i][0])
			Y2.append(features_train[i][1])

	slope = clf.coef_[0][1]
	intercept = clf.coef_[0][0]
	xi = np.arange(-10, 13, 0.02)
	yline = slope * xi + intercept

	trace0 = go.Scatter(
		x = xi,
		y = yline,
		name = 'Hyperplane',
		mode = 'lines',
		)

	trace1 = go.Scatter(
	    x = X1,
	    y = Y1,
	    name = 'Earthquake',
	    mode = 'markers',
	    opacity = 0.7,
	    marker=dict(
	        size='16',
	        color = 'purple',
	    )
	)

	trace2 = go.Scatter(
		x = X2,
		y = Y2,
		name = 'Blasting',
		mode = 'markers',
		opacity = 0.7,
		marker = dict(
			size = '16',
			color = 'orange',
		)
	)

	data = [trace0, trace1, trace2]

	plotly.offline.plot({"data": data, "layout": go.Layout(title='Scatterplot and Decision Boundary')})

if __name__ == "__main__":
	main()
