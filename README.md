# GroundMotionClassifier
A project to differentiate between earthquakes and blasting waves using Machine Learning.

## Prerequisites:

GMC is written with python3. Run ```scripts/setup.py``` to install any dependencies and setup the environment:

```bash
	cd /path/to/gmc/
	python scripts/setup.py
```

## Running the code:

#### Preprocessing of data (only needed if new data):

#### Training the model:

Run train_model.py in ```gmc/GMC/```:

```bash
	gmc train
```

The weights are now stored in ```model.pkl```.

#### Prediction on model:

Run predict.py in ```gmc/GMC/```:

```bash
	python predict.py z_file n_file e_file
```

Where ```z_file```, ```n_file``` and ```e_file``` are paths to the z, n and e compoments of the event to be predicted. 



