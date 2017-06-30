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

def main():
	#creating classifier
	clf = SVC(kernel='linear')

	#training the SVM
	t0 = time()
	clf.fit(features_train, labels_train)
	print ("training time: ", round(time() - t0, 3), "secs")

	#predicting
	t1 = time()
	pred = clf.predict(features_train)
	print ("prediction time: ", round(time() - t1, 3), "secs")

	#finding the accuracy
	print ("accuracy is: ", accuracy_score(pred, labels_test))

if __name__ == "__main__":
	main()