#!bin/bash

#Erase any data in headers.txt
> headers.txt

strones="pitsa001.00"
strtens="pitsa001.0"

path="/home/vedang/Desktop/PS/Datasets/Kachchh"

for iter in `seq 1 9`;
do
	c=$strones$iter
	statement="Storing header of "
	filename=$statement$c
	var1="$(python 0res_readheader.py $c $path)"
	echo $var1 > headers.txt
done

for iter in `seq 10 57`;
do
	c=$strtens$iter
	statement="Storing header of "
	filename=$statement$c
	var1="$(python 0res_readheader.py $c $path)"
	echo $var1 > headers.txt
done

path="/home/vedang/Desktop/PS/Datasets/Surendranagar"

for iter in `seq 1 9`;
do
	c=$strones$iter
	statement="Storing header of "
	filename=$statement$c
	var1="$(python 0res_readheader.py $c $path)"
	echo $var1 > headers.txt
done

for iter in `seq 10 57`;
do
	c=$strtens$iter
	statement="Storing header of "
	filename=$statement$c
	var1="$(python 0res_readheader.py $c $path)"
	echo $var1 > headers.txt
done