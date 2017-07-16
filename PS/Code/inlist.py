#!usr/bin/python

import os
import pandas
import sys

def main():
	fl = open('store.txt', 'r')
	lines = fl.readlines()
	print "No. of data points = ", len(lines)

	flist = pandas.read_csv('store.txt', header=None).values
	print flist

if __name__ == "__main__":
	main()