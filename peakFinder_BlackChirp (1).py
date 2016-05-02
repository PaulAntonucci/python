#!/usr/bin/python3
#coding -*-coding:Utf-8 -*

# Import
import sys # basic files tools
from matplotlib.pyplot import *
import numpy
from math import floor, sqrt, exp, ceil
from scipy import signal
from bisect import bisect_left


#########################################################
# BODY OF THE PROGRAM
#########################################################

#------------------------------------
# Parameters
#------------------------------------

# Points for the truncated FID
fid_ini_pt = 269998

# Frequency range of the FFT in MHz
fft_ini_freq = 6500
fft_end_freq = 19500

#Noise shift
noise_shift = 0
shift_1 = 0.0012
shift_2 = 0.0010
shift_3 = 0.0007

#Points for smooth
# Use of 2 different points to find all the lines
smooth_pt1 = 20
smooth_pt2 = 200


#------------------------------------
# Input file and reading of the file
#------------------------------------
# Input file
if len(sys.argv) != 2:
    print('Usage: peakfinder.py spectrum_file')
    exit(1)

spectrum_name = sys.argv[1]
file_name, ext = sys.argv[1].split('.')

if ('fid' in file_name):
    file_name = file_name.split('_')[0]

while True:
    try:
        n_pzf = int(input("Please enter a pzf number (>0): "))
        if (n_pzf > 0):
            break
        else:
            print("Oops!  That was no valid number.  Try again...")
    except ValueError:
        print("Oops!  That was no valid number.  Try again...")

print()

#--------------------------------------------------------------------
# Read the spectrum file
#--------------------------------------------------------------------

# 
with open(spectrum_name, 'r') as spectrum_file:
    spectrum_lines = spectrum_file.read().splitlines()

#Find informations in the headline
for i in range(len(spectrum_lines)):  
    #Find the sample rate and calculate the step
    if "#Spacing" in spectrum_lines[i]:
        step = float(spectrum_lines[i].split('\t')[1])
    #Find the beginning of the FID
    if "fid" in spectrum_lines[i]:
        fid_ini = i+1
    #Find the end of the FID
    if("#Shots" in spectrum_lines[i]):
        shots = spectrum_lines[i].split()[1]
        shots = int(shots)        
    #Determine the sideband
    if "#Sideband" in spectrum_lines[i]:
        sideband = spectrum_lines[i].split('\t')[1]
    if "#Probe freq" in spectrum_lines[i]:
        probe_freq = float(spectrum_lines[i].split()[2])

fid_end = len(spectrum_lines)-1

#---------------------------------------------------
# SCREEN INFORMATIONS
#---------------------------------------------------

print('File:', spectrum_name)
print('Number of shots:', shots, '\n')

#--------------------------------------------------------------------
# FID to FFT
#--------------------------------------------------------------------

time_fid=-step
time_list=[]
int_list_fid=[]
#Read the FID and calculate the time
for i in range(fid_ini,fid_end):
    int_fid = spectrum_lines[i]
    int_list_fid.append(float(int_fid))
    time_fid = time_fid + step
    time_list.append(float(time_fid))

del(spectrum_lines)

len_fid_ini = len(int_list_fid)

# Screen infos
print('Initial length of the FID:', len_fid_ini)
print('Initial length of the time list:', len(time_list))
  
# FID to FFT:
#Correction of the offset
somme = 0
for i in range (fid_ini_pt,len_fid_ini):
    somme += float(int_list_fid[i])
moyenne = somme / (len_fid_ini - fid_ini_pt)
for i in range (len(int_list_fid)):
    int_list_fid[i] -= moyenne
    # numpy mean useful here

# With apodisation
int_list_fid_arr = numpy.array(int_list_fid) * signal.blackmanharris(len(int_list_fid))
int_list_fid = list(int_list_fid_arr)
del(int_list_fid_arr)
    
