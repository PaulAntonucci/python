#!/usr/bin/python3
#coding -*-coding:Utf-8 -*
# Import
import sys # basic files tools
import numpy as np
from math import ceil



# Takes a peak list (from the CP) and creates a ftb file for the categorize mode

#########################################################
# BODY OF THE PROGRAM
#########################################################


#------------------------------------
# Input file and reading of the file
#------------------------------------
# Input file
if len(sys.argv) != 2:
    print('Usage: peak2cat.py peak_file')
    exit(1)

peak_name = sys.argv[1]
file_name, ext = sys.argv[1].split('.')


#--------------------------------------------------------------------
# Read the peak file
# and an array with a list of frequencies and intensities
# and a transpose of this array as the initial list of remaining peaks
#--------------------------------------------------------------------

with open(peak_name, 'r') as peak_file:
    peak_lines = peak_file.read().splitlines()

peak_freq = []
peak_int = []

for i in range(len(peak_lines)):
    freq = peak_lines[i].split()[0]
    intensity = peak_lines[i].split()[1]
    peak_freq.append(float(freq))
    peak_int.append(float(intensity))

print(str(len(peak_int)) + ' peaks')

peak_array = np.array( [peak_freq, peak_int] ).transpose()
peak_array = peak_array[peak_array[:, 1].argsort()[::-1]]
# the list is here sorted by decreasing intensities

del(peak_lines, peak_freq, peak_int)



#---------------------------------------------------
# EXPORT FILE
#---------------------------------------------------

# Export a batch file with frequencies in MHz
with open('1_peak2cat_' + file_name + '.ftb', 'w') as out_file:
    
    for i in range(len(peak_array)):
        # define the number of shots as a function of the intensity
        n_shots = ceil(2 / (5 * peak_array[i,1])) 
        if (n_shots < 10):
            n_shots = 10
        
        out_file.write('ftm:%5.3f shots:%1s dipole:1.0 drpower:-20 drfreq:1000.000\n' %(peak_array[i,0], n_shots))
