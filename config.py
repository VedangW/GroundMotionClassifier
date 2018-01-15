# Config file for the project
project_home = '/home/vedang/Desktop/gmc'

### HYPER-PARAMETERS

## Hyper-parameters for feature calculations

# Limiting ratio for p waves in S/P ratio calculation
p_lim_ratio = 2.5
# Limiting ratio for s waves in S/P ratio calculation
s_lim_ratio = 3.58

# Higher frequency band for spectral ratio
sr_lh = [11, 15]
# Lower frequency band for spectral ratio
sr_ll = [1, 10]

# Lower amount of number of seconds from p wave
# for calculating complexity
comp_lv = 3
# Higher amount of number of seconds from p wave
# for calculating complexity
comp_hv = 7

## For train-validation-test breaking

# Train percentage
train_ratio = 0.6
# Validation percentage
validation_ratio = 0.2
# Test percentage
test_ratio = 0.2

# For dev/test set
cl_kachchh = 10
ch_kachchh = 15

cl_sur = 8
ch_sur = 10