# Postzero-padding (stop at the closest multiple of 100 and power of two (lower value)
fid_pzf_length = int ((floor(sqrt((len_fid_ini - fid_ini_pt -1) * n_pzf)))**2)

for i in range(len_fid_ini,fid_pzf_length + fid_ini_pt):
    int_list_fid.append(0)
    time_fid = time_fid + step
    time_list.append(float(time_fid))
    # numpy zero and numpy linspace
    
del(time_fid)

# Screen infos    
print('Length of the PZF FID:', len(int_list_fid))
print('Length of the PZF time list:', len(time_list), '\n')

int_list_fid_trunc=[]  
#   Creation of a truncated list
int_list_fid_trunc = int_list_fid[fid_ini_pt:fid_pzf_length + fid_ini_pt]
print('Truncature length of the PZF FID:', len(int_list_fid_trunc))

# Convert into numpy array
int_list_fid_trunc = numpy.array(int_list_fid_trunc)

# FFT
int_list_fft = numpy.fft.rfft(int_list_fid_trunc)
magnitude = numpy.absolute(int_list_fft)

del(int_list_fid_trunc)

freq_list = []
# Determine the frequencies in MHz
for i in range(len(int_list_fft)):
    if sideband == "Upper":
        freq = probe_freq + i /(2* len(int_list_fft) * step) * 1e-6
        freq_list.append(freq)
    else:
        freq = probe_freq - i /(2* len(int_list_fft) * step) * 1e-6
        freq_list.append(freq)
        
del(int_list_fft)


#---------------------------------------------------
# SMOOTH FUNCTION 1
#---------------------------------------------------

n_smooth1= smooth_pt1 * n_pzf
n_smooth_test1= ceil(smooth_pt1 * n_pzf)
magn_smooth_list1 = list(magnitude)
smooth_test1 = list(magnitude)

for i in range(n_smooth1,len(magnitude)-n_smooth1):
    value = magnitude[i] - 0.5 * numpy.mean(magnitude[i-n_smooth1:i+n_smooth1]) 
    magn_smooth_list1[i] = value
    if (freq_list[i] < 16300):
        smooth_test1[i] = numpy.mean(magnitude[i-n_smooth_test1:i+n_smooth_test1]) + shift_1
    elif  (16300 < freq_list[i] < 17000):
        smooth_test1[i] = numpy.mean(magnitude[i-n_smooth_test1:i+n_smooth_test1]) + shift_2
    else:
        smooth_test1[i] = numpy.mean(magnitude[i-n_smooth_test1:i+n_smooth_test1]) + shift_3
del(value)

#---------------------------------------------------
# SMOOTH FUNCTION 2
#---------------------------------------------------

n_smooth2= smooth_pt2 * n_pzf
n_smooth_test2= ceil(smooth_pt2 * n_pzf)
magn_smooth_list2 = list(magnitude)
smooth_test2 = list(magnitude)

for i in range(n_smooth2,len(magnitude)-n_smooth2):
    value = magnitude[i] - 0.5 * numpy.mean(magnitude[i-n_smooth2:i+n_smooth2]) 
    magn_smooth_list2[i] = value
    if (freq_list[i] < 16300):
        smooth_test2[i] = numpy.mean(magnitude[i-n_smooth_test2:i+n_smooth_test2]) + shift_1
    elif  (16300 < freq_list[i] < 17000):                                           
        smooth_test2[i] = numpy.mean(magnitude[i-n_smooth_test2:i+n_smooth_test2]) + shift_2
    else:                                                                           
        smooth_test2[i] = numpy.mean(magnitude[i-n_smooth_test2:i+n_smooth_test2]) + shift_3

del(value)

#---------------------------------------------------
# PEAK DETECTION
#---------------------------------------------------

local_max = 0
lower_limit = 0.2
peak_int_list = []
peak_int_fig = []
peak_freq_list = []
noise_level = []

