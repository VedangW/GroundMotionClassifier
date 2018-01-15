#!usr/bin/python

""" A module to setup the general environment for the app

	Author: VedangW
"""

import os
import subprocess as sbp

def update_config():
	""" 
	Function to update the config file as needed.
	
	Updates the config file such that the project home
	variable is set according to the path given by the
	user.
	
	Parameters
	----------
	None

	Returns
	-------
	path: str
		path of project home

	"""
	print ("Detecting GMC home...")

	# Write to scripts/boot_data.txt the address to the 
	# project home
	boot_data = open('scripts/boot_data.txt', 'w')
	retcode = sbp.call(['pwd'], stdout=boot_data, stderr=sbp.STDOUT)
	boot_data.close()

	print ("Updating config file...")

	# Open config file and read the lines
	config_file = open('config.py')
	lines = config_file.readlines()
	config_file.close()

	# Read project_home from boot_data
	boot_data = open('scripts/boot_data.txt', 'r')
	path = boot_data.readlines()[0]
	boot_data.close()

	# Change 2nd line to set new value for project_home
	path_ = list(path)
	path_[-1:] = "'"
	path_ = ''.join(path_)
	write_str = "project_home = " + "'" + path_ + "\n"
	lines[1] = write_str

	# Open config and write new project_home to it
	pl = open('config.py', 'w')
	for i in lines:
		pl.write(i)
	pl.close()

	print ("Updated.")

	return path

def update_bashrc(path):
	""" 
	Function to update the .bashrc file

	Appends the project home to the PYTHONPATH
	and exports it in ~/.bashrc
	
	Parameters
	----------
	path: str
		Path to project home

	Returns 
	-------
	None

	"""
	
	print ("Updating PYTHONPATH in .bashrc...")

	python_path_str = "export PYTHONPATH=$PYTHONPATH:" + path

	# Get $HOME for user
	user_home = os.getenv("HOME")
	# A comment which can be added
	comment = "\n" + "\n" + "# Added by GroundMotionClassifer" + "\n"

	path = list(path)
	path.pop()
	path = ''.join(path)

	alt_string = "PROMPT_COMMAND='if [[ \"$bashrc\" != \"$PWD\" && \"$PWD\" != \"$HOME\" && -e .bashrc ]]; then bashrc=\"$PWD\"; . .bashrc; fi'"

	# Open .bashrc and write the comment and export PYTHONPATH
	bashrc = user_home + "/.bashrc"
	f = open(bashrc, 'a')
	f.write(comment)
	f.write(python_path_str)
	f.write("GMC_HOME=" + "\"" + path + "\"" + "\n")
	f.write(alt_string)
	f.close()

	print ("Updated.")

def install_dependencies():
	""" 
	Function to install all the dependecies in project

	Installs all the dependencies needed for the 
	application.
	
	Parameters
	----------

	Returns
	------- 
	None

	"""
	print ("Checking Dependencies...")

	try:
		# Tries importing the needed modules to check
		# if they are already installed.
		import numpy
		import scipy
		import matplotlib
		import peakutils
		import plotly
		import sklearn
		import pickle
		import obspy
	except ImportError:
		# Install dependencies in case importing is not possible.
		os.system('sudo apt-get install python-pip')
		os.system('sudo pip install numpy')
		os.system('sudo pip install scipy')
		os.system('sudo pip install matplotlib')
		os.system('sudo pip install peakutils')
		os.system('sudo pip install plotly')
		os.system('sudo pip install scikit-learn')
		os.system('sudo pip install pickle')
		os.system('sudo pip install obspy')

	print ("Installed all dependencies.")

def main():
	print ("Setting up GroundMotionClassifier...")
	path = update_config()
	update_bashrc(path)
	install_dependencies()
	print ("Done.")

if __name__ == "__main__":
	main()