#!/usr/bin/python3
#coding -*-coding:Utf-8 -*

# Import
import sys # basic files tools
from matplotlib.pyplot import *
from mpl_toolkits.axes_grid1.axes_rgb import make_rgb_axes, RGBAxes
import numpy as np
from math import *
import time

# Yes, they really are
# VARIABLES GLOBAL to the Module

# in getFileName
spectrum_name = 'FromMarie/CP99_pzf1.sp'
file_name = 'FromMarie/CP99_pzf1'
known_freq_name = 'FromMarie/artifacts.cat'
known_name = 'artifacts'
ext = 'cat'
factor = 1

# in readSpectrumAndLineFiles
freq_list_ini = []
int_list_ini = []
step = 1.0

peak_freq_ini = []
peak_int_ini = []
peak_unc_ini = []
peak_array = np.array( [peak_freq_ini, peak_int_ini, peak_unc_ini] )


# in readKnownFile
known_freq_array = []

#in peak_assignment
match_freq = []
match_int = []

# in createListOfPeaks
match_peak_array = []
peak_freq_end = []
peak_int_end = []
peak_unc_end = []
peak_freq_assign = []
peak_int_assign = []
peak_unc_assign = []

#in ClearSpectrum
freq_list_assign = []
int_list_end = []
freq_list_end = []
int_list_assign = []
bucket = []
bucketedLines = []


def clearVariables():       # This clears the variables necessary for re-doing "remove molecular lines"
                            # IT does NOT remove the variables necessary for opening a new file, or creating a new FFT
    global known_freq_array; global match_freq;     global match_int;
    global match_peak_array; global peak_freq_end;  global peak_int_end; global peak_unc_end;
    global peak_freq_assign; global peak_int_assign; global peak_unc_assign;
    global freq_list_assign; global int_list_end;   global freq_list_end; global int_list_assign

    # del known_freq_array[:] - set to an np.array
    # in peak_assignment
    del match_freq[:]
    del match_int[:]
    
    # in createListOfPeaks
    # del match_peak_array[:] - set to an np.array
    del peak_freq_end[:]
    del peak_int_end[:]
    del peak_unc_end[:]
    del peak_freq_assign[:]
    del peak_int_assign[:]
    del peak_unc_assign[:]
    #in ClearSpectrum
    del freq_list_assign[:]
    del int_list_end[:]
    del freq_list_end[:]
    del int_list_assign[:]



#########################################################
# BODY OF THE PROGRAM
#########################################################

#------------------------------------
# Input file and reading of the file
#------------------------------------
# Input file

def getFileName():
    global spectrum_name;   global file_name;   global known_freq_name
    global known_name;      global ext;         global factor
    if len(sys.argv) != 3:
        print('Usage: ClearSpectrum.py spectrum_file known_freq_file')
        exit(1)
    # The script needs 3 input files :
    # the experimental spectrum;
    # the peak list with the same name than the experimental spectrum, and the extension'.lines';
    # a file containing a list of known frequencies

    # The peak list can contain as many column as desired.
    # However, the frequency should be in the first column,
    # and the intensity in the second

    # In order to have the output files name correctly,
    # please respect these few pre-requisites:
    # the experimental spectrum should possess an extension
    # the known frequency file should possess an extension
    # and be placed in a subfolder.
    # It should contain in its first column the frequency, and
    # on the third the intensity in Pickett's format (log(int))

    spectrum_name = sys.argv[1]
    file_name = sys.argv[1].split('.')[0]

    known_freq_name = sys.argv[2]
    known_name, ext = sys.argv[2].split('.')

    if ('/' in known_name):
        known_name = known_name.split('/')[1]

    factor = 1
    if ('artifacts' in known_name):
        factor = 2

