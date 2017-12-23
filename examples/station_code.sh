> stations.txt

strones="pitsa001.00"
strtens="pitsa001.0"
path="Surendranagar"
space=" "

for iter in `seq 1 9`;
do
	c=$strones$iter
	var1="$(python Seismogram.py $path $c)"
	echo $iter$space$var1 >> stations.txt
done

#For files 'pitsa001.010' to 'pitsa001.046'
for iter in `seq 10 46`;
do
	c=$strtens$iter
	var1="$(python Seismogram.py $path $c)"
	echo $iter$space$var1 >> stations.txt
done
