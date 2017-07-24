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
from sklearn.metrics import accuracy_score
from fetch_data import fetch_feature_vector, fetch_labels_vector

import dash
import dash_core_components as dcc
import dash_html_components as html
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

#	print features_train, '\n', "Length of feature vector: ", len(features_train)
#	print labels_train, '\n', "Length of labels vector: ", len(labels_train)

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

	"""
	t = np.arange(-20., 20., 1)
	fig = plt.figure("Scatterplot of data")
	axes = plt.axis()
	print axes

	ax0 = fig.add_subplot(111)
	ax0.plot(X1, Y1, 'bo', label='Earthquakes', ms = 4)
	ax0.plot(X2, Y2, 'rx', label='Blasting')
	ax0.plot(t, clf.coef_[0][1] * t + clf.coef_[0][0], linewidth=1.0)
	ax0.set_xlabel('Complexity')
	ax0.set_ylabel('log Pe')
	ax0.legend()
	plt.show()
	"""
	
	comp = []
	logpose = []
	lbl = []
	of_class = []

	index = 0
	for i in features_train:
		comp.append(i[0])
		logpose.append(i[1])

		if labels_train[index] == 0:
			of_class.append('Earthquake')
		elif labels_train[index] == 1:
			of_class.append('Blasting')
		index += 1

	raw_data = {'complexity': comp, 'logpoe': logpose, 'label': labels_train, 'class': of_class}
	df = pd.DataFrame(raw_data, columns=['complexity', 'logpoe', 'label', 'class'])
	df.to_csv('~/Desktop/PS/Code/featurestore.csv')

	app = dash.Dash()

	df = pd.read_csv('~/Desktop/PS/Code/featurestore.csv')

	app.layout = html.Div([
	    dcc.Graph(
	        id='complexity-vs-logPe',
	        figure={
	            'data': [
	                go.Scatter(
	                    x=df[df['label'] == i]['complexity'],
	                    y=df[df['label'] == i]['logpoe'],
	                    text=df[df['label'] == i]['class'],
	                    mode='markers',
	                    opacity=0.7,
	                    marker={
	                        'size': 15,
	                        'line': {'width': 0.5, 'color': 'white'}
	                    },
	                    name=i
	                ) for i in df.label.unique()
	            ],
	            'layout': go.Layout(
	                xaxis={'type': 'log', 'title': 'Complexity'},
	                yaxis={'title': 'log Pe'},
	                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
	                legend={'x': 0, 'y': 1},
	                hovermode='closest'
	            )
	        }
	    )
	])

	app.run_server()


###################################a
#	x = ask_for_data()	
	
#	x = [[1.0010466633, 0.169843732038], [1.58787884493, 0.769931641951], [1.23733655143, 0.206543477241], [-3.01018059594, 0.560479182515], [0.914409898799, -0.35812293039]]
#	print "Distances of points from decision boundary: ", clf.decision_function(x)
	""""
	pred = clf.predict(x)

	for prediction in pred:
		if prediction == 0:
			print "Earthquake"
		elif prediction == 1:
			print "Blasting"
		else:
			print "Invalid data, check again."
	"""
if __name__ == "__main__":
	main()
