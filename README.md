## isrsvm
A project to differentiate between earthquakes and blasting waves using Support Vector Machines.

#Prerequisites:
To run this project, you would need a linux-based operating system (Ubuntu or Fedora would work best).

The code is written in Python 2.7.12+, but any version of Python 2 would work. 

You would also need the following downloaded in your system:
- Scipy
- Numpy
- Matplotlib
- Scikit-Learn

#Running the code:
The feature vector is stored in store.txt present in isrsvm/PS/Code.
To create a new feature vector (while erasing the previous one):
```
sh run.sh
```
To test the working of any module, you can simply compile it with Python 2, for eg.:
```
python Seismogram.py
```
or
```
python P_S.py
```

#Datasets:
The datasets are present in isrsvm/PS/Datasets.


