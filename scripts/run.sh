#!bin/bash

# Program to find the feature vector for the classifier
# Author: VedangW

echo Beginning to form the feature vector...

# Home of project
project_home="/home/vedang/Desktop/isr_project"
cd $project_home

# Go to required folder 
destination="data/features"
cd $destination

# Clear all contents of all the files
> store.txt
> index.txt
> headers.txt

# Start by entering a particular directory and giving the access rights.

# Location 
path="/home/vedang/Desktop/isr_project/data/Kachchh"
files="/home/vedang/Desktop/isr_project/data/features/"
access_rights="r"

index="index.txt"
store="store.txt"
headers="headers.txt"

echo Searching in $path...

strones="pitsa001.00"
strtens="pitsa001.0"

space=" "
src="home/vedang/Desktop/isr_project/src"

cd $src

# For files 'pitsa001.001' to 'pitsa001.009'
for iter in `seq 1 9`;
do
	c=$strones$iter
	running="Analysing "
	echo $running$c
	var1="$(python rsp.py $path $c $access_rights)"
	var2="$(python complexity.py $path $c $access_rights $var1)"
	var5="$(python eventid.py $path $c $access_rights)"
	echo $var5 >> $files$headers
	if [ \( "$var2" != "inf" \) -a \( "$var2" != "nan" \) -a \( "$var2" != "-inf" \) -a \( "$var2" != "0.0" \) -a \( "$var2" != "-0.0" \) -a \( "$var2" != "N/A" \) ]
	then 
		var3="$(python sr.py $path $c $access_rights)"
		var4="$(python pe.py $var1 $var3 $var2)"
		reading=$var2$space$var4$space$var5
		echo $reading >> $files$store
		echo $iter >> $files$index
	fi
done

# For files 'pitsa001.010' to 'pitsa001.057'
for iter in `seq 10 57`;
do
	c=$strtens$iter
	running="Analysing "
	echo $running$c
	var1="$(python rsp.py $path $c $access_rights)"
	var2="$(python complexity.py $path $c $access_rights $var1)"
	var5="$(python eventid.py $path $c $access_rights)"
	echo $var5 >> $files$headers
	if [ \( "$var2" != "inf" \) -a \( "$var2" != "nan" \) -a \( "$var2" != "-inf" \) -a \( "$var2" != "0.0" \) -a \( "$var2" != "-0.0" \) -a \( "$var2" != "N/A" \) ]
	then 
		var3="$(python sr.py $path $c $access_rights)"
		var4="$(python pe.py $var1 $var3 $var2)"
		reading=$var2$space$var4$space$var5
		echo $reading >> $files$store
		echo $iter >> $files$index
	fi
done

# Location 
path="/home/vedang/Desktop/isr_project/data/Surendranagar"
access_rights="r"

echo Searching in $path...
cd $src

# For files 'pitsa001.001' to 'pitsa001.009'
for iter in `seq 1 9`;
do
	c=$strones$iter
	running="Analysing "
	echo $running$c
	var1="$(python rsp.py $path $c $access_rights)"
	var2="$(python complexity.py $path $c $access_rights $var1)"
	var5="$(python eventid.py $path $c $access_rights)"
	echo $var5 >> $files$headers
	if [ \( "$var2" != "inf" \) -a \( "$var2" != "nan" \) -a \( "$var2" != "-inf" \) -a \( "$var2" != "0.0" \) -a \( "$var2" != "-0.0" \) -a \( "$var2" != "N/A" \) ]
	then 
		var3="$(python sr.py $path $c $access_rights)"
		var4="$(python pe.py $var1 $var3 $var2)"
		reading=$var2$space$var4$space$var5
		echo $reading >> $files$store
		echo $iter + 57 >> $files$index
	fi
done

# For files 'pitsa001.010' to 'pitsa001.046'
for iter in `seq 10 46`;
do
	c=$strtens$iter
	running="Analysing "
	echo $running$c
	var1="$(python rsp.py $path $c $access_rights)"
	var2="$(python complexity.py $path $c $access_rights $var1)" 
	var5="$(python eventid.py $path $c $access_rights)"
	echo $var5 >> $files$headers
	if [ \( "$var2" != "inf" \) -a \( "$var2" != "nan" \) -a \( "$var2" != "-inf" \) -a \( "$var2" != "0.0" \) -a \( "$var2" != "-0.0" \) -a \( "$var2" != "N/A" \) ] 
	then 
		var3="$(python sr.py $path $c $access_rights)"
		var4="$(python pe.py $var1 $var3 $var2)"
		reading=$var2$space$var4$space$var5
		echo $reading >> $files$store
		echo $iter + 57 >> $files$index
	fi
done

echo Feature vector stored.