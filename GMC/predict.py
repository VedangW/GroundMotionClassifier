#!usr/bin/python

""" A module for the prediction of a particular event.
	
	Parameters
	----------
	z_path: str
		Path to the z_file 
	n_path: str
		Path to the n_file
	e_path: str
		Path to the e_file

	Author: VedangW
"""

import sys
import config
import pickle
from obspy import read
from SeismicEvent import SeismicEvent

def predict(event):
	""" 
	A function to process the event parameters, load
	the model and make the prediction.

	Parameters
	----------
	event: SeismicEvent object
		Created in read_event

	Returns
	-------
	pred: Number (0 or 1)
		Prediction for the event

	""" 
	
	data_home = config.project_home + "/data/"

	# Load classifier from disk
	clf_out = open(data_home + "model.pkl", "rb")
	clf = pickle.load(clf_out)
	clf_out.close()

	# Calculate all parameters for the event
	try:
		rsp, ptime = event.ratio_sp()
		c = event.comp(ptime)
		sr = event.spec_ratio()
		logpe = event.log_pe(rsp, c, sr)
	except:
		# If not possible, return -1
		print ("All features couldn't be calculated.")
		return -1

	# Feed preprocessed info to the classifier
	feat = [rsp, c, sr, logpe]
	pred = clf.predict([feat])

	return pred[0]

def read_event(z_file, n_file, e_file):
	""" 
	A function to read the z_path, n_path and e_path
	into a SeismicEvent

	Parameters
	---------
	z_path: str
		Path to the z_file 
	n_path: str
		Path to the n_file
	e_path: str
		Path to the e_file

	Returns
	-------
	se: SeismicEvent object
		SeismicEvent with these three traces

	""" 

	# Read the traces
	st = read(z_file)
	st += read(n_file)
	st += read(e_file)

	se = SeismicEvent(st, "new_event")
	return se

def check(z_file, n_file, e_file):
	"""
	Function which prints the prediction

	Parameters
	----------
	z_path: str
		Path to the z_file 
	n_path: str
		Path to the n_file
	e_path: str
		Path to the e_file

	Returns
	-------
	None

	"""
	seismic_event = read_event(z_file, n_file, e_file)
	pred = predict(seismic_event)

	if pred == 0:
		print ("Given event is an Earthquake")
	elif pred == 1:
		print ("Given event is a Blast")
	else:
		print ("Couldn't classify event.")

def main():
	check(sys.argv[1], sys.argv[2], sys.argv[3])

if __name__ == "__main__":
	main()