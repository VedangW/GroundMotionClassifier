#!usr/bin/python

""" Resource file to store the headers of the files
	into another file, header.txt.
"""
import os
import sys

#sys.argv[1] = name of file
def main():
	path = sys.argv[2]
	os.chdir(path)

	f = open(sys.argv[1], 'r')
	lines = f.readlines()

	header_string = lines[0]
	print header_string

if __name__ == "__main__":
	main()