for i in range(1,len(magn_smooth_list1)-1):
    if (magn_smooth_list1[i-1] < magn_smooth_list1[i] > magn_smooth_list1[i+1] and magn_smooth_list1[i] > smooth_test1[i] and fft_ini_freq < freq_list[i] < fft_end_freq): 
        local_max = magn_smooth_list1[i]
        
        peak_int_list.append(magnitude[i])
        peak_int_fig.append(magnitude[i] + lower_limit)
        peak_freq_list.append(freq_list[i])
        noise_level.append(smooth_test2[i])


del(local_max)

for i in range(1,len(magn_smooth_list2)-1):
    if (magn_smooth_list2[i-1] < magn_smooth_list2[i] > magn_smooth_list2[i+1] and magn_smooth_list2[i] > smooth_test2[i] and fft_ini_freq < freq_list[i] < fft_end_freq): 
        local_max = magn_smooth_list2[i]
        
        if (freq_list[i] not in peak_freq_list):
            peak_int_list.append(magnitude[i])
            peak_int_fig.append(magnitude[i] + lower_limit)
            peak_freq_list.append(freq_list[i])
            noise_level.append(smooth_test2[i])


del(local_max)

#---------------------------------------------------
# EXPORT FILE
#---------------------------------------------------

n_pzf = str(n_pzf)
#Spacing between two frequencies
sampling = freq_list[1] - freq_list[0]

#export the graph
with open('CP' + file_name + '_pzf' + n_pzf + '.sp', 'w') as sp_file:
    for i in range(len(magnitude)):  
        if (fft_ini_freq < freq_list[i] < fft_end_freq):
            sp_file.write('%5.3f %5.5f\n' %(freq_list[i], magnitude[i]))

#export the linelist
with open('CP' + file_name + '_pzf' + n_pzf + '.lines', 'w') as linelist_file:
    for i in range(len(peak_freq_list)):
        linelist_file.write('%9.3f %7.4f %7.4f %7.3f\n' %(peak_freq_list[i], peak_int_list[i], noise_level[i], ceil((0.3 / (2*peak_int_list[i]/noise_level[i])+ sampling/2) *200)/200)  )

#---------------------------------------------------
# SCREEN INFORMATIONS
#---------------------------------------------------

print('Spectral range:', fft_ini_freq, '-', fft_end_freq, ' MHz' )
print('Frequency step: %5.3f MHz' %(sampling))
print('Number of peaks:', len(peak_int_list) )


#---------------------------------------------------
# PLOT 
#(only for small pzf values, to avoid memory errors)
#---------------------------------------------------

if (int(n_pzf) < 16):
    figure(1) # creation of a figure
    
    #FID
    subplot(211) # 3 graphs, one column, line 1
    title ('FID and selected range for FFT')
    ion() #interactive mode
    plot(time_list,int_list_fid)
    vlines(time_list[fid_ini_pt], min(int_list_fid), max(int_list_fid), linewidth=3, colors='red')
    vlines(time_list[len_fid_ini-1], min(int_list_fid), max(int_list_fid), linewidth=3, colors='red', linestyle = '--')
    vlines(time_list[fid_ini_pt + fid_pzf_length-1], min(int_list_fid), max(int_list_fid), linewidth=3, colors='red')
    
    #FFT and peaks
    subplot(212) 
    title ('FFT spectrum and peaks')
    plot(freq_list, magnitude) 
    #plot(freq_list, magn_smooth_list1) 
    #plot(freq_list, magn_smooth_list2) 
    plot(freq_list, smooth_test1, color='red') 
    plot(freq_list, smooth_test2, color='orange') 
    if (len(peak_int_list) != 0):
        #vlines(peak_freq_list, 1e-6, peak_int_list, colors='red', linestyle = '--')
        bar(peak_freq_list, peak_int_fig, width=0.001, bottom =-lower_limit, edgecolor='red')
    xlim(xmin=fft_ini_freq, xmax=fft_end_freq)
    
    show(block=True)
