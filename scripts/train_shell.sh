#!bin/bash

# Run read_events
python GMC/read_events.py

# If b -> exit otherwise continue
echo Press 'b' to end, any other key to continue, followed by ENTER:
read char

if [ "$char" == "b" ]; then
	exit 0
fi;

# Run store_data
python GMC/store_data.py

# If b -> exit otherwise continue
echo Press 'b' to end, any other key to continue, followed by ENTER:
read char

if [ "$char" == "b" ]; then
	exit 0
fi;

# Run fetch_data
python GMC/fetch_data.py

# If b -> exit otherwise continue
echo Press 'b' to end, any other key to continue, followed by ENTER:
read char

if [ "$char" == "b" ]; then
	exit 0
fi;

# Run train_model
python GMC/train_model.py