#--------------------------------------------------------------------
# Read the spectrum file
# and create a list of frequencies, and a list of intensities
#--------------------------------------------------------------------
def readSpectrumAndLineFiles():
    global freq_list_ini;   global int_list_ini
    global peak_freq_ini;   global peak_int_ini;    global peak_unc_ini;
    global peak_array;      global step
    global bucket;          global bucketedLines;
    
    with open(spectrum_name, 'r') as spectrum_file:
        spectrum_lines = spectrum_file.read().splitlines()

    del freq_list_ini[:]
    del int_list_ini[:]
    del bucket[:]
    del bucketedLines[:]

    for i in range(len(spectrum_lines)):
        if (len(spectrum_lines[i])>1):
            freq_ini, int_ini = spectrum_lines[i].split()
            freq_list_ini.append(float(freq_ini))
            int_list_ini.append(float(int_ini))
        #else:
        #    freq_list_ini.append(freq_list_ini[i-1])
        #    int_list_ini.append(-0.0001)

    del(spectrum_lines)

    step = freq_list_ini[1] - freq_list_ini[0]

    #--------------------------------------------------------------------
    # Read the peak file
    # and an array with a list of frequencies and intensities
    # and a transpose of this array as the initial list of remaining peaks
    #--------------------------------------------------------------------

    with open(file_name + '.lines', 'r') as peak_file:
        peak_lines = peak_file.read().splitlines()

    del peak_freq_ini[:]
    del peak_int_ini[:]
    del peak_unc_ini[:]
    
    for i in range(len(peak_lines)):
        peak_freq = peak_lines[i].split()[0]
        peak_int = peak_lines[i].split()[1]
        peak_freq_ini.append(float(peak_freq))
        peak_int_ini.append(float(peak_int))
        peak_unc = peak_lines[i].split()[2]
        peak_unc_ini.append(float(peak_unc))

    lines_ini_length = str(len(peak_int_ini))

    print(lines_ini_length + ' initial experimental frequencies')

    peak_array = np.array( [peak_freq_ini, peak_int_ini, peak_unc_ini] )
    

    #--------------------------------------------------------------------
    # Read the known freq file
    # Create a list and an array of known frequencies
    #--------------------------------------------------------------------
def readKnownFile():
    global known_freq_array
    global known_name; global ext; global factor
    with open(known_freq_name, 'r') as known_freq_file:
        known_freq_lines = known_freq_file.read().splitlines()
        
    known_freq_list = []
    known_freq_int = []

    known_name, ext = known_freq_name.split('.')
    print("known name = " + known_name)
    if ('/' in known_name):
        known_name = known_name.split('/')[1]
    factor = 1
    if ('artifacts' in known_name):
        factor = 2  
    #print("Number of Lines = " + str(len(known_freq_lines)))
    
    for i in range(len(known_freq_lines)):
        #if(known_name == "h2c6"):
        #    print ("i:", i)
        #    print (known_freq_lines[i])
        # print("i = " + str(i))
        # print("string = "+ known_freq_lines[i])
        known_freq  = known_freq_lines[i].split()[0]
            
        if (ext == 'list'): # case of just a frequency list
            known_int  = -1
        elif (ext == "lines"):   #PRAA Mar 29 2016
            known_int  = -1    
        else :
            known_int  = known_freq_lines[i].split()[2]
            
        if (freq_list_ini[0] < float(known_freq) < freq_list_ini[-1]):        
            if (ext == 'mrg'):
                seen_freq = known_freq_lines[i].split()[5]
                try:
                    seen_freq = float(seen_freq)
                except ValueError: #only if the sixth column is not an interger == only if the column has a '-' sign == experimental frequency
                    known_freq_list.append(float(known_freq))
                    known_freq_int.append(10**float(known_int))            
            else:
                known_freq_list.append(float(known_freq))
                known_freq_int.append(10**float(known_int))
                
    del(known_freq_lines)   
        
    known_freq_array = np.array( [known_freq_list, known_freq_int] ).transpose()
    known_freq_array = known_freq_array[known_freq_array[:, 1].argsort()[::-1]]
        # the list is here sorted by decreasing intensities

    del(known_freq_list, known_freq_int)


#---------------------------------------------------
# PEAK ASSIGNMENT
# Compare the list of experimental peaks
# and the list of known frequencies to find matches
#---------------------------------------------------

