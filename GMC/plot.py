#!usr/bin/python

""" A module which plots the train and test set

	Author: VedangW
"""
import warnings
warnings.filterwarnings("ignore")

import matplotlib.pyplot as plt

import seaborn as sns
import plotly
import plotly.graph_objs as go

from sklearn.svm import SVC

def plot_tt(X_train, y_train, X_test, y_test, clf):
	""" 
	Function to plot the graph for the training and
	test set.

	This plots a scatterplot for all the training instances and
	the test instances in 2D, where the axes are :
	X -> Complexity
	Y -> log(Power of Event)

	Parameters
	----------
	X_train: list of lists
		Feature vector of the training set.
	X_test: list of lists
		Feature vector of the test set.
	y_train: list
		Label vector of the training set 
	y_test: list
		Label vector of the test set.
	clf: SVC object
		A Scikit-Learn Support Vector Machine classifier
		which has been trained.

	Returns
	-------
	None

	"""	

	# Take only the complexity and log_pe from X_train
	X1, y1 = [], []
	for i in range(len(X_train)):
		X1.append(X_train[i][1])
		y1.append(X_train[i][3])

	# Take only the complexity and log_pe from X_test
	X2, y2 = [], []
	for i in range(len(X_test)):
		X2.append(X_test[i][1])
		y2.append(X_test[i][3])

	# trace for Training set
	trace1 = go.Scatter(
	    x = X1,
	    y = y1,
	    name = 'Train',
	    mode = 'markers',
	    text = 'train',
	    opacity = 0.7,
	    marker=dict(
	        size='10',
	        color = 'purple',
	    )
	)

	# trace for Testing set
	trace2 = go.Scatter(
		x = X2,
		y = y2,
		name = 'Test',
		mode = 'markers',
		text = 'test',
		opacity = 0.7,
		marker = dict(
			size = '10',
			color = 'orange',
		)
	)

	# Description of layout
	layout = go.Layout(
	    title='Scatterplot of data',
	    xaxis=dict(
	        title='complexity',
	        titlefont=dict(
	            family='Courier New, monospace',
	            size=18,
	            color='#7f7f7f'
	        )
	    ),
	    yaxis=dict(
	        title='log Pe',
	        titlefont=dict(
	            family='Courier New, monospace',
	            size=18,
	            color='#7f7f7f'
	        )
	    )
	)

	# Append traces to a list
	data = [trace1, trace2]
	# Plot the graph
	plotly.offline.plot({"data": data, "layout": layout}, filename="Train vs Test")

def plot_eb(X_train, y_train, X_test, y_test):
	"""
	A function to plot the distribution of the 
	train and test sets using plotly.

	Parameters
	----------
	X_train: list of lists
		Feature vector of the training set.
	X_test: list of lists
		Feature vector of the test set.
	y_train: list
		Label vector of the training set 
	y_test: list
		Label vector of the test set.

	Returns
	-------
	None

	"""

	# Create lists x1, y1, x2, y2 
	x1, y1, x2, y2 = [], [], [], []
	for i in range(len(y_train)):
		if y_train[i] == 1:
			x2.append(X_train[i][1])
			y2.append(X_train[i][3])
		elif y_train[i] == 0:
			x1.append(X_train[i][1])
			y1.append(X_train[i][3])

	for i in range(len(y_test)):
		if y_test[i] == 1:
			x2.append(X_test[i][1])
			y2.append(X_test[i][3])
		elif y_test[i] == 0:
			x1.append(X_test[i][1])
			y1.append(X_test[i][3])

	# trace for Training set
	trace1 = go.Scatter(
	    x = x1,
	    y = y1,
	    name = 'Earthquake',
	    mode = 'markers',
	    text = 'eq',
	    opacity = 0.7,
	    marker=dict(
	        size='10',
	        color = 'green',
	    )
	)

	# trace for Testing set
	trace2 = go.Scatter(
		x = x2,
		y = y2,
		name = 'Blasting',
		mode = 'markers',
		text = 'blast',
		opacity = 0.7,
		marker = dict(
			size = '10',
			color = 'yellow',
		)
	)

	# Description of layout
	layout = go.Layout(
	    title='Scatterplot of data',
	    xaxis=dict(
	        title='complexity',
	        titlefont=dict(
	            family='Courier New, monospace',
	            size=18,
	            color='#7f7f7f'
	        )
	    ),
	    yaxis=dict(
	        title='log Pe',
	        titlefont=dict(
	            family='Courier New, monospace',
	            size=18,
	            color='#7f7f7f'
	        )
	    )
	)

	# Append traces to a list
	data = [trace1, trace2]
	# Plot the graph
	plotly.offline.plot({"data": data, "layout": layout}, filename="Eqs vs Blasts")

def plot_predictions(X_train, y_train, X_test, y_test):
	"""
	A function to plot the prediction distribution and the
	train and test set. The x-axis is the complexity and the y-axis is
	the log of the power of event.

	Parameters
	----------
	X_train: list of lists
		Feature vector of the training set.
	X_test: list of lists
		Feature vector of the test set.
	y_train: list
		Label vector of the training set 
	y_test: list
		Label vector of the test set.

	Returns
	-------
	None

	"""
	x1, y1, x2, y2 = [], [], [], []
	for i in range(len(y_train)):
		if y_train[i] == 1:
			x2.append(X_train[i][1])
			y2.append(X_train[i][3])
		elif y_train[i] == 0:
			x1.append(X_train[i][1])
			y1.append(X_train[i][3])

	for i in range(len(y_test)):
		if y_test[i] == 1:
			x2.append(X_test[i][1])
			y2.append(X_test[i][3])
		elif y_test[i] == 0:
			x1.append(X_test[i][1])
			y1.append(X_test[i][3])

	# Take only the complexity and log_pe from X_train
	tr_x, tr_y = [], []
	for i in range(len(X_train)):
		tr_x.append(X_train[i][1])
		tr_y.append(X_train[i][3])

	# Take only the complexity and log_pe from X_test
	te_x, te_y = [], []
	for i in range(len(X_test)):
		te_x.append(X_test[i][1])
		te_y.append(X_test[i][3])

	# Plotting the graphs
	fig = plt.figure('Train, test and Predictions')

	# Earthquakes vs blasts
	ax0 = fig.add_subplot(211)
	ax0.scatter(x1, y1, c='b', marker='o', label='earthquakes')
	ax0.scatter(x2, y2, c='r', marker='o', label='blasts')
	ax0.set_xlabel('Complexity (C)')
	ax0.set_ylabel('log(pe)')
	ax0.legend()

	# Train vs test
	ax1 = fig.add_subplot(212)
	ax1.scatter(tr_x, tr_y, c='g', marker='o', label='train')
	ax1.scatter(te_x, te_y, c='y', marker='o', label='test')
	ax1.set_xlabel('Complexity')
	ax1.set_ylabel('log(pe)')
	ax1.legend()

	plt.show()

def plot_heatmap(data, filename, labels):
	"""
	Function to plot a heatmap with the x and y labels.
	Used for accuracy and F1 score heatmap analysis on the
	validation set.

	Parameters
	----------
	data: list of lists
		A 2D array containing the values at those points
	filename: str
		Name of file
	labels: list
		A list with 2 elements: x-axis name and y-axis name

	Returns
	------
	None

	"""

	# Use a seaborn heatmap
	ax = sns.heatmap(data, annot=True)
	ax.set_xlabel(labels[0])
	ax.set_ylabel(labels[1])
	ax.legend()
	plt.show()