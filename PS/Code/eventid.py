#!usr/bin/python

""" File for finding the event id of a particular Seismogram object
	Filename, path, access rights given as command line parameters.

	Author: VedangW
"""
import os
import sys
from Seismogram import Seismogram

def main():
	smg = Seismogram(sys.argv[1], sys.argv[2], sys.argv[3])
	print smg.get_event_id()

if __name__ == "__main__":
	main()