def peakAssignment(doNotPlot):
    global match_freq 
    global match_int
    index_list = []
    match_unc = []

    # Initialize a counter for matches
    counter = 0
    del match_freq[:]
    del match_int[:]
    del match_unc[:]

    for i in range(len(known_freq_array)):          # PRAA note that peak_array[0] is a column of frequencies
        min_freq = np.abs(known_freq_array[i,0] - peak_array[0])    # PRAA note that min_freq is an array
        index = np.argmin(min_freq)
        #print("I, index, freq ", str(i), str(index), known_freq_array[i,0])
        
        if (min_freq[index] < 0.2):
            #append the match list, and remove items from the remaining peaks array
            print("index= "+ str(index))
            print("peak_array[0, index] = " + str(peak_array[0, index]))
            match_freq.append(peak_array[0,index])
            match_int.append(peak_array[1,index])
            match_unc.append(peak_array[2,index])
            index_list.append(index)
            counter += 1

        # Exit the script if counter < i for the 3 strongest predicted lines
        if (counter - i < 0 and 0 < i < 1 and (doNotPlot == False)):
            print('No plausible line of ' + known_name + ' in the spectrum')
            
            #---------------------------------------------------
            # PLOT
            #---------------------------------------------------
            
            figure(2) # creation of a figure
            #
            # Known frequencies
            subplot(211) #
            title ('Known frequencies: ' + known_name)
            ion() #interactive mode
            xlim([freq_list_ini[0], freq_list_ini[-1]])
            vlines(known_freq_array[:,0], 1e-10, known_freq_array[:,1], colors='red')
            #
            # Initial spectrum in the background, Cleared spectrum in the front
            subplot(212, sharex=subplot(211)) 
            title ('Initial spectrum (red), Cleared spectrum (blue)')
            plot(freq_list_ini,int_list_ini)
            #
            show(block=True)
            sys.exit()
            
          
        del(index)

    if ((counter == 0) and (doNotPlot == False)):
        print('No plausible line of ' + known_name + ' in the spectrum')
        
        #---------------------------------------------------
        # PLOT
        #---------------------------------------------------
        
        figure(2) # creation of a figure
        #
        # Known frequencies
        subplot(211) #
        title ('Known frequencies: ' + known_name)
        ion() #interactive mode
        xlim([freq_list_ini[0], freq_list_ini[-1]])
        vlines(known_freq_array[:,0], 1e-10, known_freq_array[:,1], colors='red')
        #
        # Initial spectrum in the background, Cleared spectrum in the front
        subplot(212, sharex=subplot(211)) 
        title ('Initial spectrum (red), Cleared spectrum (blue)')
        plot(freq_list_ini,int_list_ini)
        # Remove the following two lines for testing Feb 9 2016 praa
        # show(block=True)
        show(block=False)
        # sys.exit()
        time.sleep(2)
        print(" finished with this task, and sleeping for 2 seconds")
    return(counter)

#---------------------------------------------------
# Creation of a reduce list of peaks
# And a list of assigned peaks
#---------------------------------------------------

