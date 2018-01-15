#!usr/bin/python

""" A module to create the classifier, train it,
	predict on the test set and store it on disk

	Author: VedangW
"""

import warnings
warnings.filterwarnings('ignore')

import config
import pickle
import plot
import analyze
import cross_validate as cv

from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import f1_score
from sklearn.model_selection import cross_val_score

from sklearn.tree import _tree
from sklearn.neural_network import MLPClassifier

#import graphviz 

# def tree_to_code(tree, feature_names):
#     tree_ = tree.tree_
#     feature_name = [
#         feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
#         for i in tree_.feature
#     ]
#     print ("def tree({}):".format(", ".join(feature_names)))

#     def recurse(node, depth):
#         indent = "  " * depth
#         if tree_.feature[node] != _tree.TREE_UNDEFINED:
#             name = feature_name[node]
#             threshold = tree_.threshold[node]
#             print ("{}if {} <= {}:".format(indent, name, threshold))
#             recurse(tree_.children_left[node], depth + 1)
#             print ("{}else:  # if {} > {}".format(indent, name, threshold))
#             recurse(tree_.children_right[node], depth + 1)
#         else:
#             print ("{}return {}".format(indent, tree_.value[node]))

#     recurse(0, 1)

def split_ids(X):
	""" 
	Function to remove the event_ids from the feature vectors.

	Parameters
	----------
	X: list
		Feature vector
	
	Returns
	-------
	X: list
		Feature vector without ids 
	ids: list
		List of corresponding IDs

	"""

	ids = []
	for i in range(len(X)):
		ids.append(X[i].pop(0))
	return X, ids

def unpickle():
	""" 
	A function to load the train and test set from disk.

	This function uses pickle.load to load X_train, y_train, 
	X_test, y_test from their respective pickle files in
	gmc/data/.
	
	Parameters
	----------
	None

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

	data_home = config.project_home + "/data/"

	# Load X_train
	X_train_in = open(data_home + "x_train.pkl", "rb")
	X_train = pickle.load(X_train_in)
	X_train_in.close()

	# Load X_test
	X_test_in = open(data_home + "x_test.pkl", "rb")
	X_test = pickle.load(X_test_in)
	X_test_in.close()

	# Load y_train
	y_train_in = open(data_home + "y_train.pkl", "rb")
	y_train = pickle.load(y_train_in)
	y_train_in.close()

	# Load y_test
	y_test_in = open(data_home + "y_test.pkl", "rb")
	y_test = pickle.load(y_test_in)
	y_test_in.close()

	return X_train, X_test, y_train, y_test

def train_model():
	""" 
	Main function creates a classifier, gets the cross-validation
	scores, fits the data in the classifier and stores it on disk

	Parameters
	----------
	None

	Returns
	------- 
	None

	"""
	
	data_home = config.project_home + "/data/"

	# Retrieve X_train, y_train, X_test, y_test from disk
	X_train, X_test, y_train, y_test = unpickle()

	# Separate ids from the feature vectors
	X_train, train_ids = split_ids(X_train)
	X_test, test_ids = split_ids(X_test)

	# C, gamma = cv.cross_validation(X_train, y_train)

	# # Create a Support Vector Machine Classifier
	# clf = SVC(kernel='rbf', C=C, gamma=gamma)

	clf = SVC(kernel='rbf', C=3)

	# Fit the training data
	clf.fit(X_train, y_train)

	# print ("Rule set of tree: ")
	# tree_to_code(clf, features)

	# dot_data = tree.export_graphviz(clf, out_file=None) 
	# graph = graphviz.Source(dot_data) 
	# graph.render("iris") 

	# Save the model on disk
	clf_out = open(data_home + "model.pkl", "wb")
	pickle.dump(clf, clf_out)
	clf_out.close()

	# Predict on the test data
	pred = clf.predict(X_test)

	# Print stats for predictions
	analyze.analyze_prediction(pred, y_test)

	# Plot the graph (see plot.py for more documentation of this)
	# plot.plot_tt(X_train, y_train, X_test, y_test, clf)
	plot.plot_predictions(X_train, y_train, X_test, y_test)

	print ("Done.")

def main():
	train_model()

if __name__ == "__main__":
	main()