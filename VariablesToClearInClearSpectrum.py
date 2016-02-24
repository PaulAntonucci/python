    global freq_list_ini
    global int_list_ini

    global peak_freq_ini;
    global peak_int_ini;
    global peak_unc_ini;
    global peak_array;
    
    global known_freq_array - similar to peak_array - is set equal to an np.array
    global step
    
    global match_freq 
    global match_int
    global match_peak_array
   
    global  peak_freq_end
    global  peak_int_end 
    global  peak_unc_end 
    global  peak_freq_assign
    global  peak_int_assign
    global  peak_unc_assign

 
    global freq_list_assign
    global int_list_end
    global freq_list_end
    global int_list_assign
  

    total of 21 variables, of them peak_array
    is an np. array of arrays
    peak_array =
    np.array( [peak_freq_ini, peak_int_ini, peak_unc_ini] )

# These are in get_file_name:
    # There are also
    global spectrum_name;   # spectrum file
    global file_name;       # This is spectrum_name without the extension
    global known_freq_name; # The list of lines to be subtracted 
    global known_name;      # The same thing without the extension or the directory (if it was e.g. files/c3s.cat)
    global ext;             # the extension of the known frequency file
    global factor;          # 2 if it's an artifact file, else 1


# In Read the spectrum file
    # the initial spectrum
    global freq_list_ini;   global int_list_ini;
    global step; # only one that's not an array    

    # The .lines file of the spectrum
    global peak_freq_ini;   global peak_int_ini;    global peak_unc_ini;
    peak_array - the three above as an np.array

    # the "known" (e.g. artifacts) file
    global known_freq_array = np.array(freq, inten)

# in peak assignment
    global match_freq global match_int

# in createListsOfPeaks():
    global match_peak_array (also match_freq and peak_array)
    global  peak_freq_end
    global  peak_int_end 
    global  peak_unc_end 
    global  peak_freq_assign
    global  peak_int_assign
    global  peak_unc_assign

# in clearSpectrum
    global freq_list_ini
    global int_list_ini
    global match_peak_array
    
    global freq_list_assign
    global int_list_end
    global freq_list_end
    global int_list_assign

    

    