def createListsOfPeaks():
    # Remove multiple occurences in index_list
    # and sort by decreasing values (allow to delete)
    global  match_freq
    global  peak_array
    global  match_peak_array
    
    #index_list = list(set(index_list))
    #index_list.sort(reverse=True)
    #
    #peak_lines_end = list(peak_lines)
    global  peak_freq_end
    global  peak_int_end 
    global  peak_unc_end 
    global  peak_freq_assign
    global  peak_int_assign
    global  peak_unc_assign
    global  bucket
    global  bucketedLines

    #peaks_assigned = []

    # remove the assigned peak + those that are too close (in the cleaning window)
    # print(str(peak_freq_ini))
    for i in range(len(peak_freq_ini)):
        counter = 0
        for j in range(len(match_freq)):
            if (abs(match_freq[j]-peak_freq_ini[i]) < (5.2 - 4.97 * 0.41**(match_int[j])) *factor):
                counter += 1     
                peak_freq_assign.append(peak_freq_ini[i])
                peak_int_assign.append(peak_int_ini[i])
                peak_unc_assign.append(peak_unc_ini[i])
                # Also drop these into the bucket of lines that are assigned, with the
                # name of the assignment . . ..  something like
                bucket.append([peak_freq_ini[i], peak_int_ini[i], known_name]) 
                # where file_name gives the name of the molecule or "artifact"

                #but now we need to keep track of what was taken out so we will have a list of unassigned lines -
                # could do somthing like 
                #if(peak_freq_ini[i]) in leftoversOfBucket:  removeIt
                # humk - this seems awkward -
                # how about we just record the indices??  That's much better !!!
                bucketedLines.append(i)

        if (counter == 0):        
            peak_freq_end.append(peak_freq_ini[i])
            peak_int_end.append(peak_int_ini[i])
            peak_unc_end.append(peak_unc_ini[i])


    #for i in range(len(index_list)):
    #    del(peak_lines_end[index_list[i]])
    #    peaks_assigned.append(peak_lines[index_list[i]])
    #
    #del(index_list)

    # Check that the matching frequencies + new peak list
    # is equal to the initial number of peaks
    #check = len(peak_lines) - len(peaks_assigned) - len(peak_lines_end)

    print(str(len(match_freq)) + ' matching frequencies in ' + known_freq_name)
    print(str(match_freq))   #praa MArch 30 2016

    print(str(len(peak_freq_ini) - len(peak_freq_end)) + ' peak removed')
    if (len(match_freq) >  (len(peak_freq_ini) - len(peak_freq_end))):
        print("Mismatch !  Matching Frequencies: "+ str(match_freq))
    #print(peaks_assigned)
    print(str(len(peak_freq_end)) + ' remaining peaks')
    #print('----------------------')
    #print(str(len(peak_freq_end)) + ' - ' + str(len(peaks_assigned)) + ' - ' + str(len(peak_lines_end)) + ' = ' + str(check))
    #print('----------------------')

    # Create an array containing the list of matching frequencies
    match_peak_array = np.array( match_freq )

    del(counter)

#---------------------------------------------------
# CLEAR SPECTRUM
# Create a new spectrum without known transitions
#---------------------------------------------------
def clearSpectrum():
    global freq_list_ini
    global int_list_ini
    global match_peak_array
    global freq_list_assign
    global int_list_end
    global freq_list_end
    global int_list_assign


    # Loop on the spectrum frequencies
    for i in range(len(freq_list_ini)):
        # definition of an array for each frequency
        # by calculating the difference between the frequencies of the spectrum 
        # and the matching frequencies
        diff = np.abs(match_peak_array-freq_list_ini[i])
        # finding the index of the minimum of this array
        index = np.argmin(diff)
        
        # Since the array diff is of the same dimension as match_peak_array,
        # it is also of the same dimension as the match_int list,
        # We can thus determine intensity at this index.
        # The following expression of type y = a - b * c**x allows to clear the spectrum
        # in a range depending of the intensity of the peak to remove.
        # Values have been determined to describe these points:
        # (0,0), (0.03,0.3), (1,3), (5,5)
        if ( diff[index] < (5.2 - 4.97 * 0.41**(match_int[index])) *factor ):
            freq_list_assign.append(freq_list_ini[i])
            int_list_assign.append(int_list_ini[i])
            # Also drop these into the bucket of lines that are assigned, with the
            # name of the assignment . . ..  e.g. - oh, not here in the spectrum, in the line list - previous routime
            #  bucket.append(freq_list_ini[i], int_list_ini[i], file_name)
        else:
            int_list_end.append(int_list_ini[i])
            freq_list_end.append(freq_list_ini[i])
        # Create new lists for the assigned transitions 
        # and without them            
            

#---------------------------------------------------
# EXPORT THE ClEARED GRAPH, 
# THE ASSIGNED PORTIONS OF THE GRAPH
# THE LIST OF REMAINING PEAKS,
# AND THE LIST OF ASSIGNED PEAKS
#---------------------------------------------------

