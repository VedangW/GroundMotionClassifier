#!usr/bin/python

import os
import sys
import subprocess as sbp

# Does setup of the gmc module

def setup():
	run_gmc = open('scripts/run_gmc.txt', 'w')
	retcode = sbp.call(['python', 'scripts/setup.py'], stdout=run_gmc, stderr=sbp.STDOUT)
	run_gmc.close()

# Trains the model on the given data

def train():
	run_gmc = open('scripts/run_gmc.txt', 'w')
	retcode = sbp.call(['python', 'GMC/read_events.py'], stdout=run_gmc, stderr=sbp.STDOUT)
	retcode = sbp.call(['python', 'GMC/store_data.py'], stdout=run_gmc, stderr=sbp.STDOUT)
	retcode = sbp.call(['python', 'GMC/fetch_data.py'], stdout=run_gmc, stderr=sbp.STDOUT)
	retcode = sbp.call(['python', 'GMC/train_model.py'], stdout=run_gmc, stderr=sbp.STDOUT)
	run_gmc.close()

# Runs various unit tests

def test():
	run_gmc = open('scripts/run_gmc.txt', 'w')
	retcode = sbp.call(['python', 'tests/test_seismic_event.py'], stdout=run_gmc, stderr=sbp.STDOUT)
	retcode = sbp.call(['python', 'tests/test_seismic_event_features.py'], stdout=run_gmc, stderr=sbp.STDOUT)
	run_gmc.close()

def main():
	if (sys.argv[1] == "0"):
		setup()
	elif (sys.argv[1] == "1"):
		train()
	elif (sys.argv[1] == "2"):
		test()
	else:
		raise TypeError("Argument should be in 0, 1 or 2.")

if __name__ == "__main__":
	main()
