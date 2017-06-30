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
	running="Running "
	echo $running$c
	var1="$(python P_S.py $path $c $access_rights)"
#	echo $var1 >> store.txt
	var2="$(python spectral.py $path $c $access_rights)"
	var3="$(python complexity.py $path $c $access_rights)"
	var4="$(python rms.py $path $c $access_rights)"
	reading=$var1$space$var2$space$var3$space$var4
	echo $reading >> store.txt
done

#For files 'pitsa001.010' to 'pitsa001.057'
for iter in `seq 10 57`;
do
	c=$strtens$iter
	running="Running "
	echo $running$c
	var1="$(python P_S.py $path $c $access_rights)"
#	echo $var1 >> store.txt
	var2="$(python spectral.py $path $c $access_rights)"
	var3="$(python complexity.py $path $c $access_rights)"
	var4="$(python rms.py $path $c $access_rights)"
	reading=$var1$space$var2$space$var3$space$var4
	echo $reading >> store.txt
done

#Location 
path="/home/vedang/Desktop/PS/Datasets/Surendranagar"
access_rights="r"

echo Searching in $path...

strones="pitsa001.00"
strtens="pitsa001.0"

space=" "

#For files 'pitsa001.001' to 'pitsa001.009'
for iter in `seq 1 9`;
do
	c=$strones$iter
	running="Running "
	echo $running$c
	var1="$(python P_S.py $path $c $access_rights)"
#	echo $var1 >> store.txt
	var2="$(python spectral.py $path $c $access_rights)"
	var3="$(python complexity.py $path $c $access_rights)"
	var4="$(python rms.py $path $c $access_rights)"
	reading=$var1$space$var2$space$var3$space$var4
	echo $reading >> store.txt
done

#For files 'pitsa001.010' to 'pitsa001.046'
for iter in `seq 10 46`;
do
	c=$strtens$iter
	running="Running "
	echo $running$c
	var1="$(python P_S.py $path $c $access_rights)"
#	echo $var1 >> store.txt
	var2="$(python spectral.py $path $c $access_rights)"
	var3="$(python complexity.py $path $c $access_rights)"
	var4="$(python rms.py $path $c $access_rights)"
	reading=$var1$space$var2$space$var3$space$var4
	echo $reading >> store.txt
done

echo All finished.