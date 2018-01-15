#!usr/bin/python

def measure_accuracy(pred, truth):
	""" 
	A function to measure the accuracy and the F1 score

	Each metric is calculated as its definition relating
	to the true positives, true negatives, false positives,
	false negatives.

	Parameters
	----------
	pred: list
		List of predicted values (1 or 0) 
	truth: list
		List of labels for test set

	Returns
	-------
	accuracy: float
		Accuracy (by definition) on the test set
	f1score: float
		F1 score (by definition) on the test set

	"""

	# tp = true positives
	# tn = true negatives
	# fp = false positives
	# fn = false negatives

	# Set all to zero
	tp, tn, fp, fn = 0, 0, 0, 0

	try:
		# Check if both are of equal length
		assert len(pred) == len(truth)
	except AssertionError:
		print ("pred and truth of different sizes.")
		return

	# Compare each value oin pred and truth and increment
	# parameter accordingly
	for i in range(len(pred)):
		if pred[i] == 0 and truth[i] == 0:
			tp += 1
		elif pred[i] == 0 and truth[i] == 1:
			fp += 1
		elif pred[i] == 1 and truth[i] == 1:
			tn += 1
		elif pred[i] == 1 and truth[i] == 0:
			fn += 1
		else:
			raise TypeError("Entries in pred and truth must by 0 or 1")

	# By definition of precision and recall
	precision = tp / (tp + fp)
	recall = tp / (tp + fn)

	# By definition of accuracy and f1 score
	accuracy = (tp + tn) / (tp + tn + fp + fn)
	f1score = 2 * precision * recall / (precision + recall)

	return [accuracy, f1score, tp, tn, fp, fn]

def analyze_prediction(pred, truth):
	"""
	A function to analyze the performance of the classifier on
	the test set using a confusion matrix approach

	Parameters
	----------
	pred: list
		List of predictions by the classifier on test set
	truth: list
		Labels of the test set

	"""
	metrics = measure_accuracy(pred, truth)

	print ("-- Analyzing predictions on test set --")
	print ("")

	print ("No. of instances in test set = ", len(truth))
	print ("")

	# Calculate the number of positives and negatives predicted
	pos, neg = 0, 0
	for i in truth:
		if i == 0:
			pos += 1
		else:
			neg += 1

	print ("No. of positives in test set = ", pos)
	print ("No. of negatives in test set = ", neg)
	print ("")

	# Calculate the number of 0s and 1s predicted
	count = 0
	for i in pred:
		if i == 1:
			count += 1
	print ("No. of positives predicted = ", len(pred) - count)
	print ("No. of negatives predicted = ", count)
	print ("")

	# Print contents of the confusion matrix
	print ("True positives = ", metrics[2])
	print ("True negatives = ", metrics[3])
	print ("False positives = ", metrics[4])
	print ("False negatives = ", metrics[5])
	print ("")

	print ("Accuracy achieved on test = ", metrics[0] * 100, "%")
	print ("F1 score achieved on test = ", metrics[1] * 100, "%")