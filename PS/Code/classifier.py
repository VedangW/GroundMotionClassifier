#!usr/bin/python

"""
	This is the script code to implementing an SVM
	in the earthquake-blasting differentiation project.

	Earthquake has label 1
	Not Earthquake has label 0

	Author: VedangW
"""

#import statements
import os
import sys
import pandas
import matplotlib.pyplot as plt
from time import time
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from fetch_data import fetch_feature_vector, fetch_labels_vector

def main():
	#creating classifier
	clf = SVC(kernel='rbf')

	features_train = fetch_feature_vector()
	labels_train = fetch_labels_vector()

	t0 = time()
	clf.fit(features_train, labels_train)
	print "Training time: ", time() - t0, " secs"

	plt.scatter(features_train[:,0],features_train[:,1], marker='+')
	plt.show()

	x = [[1.0010466633, 0.169843732038], [1.58787884493, 0.769931641951], [1.23733655143, 0.206543477241], [-3.01018059594, 0.560479182515], [0.721427711822, -0.1930478492097]]
	print clf.decision_function(x)
	print clf.predict(x)

if __name__ == "__main__":
	main()