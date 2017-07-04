#!usr/bin/python

"""
	This is the script code to implementing an SVM
	in the earthquake-blasting differentiation project.

	Earthquake has label 1
	Not Earthquake has label 0
"""

#import statements
import sys
from time import time
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

#Training the classifier
def fit(clf, features_train, labels_train):
	t0 = time()
	clf.fit(features_train, labels_train)
	print "Training time: ", time() - t0, " secs"

#Predicts the labels of a test set
def predict(features_test, clf):
	t1 = time()
	pred = clf.predict(features_test)
	print "Prediction time: ", time() - t1, " secs"
	return pred

#Returns accuracy of the SVM
def accuracy(pred, labels_test):
	acc_score = accuracy_score(pred, labels_test)
	return acc_score

#Command line arguments:
#argv[1] = deciding_argument -> t = train, p = predict, a = accuracy
#if argv[1] = 't' -> argv = ['t', features_train, labels_train]
#if argv[1] = 'p' -> argv = ['p', features_test]
#if argv[1] = 'a' -> argv = ['a', features_test, labels_test]
def main():
	#creating classifier
	clf = SVC(kernel='linear')

	if (sys.argv[1] == 't'):
		print "Beginning to train..."
		fit(clf, argv[2], argv[3])
		print "Trained the classifer."
	elif (sys.argv[1] == 'p'):
		pred = predict(clf, argv[2])
		print pred
	elif (sys.argv[1] == 'a'):
		pred = predict(clf, argv[2])	
		acc_score = accuracy(pred, argv[3])
		print "Accuracy is: ", acc_score

if __name__ == "__main__":
	main()