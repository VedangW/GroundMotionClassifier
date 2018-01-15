import os
import config
from obspy import read

print ("Locating events in the data directory...")

data_home = config.project_home + "/data/"
sub_dirs = next(os.walk(data_home))[1]

all_events = []
all_labels = []

# Enter each directory and retrieve its events and labels
mininmum = []
for d in sub_dirs:
	print("Entering directory ", d, "...")
	path = data_home + d
	for file in os.listdir(path):
		print ("Processing ", file)
		path_ = path + "/" + file
		st = read(path_)
		dat = st[0].data
		m = min(dat)
		mininmum.append(m)

v = min(mininmum)
print (v)

# 8400000