#!bin/bash

# Run test_seismic_event
python tests/test_seismic_event.py

# If b -> exit otherwise continue
echo Press 'b' to end, any other key to continue, followed by ENTER:
read char

if [ "$char" == "b" ]; then
	exit 0
fi;

# Run test_seismic_event_features
python tests/test_seismic_event_features.py