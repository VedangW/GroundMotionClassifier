#!bin/bash

#Program to find the feature vector for the classifier
#Author: VedangW

echo Beginning to form the feature vector...
#Clear all contents of all the files
> store.txt 
> index1.txt
> index2.txt
> headers.txt

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
	var2="$(python complexity.py $path $c $access_rights $var1)"
	echo $var5 >> headers.txt
	var5="$(python eventid.py $path $c $access_rights)"
	if [ \( "$var2" != "inf" \) -a \( "$var2" != "nan" \) -a \( "$var2" != "-inf" \) -a \( "$var2" != "0.0" \) -a \( "$var2" != "-0.0" \) -a \( "$var2" != "N/A" \) ]
	then 
		var3="$(python sr.py $path $c $access_rights)"
		var4="$(python pe.py $var1 $var3 $var2)"
		reading=$var2$space$var4$space$var5
		echo $reading >> store.txt
		echo $iter >> index1.txt

	fi
done

#For files 'pitsa001.010' to 'pitsa001.057'
for iter in `seq 10 57`;
do
	c=$strtens$iter
	running="Analysing "
	echo $running$c
	var1="$(python rsp.py $path $c $access_rights)"
	var2="$(python complexity.py $path $c $access_rights $var1)"
	var5="$(python eventid.py $path $c $access_rights)"
	echo $var5 >> headers.txt
	if [ \( "$var2" != "inf" \) -a \( "$var2" != "nan" \) -a \( "$var2" != "-inf" \) -a \( "$var2" != "0.0" \) -a \( "$var2" != "-0.0" \) -a \( "$var2" != "N/A" \) ]
	then 
		var3="$(python sr.py $path $c $access_rights)"
		var4="$(python pe.py $var1 $var3 $var2)"
		reading=$var2$space$var4$space$var5
		echo $reading >> store.txt
		echo $iter >> index1.txt
	fi
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
	var2="$(python complexity.py $path $c $access_rights $var1)"
	var5="$(python eventid.py $path $c $access_rights)"
	echo $var5 >> headers.txt
	if [ \( "$var2" != "inf" \) -a \( "$var2" != "nan" \) -a \( "$var2" != "-inf" \) -a \( "$var2" != "0.0" \) -a \( "$var2" != "-0.0" \) -a \( "$var2" != "N/A" \) ]
	then 
		var3="$(python sr.py $path $c $access_rights)"
		var4="$(python pe.py $var1 $var3 $var2)"
		reading=$var2$space$var4$space$var5
		echo $reading >> store.txt
		echo $iter >> index2.txt
	fi
done

#For files 'pitsa001.010' to 'pitsa001.046'
for iter in `seq 10 46`;
do
	c=$strtens$iter
	running="Analysing "
	echo $running$c
	var1="$(python rsp.py $path $c $access_rights)"
	var2="$(python complexity.py $path $c $access_rights $var1)" 
	var5="$(python eventid.py $path $c $access_rights)"
	echo $var5 >> headers.txt
	if [ \( "$var2" != "inf" \) -a \( "$var2" != "nan" \) -a \( "$var2" != "-inf" \) -a \( "$var2" != "0.0" \) -a \( "$var2" != "-0.0" \) -a \( "$var2" != "N/A" \) ] 
	then 
		var3="$(python sr.py $path $c $access_rights)"
		var4="$(python pe.py $var1 $var3 $var2)"
		reading=$var2$space$var4$space$var5
		echo $reading >> store.txt
		echo $iter >> index2.txt
	fi
done

echo Feature vector stored.