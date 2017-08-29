a = [['vedang w 1997 cs'], ['akash v 1997 mathcs'], ['manan p 1997 cs'], ['studshil p 1998 cs']]
flat_list = [item for sublist in a for item in sublist]
features = []
for x in flat_list:
	x = [i for i in x.split()]
	y = []
	y.append(x.pop(0))
	y.append(x.pop(0))
	string = ""
	for c in x:
		string = string + c + " "
	print x
	y.append(string)
	features.append(y)

print y
print features