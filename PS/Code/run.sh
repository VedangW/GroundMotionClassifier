#!bin/bash

#Program to find the feature vector for the classifier
echo Beginning to form the feature vector...
#Clear all contents of the file
> store.txt 

#Start by entering a particular directory and giving the access rights.

#Location 
path="/home/vedang/Desktop/PS/Datasets/Kachchh"
access_rights="r"

echo Searching in $path...

strones="pitsa001.00"
strtens="pitsa001.0"

space=" "

#For files 'pitsa001.001' to 'pitsa001.009'
for iter in `seq 1 9`;
do
	c=$strones$iter
	running="Analysing "
	echo $running$c
	var1="$(python rsp.py $path $c $access_rights)"
	var2="$(python sr.py $path $c $access_rights)"
	var3="$(python complexity.py $path $c $access_rights $var1)"
	var4="$(python pe.py $var1 $var2 $var3)"
	reading=$var1$space$var4
	echo $reading >> store.txt
done

#For files 'pitsa001.010' to 'pitsa001.057'
for iter in `seq 10 57`;
do
	c=$strtens$iter
	running="Analysing "
	echo $running$c
	var1="$(python rsp.py $path $c $access_rights)"
	var2="$(python sr.py $path $c $access_rights)"
	var3="$(python complexity.py $path $c $access_rights $var1)"
	var4="$(python pe.py $var1 $var2 $var3)"
	reading=$var1$space$var4
	echo $reading >> store.txt
done

#Location 
path="/home/vedang/Desktop/PS/Datasets/Surendranagar"
access_rights="r"

echo Searching in $path...

#For files 'pitsa001.001' to 'pitsa001.009'
for iter in `seq 1 9`;
do
	c=$strones$iter
	running="Analysing "
	echo $running$c
	var1="$(python rsp.py $path $c $access_rights)"
	var2="$(python sr.py $path $c $access_rights)"
	var3="$(python complexity.py $path $c $access_rights $var1)"
	var4="$(python pe.py $var1 $var2 $var3)"
	reading=$var1$space$var4
	echo $reading >> store.txt
done

#For files 'pitsa001.010' to 'pitsa001.046'
for iter in `seq 10 46`;
do
	c=$strtens$iter
	running="Analysing "
	echo $running$c
	var1="$(python rsp.py $path $c $access_rights)"
	var2="$(python sr.py $path $c $access_rights)"
	var3="$(python complexity.py $path $c $access_rights $var1)"
	var4="$(python pe.py $var1 $var2 $var3)"
	reading=$var1$space$var4
	echo $reading >> store.txt
done

echo Feature vector stored.