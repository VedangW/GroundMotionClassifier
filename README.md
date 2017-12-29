# GroundMotionClassifier
A project to differentiate between earthquakes and blasting waves using Support Vector Machines.

## Prerequisites:

To run this project, you would need a linux-based operating system (Ubuntu or Fedora would work best).

The code is written in Python 2.7.12+, but any version of Python 2 would work. 

You would also need the following installed in your system:
- Scipy
- Numpy
- Matplotlib
- Scikit-Learn
- Peakutils
- Plotly

These can be downloaded using a download manager such as pip. 

Install pip:
```
sudo apt-get install python-pip
```
Install any of the dependencies with pip. For eg,:
```
pip install scikit-learn
pip install numpy
```

## Running the code:

The feature vector is stored in store.txt present in isrsvm/PS/Code.
To create a new feature vector (while erasing the previous one):
```
sh run.sh
```
To test the working of any module, you can simply compile it with Python 2 with the appropriate command-line arguments.
Check in the comments in the relevant file to know the command-line arguments. For eg.:
```
python Seismogram.py Kachchh pitsa001.044
python rsp.py /path/to/PS/Datasets/Surendranagar pitsa001.003 r
```
To train the classifier and plot the decision boundary along with the scatterplot, compile the classifier file.
This however should be done after creating the feature vector:
```
python classifier.py
```

## Datasets:

The datasets are present in isrsvm/PS/Datasets.

#### Note: These datasets are owned by the Institute of Seismological Research, Gandhinagar, India.