def exportTheClearedFiles():
    if("clear" in file_name):
        file_name_short = file_name.split('_clear')[0]
        file_name_long = file_name
    else:
        file_name_short = file_name
        file_name_long = file_name + '_clear'
        
    with open(file_name_long + '_' + known_name + '.sp', 'w') as sp_file:
        for i in range(len(freq_list_end)-1):
            sp_file.write('%5.3f %5.5f\n' %(freq_list_end[i], int_list_end[i]))
            # test without these lines - April 6 2016 PRAA
            #if (freq_list_end[i+1] - freq_list_end[i] > 2*step):
            #    sp_file.write('\n')
        sp_file.write('%5.3f %5.5f\n' %(freq_list_end[-1], int_list_end[-1]))            

    with open(file_name_short + '_assigned_' + known_name + '.sp', 'w') as sp_assign_file:
        for i in range(len(freq_list_assign)-1):
            sp_assign_file.write('%5.3f %5.5f\n' %(freq_list_assign[i], int_list_assign[i]))
            #if (freq_list_assign[i+1] - freq_list_assign[i] > 2 * step):
            #    sp_assign_file.write('\n')
        sp_assign_file.write('%5.3f %5.5f\n' %(freq_list_assign[-1], int_list_assign[-1]))
            
            
    with open(file_name_long + '_' + known_name + '.lines', 'w') as linelist_file:
        for i in range(len(peak_freq_end)):
            linelist_file.write('%9.3f %5.3f %5.3f\n' %(peak_freq_end[i], peak_int_end[i],  peak_unc_end[i]))

    with open(file_name_short + '_assigned_' + known_name + '.lines', 'w') as lines_assign_file:
        for i in range(len(peak_freq_assign)):
            lines_assign_file.write('%9.3f  %5.3f  %5.3f\n' %(peak_freq_assign[i], peak_int_assign[i], peak_unc_assign[i]))


# def copyClearedLineListToNextInput():
    #And also spectrum??



#---------------------------------------------------
# PLOT
#---------------------------------------------------
def renamedPlot():
    freq_list_a = []
    int_list_a = []
    freq_list_e = []
    int_list_e = []

    #For a nicer plot aspect
    for i in range(len(freq_list_assign)-1):
        freq_list_a.append(freq_list_assign[i])
        int_list_a.append(int_list_assign[i])
        if (freq_list_assign[i+1] - freq_list_assign[i] > 2 * step):
            freq_list_a.append(freq_list_assign[i])
            int_list_a.append(0)
            freq_list_a.append(freq_list_assign[i+1])
            int_list_a.append(0)
    freq_list_a.append(freq_list_assign[-1])
    int_list_a.append(int_list_assign[-1])

    for i in range(len(freq_list_end)-1):
        freq_list_e.append(freq_list_end[i])
        int_list_e.append(int_list_end[i])
        if (freq_list_end[i+1] - freq_list_end[i] > 2 * step):
            freq_list_e.append(freq_list_end[i])
            int_list_e.append(0)
            freq_list_e.append(freq_list_end[i+1])
            int_list_e.append(0)
    freq_list_e.append(freq_list_end[-1])
    int_list_e.append(int_list_end[-1])
            
            
            
    figure(2) # creation of a figure
    #
    # Known frequencies
    subplot(211) #
    title ('Known frequencies: ' + known_name)
    ion() #interactive mode
    #xlim([freq_list_ini[0], freq_list_ini[-1]])
    vlines(known_freq_array[:,0], 1e-10, known_freq_array[:,1], colors='red')
    #
    # Initial spectrum in the background, Cleared spectrum in the front
    subplot(212, sharex=subplot(211)) 
    title ('Initial spectrum (red), Cleared spectrum (blue)')
    plot(freq_list_a,int_list_a, color='red')
    plot(freq_list_e,int_list_e)
    vlines(match_peak_array, 1e-6, match_int, colors='gray', linestyle = '--')
    show(block=True)


if __name__ == "__main__":

# Import
    import sys # basic files tools
    from matplotlib.pyplot import *
    import numpy as np
    from math import *
    from mpl_toolkits.axes_grid1.axes_rgb import make_rgb_axes, RGBAxes

    getFileName()
    readSpectrumAndLineFiles()
    readKnownFile()
    peakAssignment(False)
    createListsOfPeaks()
    clearSpectrum()
    exportTheClearedFiles()
    renamedPlot()

 

