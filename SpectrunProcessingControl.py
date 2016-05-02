from tkinter import *
from tkinter import filedialog #import askopenfilename

from tkinter.filedialog import askopenfilename

import subprocess
import shutil
import MatPlotDemo
import ClearSpectrum2
import CallScriptTest
import PeakFinder_BlackChirp2
import time
import os
import numpy as np
from math import ceil

#import sys # basic files tools
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.axes_rgb import make_rgb_axes, RGBAxes

inputFilename = 'defaultInputFileName'
printing = False
listOfAllMolecules = []
additionalElementsAdded = []
reportFile = []

class MyApp:
    def __init__(self, myParent):
        button_width = 20
        button_padx = "2m"
        button_pady = "1m"
        button_background = '#cfccc9'

        buttons_frame_padx = "10m"
        buttons_frame_pady = '10m'
        buttons_frame_ipadx = '100m'
        buttons_frame_ipady = '50m'
        elementsYOffset = 320
        
        self.commonVariable1 = 0
        self.commonVariable2 = None
        self.checkBox1Variable = IntVar();  self.checkBox2Variable = IntVar();
        self.checkBox3Variable = IntVar(); 
        self.checkBoxOCS = IntVar();        self.checkBoxH2O2 = IntVar();   self.checkBoxSO2 = IntVar();
        self.checkBox4Variable = IntVar()
        self.checkBoxC = IntVar();          self.checkBoxS = IntVar();      self.checkBoxO = IntVar();
        self.checkBoxH = IntVar();          self.checkBoxSi= IntVar();      self.checkBoxN = IntVar()
        
        self.myParent = myParent
        self.myContainer1 = Frame(myParent)
        #self.myContainer1.grid()
        self.myContainer1.grid(
            ipadx = buttons_frame_ipadx,
            ipady = buttons_frame_ipady,
            padx = buttons_frame_padx,
            pady = buttons_frame_pady)

        # Label(self.myContainer1, text="Current Spectrum File", height=3, width = 20).grid(row = 0, column = 0)
        self.button0 = Button(self.myContainer1, command = self.openFileFromButton)
        self.button0["text"] = 'Open File'
        self.button0['background'] = button_background
        self.button0.configure (
            width = button_width,
            padx = button_padx,
            pady = button_pady)
        self.button0.grid(row = 0, column = 0)
        self.e1 = Entry(self.myContainer1, bg = 'white', text = 'NameOfFile')
        self.e1.grid(row = 0, column = 1)
        
        
        Label(self.myContainer1, text="Frequency Range", height =3).grid(row = 1, column = 0)
        self.comboBox1 = Spinbox(self.myContainer1, values = ("6.5 - 19.6 GHz", "8 - 18 GHz", "4 - 8 GHz", "18 - 26 GHz"), bg = 'white', width = 15)
        self.comboBox1.grid(row = 1, column = 1)
        
        self.button1 = Button(self.myContainer1, command = self.createFT)   # can either put the command in here, or use the "bind" below
        self.button1['text'] = 'Create FT'
        self.button1['background'] = button_background
        self.button1.configure (
            width = button_width,
            padx = button_padx,
            pady = button_pady)
        self.button1.grid(row=2, column=0)
        # self.button1.focus_force()
        # self.button1.bind('<Button-1>', self.createFT)
        # self.button1.bind('<Return>', self.createFT_withEvent)
        
        # self.checkBox1Variable = 1
        print(self.checkBox1Variable.get() )
        self.checkBox1 = Checkbutton(self.myContainer1, text = "FT Done", variable = self.checkBox1Variable, onvalue=1,offvalue=0)#height=3,width=20)
        self.checkBox1.grid(row=2, column = 1, sticky = W) #note sticky = W has no effect if using height=, width=
        # Label(self.myContainer1, text="Window").grid(row=2, column=2)
        Label(self.myContainer1, text="pzf number").place(x=290, y = 80)
        print(self.checkBox1Variable.get() )       

        #self.comboBox2 =Spinbox(self.myContainer1, width = 8, values=("Gaussian","Rectangle","Hann", "Hamming", "Cosine"), bg = 'white').grid(row=2,column=3)
        self.comboBox2 =Spinbox(self.myContainer1, width = 8, values=("1","2","3", "4", "5", "6","7","8", "9", "10", "11","12","13", "14", "15","16"), bg = 'white').grid(row=2,column=3)

        self.button2 = Button(self.myContainer1 )
        self.button2.configure(text = "Remove Artifacts ")
        self.button2.configure(background = button_background)#'tan')
        self.button2.configure( width = button_width, padx = button_padx, pady = button_pady)
        self.button2.grid(row=10, column =0)
        self.button2.bind("<Button-1>", self.removeArtifacts)
        self.button2.bind("<Return>", self.removeArtifacts)

        self.checkBox2 = Checkbutton(self.myContainer1, text = "Artifacts Removed", variable = self.checkBox2Variable,\
                                     onvalue=1,offvalue=0,height=3,width=20)
        self.checkBox2.grid(row=10, column = 1)

        

        self.button3 = Button(self.myContainer1, text = "Remove Contaminants")
        self.button3.configure(background = button_background)
        self.button3.configure( width = button_width, padx = button_padx, pady = button_pady)
        self.button3.grid(row=20, column = 0)
        self.button3.bind("<Button-1>", self.removeContaminants)
        self.button3.bind("<Return>", self.removeContaminants)

        self.checkBox3 = Checkbutton(self.myContainer1, text = "Contaminants Removed", variable = self.checkBox3Variable,\
                                     onvalue=1,offvalue=0,height=1,width=20)
        self.checkBox3.grid(row=20, column = 1)

        self.checkBox4 = Checkbutton(self.myContainer1, text = "OCS", variable = self.checkBoxOCS, onvalue=1,offvalue=0).grid(row=21,column=0, sticky = W)
        self.checkBox5 = Checkbutton(self.myContainer1, text = "(H2O)2", variable = self.checkBoxH2O2, onvalue=1,offvalue=0).grid(row=22, column = 0, sticky = W)
        self.checkBox6 = Checkbutton(self.myContainer1, text = "SO2", variable = self.checkBoxSO2, onvalue=1,offvalue=0)
        self.checkBox6.grid(row=23, column = 0, sticky = W)

        self.button4 = Button(self.myContainer1, text = "Remove Molecular Lines")
        self.button4.configure(background = button_background)#tan')
        self.button4.configure( width = button_width, padx = button_padx, pady = button_pady)
        self.button4.grid(row=30, column = 0)
        self.button4.bind("<Button-1>", self.removeMolecularLines)
        self.button4.bind("<Return>", self.removeMolecularLines)

        self.checkBox10 = Checkbutton(self.myContainer1, text = "Molecular Lines Removed", variable = self.checkBox4Variable,onvalue=1,offvalue=0,height=3,width=20)
        self.checkBox10.grid(row=30, column = 1)
        self.label2 = Label(self.myContainer1, text = "Atoms Present")
        self.label2.grid(row=31, column = 0)
        self.checkBox11 = Checkbutton(self.myContainer1, text = "H", variable = self.checkBoxH, onvalue=1,offvalue=0).place(x=75,y=elementsYOffset)
        self.checkBox12 = Checkbutton(self.myContainer1, text = "C", variable = self.checkBoxC, onvalue=1,offvalue=0).place(x=150, y=elementsYOffset)
        self.checkBox13 = Checkbutton(self.myContainer1, text = "N", variable = self.checkBoxN, onvalue=1,offvalue=0)
        #self.checkBox13.grid(row=32, column = 2)
        self.checkBox13.place(x = 225,y=elementsYOffset)
        self.checkBox14 = Checkbutton(self.myContainer1, text = "O", variable = self.checkBoxO, onvalue=1,offvalue=0).place(x=75,y=elementsYOffset + 25)
        self.checkBox15 = Checkbutton(self.myContainer1, text = "Si", variable = self.checkBoxSi, onvalue=1,offvalue=0).place(x=150,y=elementsYOffset + 25)
        self.checkBox16 = Checkbutton(self.myContainer1, text = "S", variable = self.checkBoxS, onvalue=1,offvalue=0)
        self.checkBox16.place(x=225, y = elementsYOffset +25)

        self.label2 = Label(self.myContainer1, text = "Additional Atoms")
        self.label2.place(x=40, y = elementsYOffset + 50)
        
        self.comboBox3 = Spinbox(self.myContainer1, values = ("Choose", "He", "Li", "Be", "B", "F", "Ne", "Na", "Mg", "Al", "Si", "P", "Cl", "Ar", "K", "Ca"), width = 10)
        self.comboBox3.place (x = 75, y = elementsYOffset + 83)
        
        self.button5 = Button(self.myContainer1, text = "Add Element", bg = button_background)
        self.button5.configure(padx = button_padx, pady = button_pady)
        self.button5.place(x=200, y=elementsYOffset + 80)
        self.button5.bind("<Button-1>", self.addAdditionalElement)
        self.button5.bind("<Return>", self.addAdditionalElement)


        self.label3 = Label(self.myContainer1, text = "Molecules/Lines")
        self.label3.place(x=37
                          , y=elementsYOffset + 125)
        self.text1 = Text(self.myContainer1, height = 20, width = 20, bg = 'white')
        self.text1.place(x=37, y= elementsYOffset + 150)

        self.label4 = Label(self.myContainer1, text = "Molecules Found")
        self.label4.place(x=225, y=elementsYOffset + 125)
        self.text2 = Text(self.myContainer1, height = 20, width = 20, bg = 'white')
        self.text2.place(x=225, y= elementsYOffset + 150)

        self.label5 = Label(self.myContainer1, text = "Incoming Data")
        self.label6 = Label(self.myContainer1, text = "Processed Data")
        self.label5.place(x = 500, y = 370)
        
        self.label6.place(x = 500, y = 670)
        self.canvas1 = Canvas(self.myContainer1, height = 250, width = 750, bg = 'white', bd=3)
        self.canvas2 = Canvas(self.myContainer1, height = 250, width = 750, bg = 'white')
        self.canvas1.place(x = 500, y = 100)
        self.canvas2.place(x = 500, y = 400)

        #self.button10 = Button(self.myContainer1, text = 'Exit Button', command = self.exult)
        #self.button10.place(x=120, y = elementsYOffset + 200)


    def openFileFromButton(self):
        global inputFilename
        inputFilename = askopenfilename(parent=root)
        print ("Filename = ", inputFilename)
        self.e1.delete(0,END)
        stuffs= inputFilename.split('/')
        shortName = stuffs[len(stuffs)-1]
        print(shortName)
        self.e1.insert(0,shortName)
        self.checkBox1.deselect()       #Checkbox 1 is FFT Done
        self.checkBox2.deselect()       #Checkbox 2 is ARtifacts Removed
        self.checkBox3.deselect()       #Checkbox 3 is Contanimants
        self.checkBox10.deselect()       #Checkbox 10 is Molecules
        ClearSpectrum2.clearVariables()

    def createFT_withEvent(self, event):
        print ('mouse = ', str(event.x), str(event.y))
        report_event(event)
        self.createFT()
        self.commonVariable1 = 1
        self.checkBox1.select()

    def createFT(self): #, event):
        global inputFilename
        #report_event(event)
        if(self.checkBox1Variable.get()==1):
            print("FFT already taken !!!! returning")
            print(str(self.checkBox1Variable.get()))
            return
        print(' Creating FT - add a check for file type')
        print(self.comboBox1.get())
        if(self.comboBox1.get() == "6.5 - 19.6 GHz"):
            PeakFinder_BlackChirp2.fft_ini_freq = 6500
            PeakFinder_BlackChirp2.fft_end_freq =19500
        elif (self.comboBox1.get() ==  "4 - 8 GHz"):
            PeakFinder_BlackChirp2.fft_ini_freq = 4000
            PeakFinder_BlackChirp2.fft_end_freq = 8000
        elif (self.comboBox1.get() ==  "8 - 18 GHz"):
            PeakFinder_BlackChirp2.fft_ini_freq = 8000
            PeakFinder_BlackChirp2.fft_end_freq =18000
        elif (self.comboBox1.get() == "18 - 26 GHz"):
            PeakFinder_BlackChirp2.fft_ini_freq = 18000
            PeakFinder_BlackChirp2.fft_end_freq = 26000

        PeakFinder_BlackChirp2.spectrum_name = inputFilename;
        PeakFinder_BlackChirp2.file_name = inputFilename.split('.')[0];
        if ('fid' in PeakFinder_BlackChirp2.file_name):
            PeakFinder_BlackChirp2.file_name = PeakFinder_BlackChirp2.file_name.split('_')[0]
        if ('/' in PeakFinder_BlackChirp2.file_name):
            tempsplits = PeakFinder_BlackChirp2.file_name.split('/')
            
            PeakFinder_BlackChirp2.file_name = tempsplits[len(tempsplits) -1]
        PeakFinder_BlackChirp2.ext =inputFilename.split('.')[1];
        PeakFinder_BlackChirp2.n_pzf = 1

        PeakFinder_BlackChirp2.readInputFiles()
        print("retuned from readInputFiles****************************************")
        PeakFinder_BlackChirp2.FIDtoFFT()
        print("retuned from FID to FFT**********************************************")
        PeakFinder_BlackChirp2.peakDetection()
        print("retuned from PeakFinder**************************************************")
        PeakFinder_BlackChirp2.exportSpectrumFile()
        print("retuned from exportSpectrumFile***********************************************")
        self.checkBox1.select()
        PeakFinder_BlackChirp2.plotSpectrum()
        print("retuned from PeakFinder . . . plotSpectrum")

    def removeArtifacts(self, event):
        global inputFilename                # The input file might have been a spectrum file or a FID file.
        print( ' removing Artifacts - ')    
        self.commonVariable1 = 3
        self.checkBox2.select()
        print('inputFilename=', inputFilename)
        splitName = inputFilename.split('.')
        baseNameThatCameIn = splitName[0]
        fileType = splitName[1]
        if(fileType != 'sp'):               # IF the input file was FID, then use the file created by 'createFT', above
            print("Getting the spectrum file created by the routine createFT,")
            print(PeakFinder_BlackChirp2.exportedFileName)
            splitName = PeakFinder_BlackChirp2.exportedFileName.split('.')
            print(splitName)
            baseNameThatCameIn = splitName[0]
            fileType = splitName[1]
            if(fileType != 'sp'):
                print("Sorry - that is not a spectrum file type")
        ClearSpectrum2.clearVariables()
        ClearSpectrum2.spectrum_name = baseNameThatCameIn + '.sp'
        ClearSpectrum2.file_name = baseNameThatCameIn
        ClearSpectrum2.known_freq_name = 'ArtifactFiles/artifacts_18950MHz.cat'
        # ClearSpectrum2.known_name = 'artifacts' - now calculated in ClearSpectrum2.py praa Feb 10 2016
        ClearSpectrum2.readSpectrumAndLineFiles()
        ClearSpectrum2.readKnownFile()
        ClearSpectrum2.peakAssignment(False)    # False means it's not necessary to supress the plot
        ClearSpectrum2.createListsOfPeaks()
        ClearSpectrum2.clearSpectrum()
        ClearSpectrum2.exportTheClearedFiles()
        print("Original bucket" + str(ClearSpectrum2.bucket))
        
        # now re-load in the cleared spectrum and line file  PRAA April 11 2016
        ClearSpectrum2.spectrum_name = baseNameThatCameIn + '_clear_artifacts_18950MHz.sp'
        ClearSpectrum2.file_name = baseNameThatCameIn + '_clear_artifacts_18950MHz'
        ClearSpectrum2.readSpectrumAndLineFiles()
        print("Un - Original bucket" + str(ClearSpectrum2.bucket))
        
        ClearSpectrum2.renamedPlot()

    def removeContaminants(self, event):
        global inputFilename
        print (" Removing contaminants ")

        print('inputFilename=', inputFilename)
        splitName = inputFilename.split('.')
        baseNameThatCameIn = splitName[0]
        fileType = splitName[1]
        if(fileType != 'sp'):
            print("looks like we're going to use the exported file name")
            print(PeakFinder_BlackChirp2.exportedFileName)
            splitName = PeakFinder_BlackChirp2.exportedFileName.split('.')
            print(splitName)
            baseNameThatCameIn = splitName[0]
            fileType = splitName[1]
            if(fileType != 'sp'):
                print("Sorry - that is not a spectrum file type")
    
        ClearSpectrum2.spectrum_name = baseNameThatCameIn + '.sp'
        ClearSpectrum2.file_name = baseNameThatCameIn
        ClearSpectrum2.clearVariables()
        for i in range(0,3):
            # print('index = ' + str(i))
            if  ((i==0) and (self.checkBoxOCS.get() == 1)):     ClearSpectrum2.known_freq_name = 'Contaminants/ocs.cat'
            elif((i==1) and (self.checkBoxH2O2.get() == 1)):   ClearSpectrum2.known_freq_name = 'Contaminants/h2o_dimer.list'
            elif((i==2) and (self.checkBoxSO2.get() == 1)):     ClearSpectrum2.known_freq_name = 'Contaminants/so2.cat'
            else: ClearSpectrum2.known_freq_name = 'none'
            # print(' iteration  - file name =  ', ClearSpectrum2.known_freq_name)
            if (ClearSpectrum2.known_freq_name != 'none'):
                ClearSpectrum2.clearVariables()
                ClearSpectrum2.readKnownFile()
                # the argument True means "doNotPlot"
                ClearSpectrum2.peakAssignment(True)
                ClearSpectrum2.createListsOfPeaks()
                # ClearSpectrum2.clearSpectrum()
                # ClearSpectrum2.exportTheClearedFiles()
                # ClearSpectrum2.renamedPlot()
                # time.sleep(2)

        self.commonVariable1 = 4
        self.checkBox3.select()
        print("Uncontaminated bucket" + str(ClearSpectrum2.bucket))

    def removeMolecularLines(self, event):
        global inputFilename
        listOfMoleculesPresent = []
        print ('removing molecular lines')
        self.commonVariable1 = 5
        self.checkBox10.select()
        print('inputFilename=', inputFilename)
        splitName = inputFilename.split('.')
        baseNameThatCameIn = splitName[0]
        fileType = splitName[1]  
        ClearSpectrum2.spectrum_name = baseNameThatCameIn + '.sp'
        ClearSpectrum2.file_name = baseNameThatCameIn
        atoms = []; atoms.append("Atoms:")
        if(self.checkBoxH.get() == 1): atoms.append("H")
        if(self.checkBoxC.get() == 1): atoms.append("C")
        if(self.checkBoxN.get() == 1): atoms.append("N")
        if(self.checkBoxO.get() == 1): atoms.append("O")
        if(self.checkBoxSi.get() == 1): atoms.append("Si")
        if(self.checkBoxS.get() == 1): atoms.append("S")
        atoms.extend(additionalElementsAdded)
        print (atoms)
        
        listOfMolecluesToTry = createListOfPossibleMolecules(atoms)
        toMakeTheFTBFileFreq = []
        toMakeTheFTBFileIntensity = []
        #del toMakeTheFTBFileFreq[:]
        #del toMakeTheFTBFileIntensity[:]
        del reportFile[:]
        path = "MoleculeCatFiles"
        for molecule in listOfMolecluesToTry:
            print("\nmolecule " + str(molecule))
            self.text1.insert(END,molecule[0])
            print(molecule[2])
            if '.lines' in molecule[2]:
                localCatFileName = molecule[2]
            else:
                localCatFileName = molecule[2] + ".cat"
            print(localCatFileName)
            ClearSpectrum2.known_freq_name = 'MoleculeCatFiles/' + localCatFileName
            ClearSpectrum2.clearVariables()
            ClearSpectrum2.readKnownFile()
            numberOfMatchedPeaks = ClearSpectrum2.peakAssignment(True) # True means doNotPlot
            print("Number of Matched Peaks = ", numberOfMatchedPeaks)
            if(numberOfMatchedPeaks >0):
                listOfMoleculesPresent.append(molecule[0])
                self.text2.insert(END, molecule[0])
                ClearSpectrum2.createListsOfPeaks()
                print(str(ClearSpectrum2.match_freq))
                print("\n Molecule: "+str(molecule)+" \npeaks: ")
                reportFile.append("\n Molecule: "+str(molecule)+" \npeaks: "+str(ClearSpectrum2.match_freq))
##                ClearSpectrum2.clearSpectrum()
##                ClearSpectrum2.exportTheClearedFiles()
##                ClearSpectrum2.renamedPlot()

        print("\n\nList Of Molecules Present: ", listOfMoleculesPresent)
        print("\nNumber of molecules present = ", str(len(listOfMoleculesPresent)))
        print("Lines in spectrum: "+ str(ClearSpectrum2.freq_list_end))
        for index in range(len(reportFile)):
            print(reportFile[index])
        print("Final List of removed molecular lines (the Bucket)")
        for index in range (len(ClearSpectrum2.bucket)):
            print(ClearSpectrum2.bucket[index])
        
        print("\nUnassigned Lines:")
        print("Frequency, Intensity")
        for index in range (len(ClearSpectrum2.peak_freq_ini)):
            if index in ClearSpectrum2.bucketedLines:
                print("Cleared: " + str(ClearSpectrum2.peak_freq_ini[index]), str(ClearSpectrum2.peak_int_ini[index]))
            else:
                print(str(ClearSpectrum2.peak_freq_ini[index]),"\t" , str(ClearSpectrum2.peak_int_ini[index]))
                toMakeTheFTBFileFreq.append(ClearSpectrum2.peak_freq_ini[index])
                toMakeTheFTBFileIntensity.append(ClearSpectrum2.peak_int_ini[index])
        # Create FTB file
        FTBFilePeakArray = np.array( [toMakeTheFTBFileFreq, toMakeTheFTBFileIntensity] ).transpose()
        FTBFilePeakArray = FTBFilePeakArray[FTBFilePeakArray[:, 1].argsort()[::-1]]
        with open(baseNameThatCameIn + '.ftb', 'w') as out_file:    
            for i in range(len(FTBFilePeakArray)):
                # define the number of shots as a function of the intensity
                n_shots = ceil(2 / (5 * FTBFilePeakArray[i,1])) 
                if (n_shots < 10):
                    n_shots = 10
                out_file.write('ftm:%5.3f shots:%1s dipole:1.0 drpower:-20 drfreq:1000.000\n' %(FTBFilePeakArray[i,0], n_shots))
        out_file.close()
        # Create Report file

        filename = baseNameThatCameIn + 'report.txt'
        outf = open(filename, 'w')
        outf.write("Report File for " + baseNameThatCameIn + '\n\n Lines assigned to molecules:\n')
        for index in range (len(ClearSpectrum2.bucket)):
            lineToWrite = str(ClearSpectrum2.bucket[index]) + '\n'
            outf.write(lineToWrite)
        outf.write('\nList of un-assigned lines in Intensity order\n\n')
        outf.write('\nFrequency: \tIntensity:\n')
        for index in range (len(FTBFilePeakArray)):
              lineToWrite = str(FTBFilePeakArray[index,0]) +'   \t' + str(FTBFilePeakArray[index,1]) + '\n'
              outf.write(lineToWrite)
        outf.write('\nList of un-assigned lines in Frequency order\n\n')
        outf.write('\nFrequency: \tIntensity\n')
        FTBFilePeakArray = FTBFilePeakArray[FTBFilePeakArray[:, 0].argsort()]
        for index in range (len(FTBFilePeakArray)):
              lineToWrite = str(FTBFilePeakArray[index,0]) + '   \t'+ str(FTBFilePeakArray[index,1]) + '\n'
              outf.write(lineToWrite)
                
        outf.close()

                
        # Now create graph
        xCoord = []
        yCoord = []
        for index in range(len(ClearSpectrum2.bucket)):
            xCoord.append (ClearSpectrum2.bucket[index][0])
            yCoord.append (ClearSpectrum2.bucket[index][1])
            # print ("X coord " + str(xCoord[index]))
            # print ("Y coord " + str(yCoord[index]))

        plt.figure(3) # creation of a figure
        #
        # Known frequencies
        plt.subplot(211) #
        plt.title ('Peaks removed ')
        plt.ion() #interactive mode
        #xlim([freq_list_ini[0], freq_list_ini[-1]])
        plt.vlines(xCoord, 0, yCoord, colors='red')
        # Initial spectrum in the background, Cleared spectrum in the front
        plt.subplot(212, sharex=plt.subplot(211)) 
        plt.title ('Initial spectrum (blue), Matched lines (red)')
        #, color='red')
        plt.plot(ClearSpectrum2.freq_list_ini,ClearSpectrum2.int_list_ini)
        newY = max(ClearSpectrum2.int_list_ini) * 1.1
        plt.vlines(xCoord, 0, newY, colors='red')
        #vlines(match_peak_array, 1e-6, match_int, colors='gray', linestyle = '--')
        plt.show(block=True)
        
        
    def addAdditionalElement(self, event):
        print ('adding additional element - ', self.comboBox3.get())
        additionalElementsAdded.append(self.comboBox3.get())
        #print(self.checkBox1Variable )
        #self.checkBox1Variable += 1
        print (' testing for check box variables ')
        
        print(str(self.checkBox1Variable.get()) )
        if(self.checkBoxH.get() == 0):      print (' checkbox H =0')
        if(self.checkBoxH.get() == 1):      print (' checkbox H =1')       
        if(self.checkBoxC.get() == 0):      print (' checkbox C =0')
        if(self.checkBoxC.get() == 1):      print (' checkbox C =1')
        if(self.checkBoxN.get() == 0):      print (' checkbox N =0')
        if(self.checkBoxN.get() == 1):      print (' checkbox N =1')
        if(self.checkBoxO.get() == 0):      print (' checkbox O =0')
        if(self.checkBoxO.get() == 1):      print (' checkbox O =1')
        if(self.checkBoxSi.get() == 0):     print (' checkbox O =0')
        if(self.checkBoxSi.get() == 1):     print (' checkbox O =1')
        if(self.checkBoxS.get() == 0):      print (' checkbox O =0')
        if(self.checkBoxS.get() == 1):      print (' checkbox O =1')

        atoms = []; atoms.append("Atoms:")

        if(self.checkBoxH.get() == 1): atoms.append("H")
        if(self.checkBoxC.get() == 1): atoms.append("C")
        if(self.checkBoxN.get() == 1): atoms.append("N")
        if(self.checkBoxO.get() == 1): atoms.append("O")
        if(self.checkBoxSi.get() == 1): atoms.append("Si")
        if(self.checkBoxS.get() == 1): atoms.append("S")
        print(atoms)


        
            
    def exult(self):
        print ('Exulting and exiting')
        print ('Common variable 1 and 2 are', str(self.commonVariable1), self.commonVariable2)
        self.myParent.destroy()
    

           
def openFile():
    inputFilename = askopenfilename(parent=root)
    print ("Filename = ", inputFilename)
    self.e1.delete(0,END)
    self.e1.insert(0,"SomeString")
        

def report_event(event):
        event_name = {"2": "Keypress", "4": 'Button Press'}
        print ("Reporting event \n mouse x and y: " + str(event.x), str(event.y))
        print ("Time =", str(event.time))
        print ('type =', str(event.type), event_name[str(event.type)])
        print ('EventWidgetId' + str(event.widget), 'eventKey symbol' +str(event.keysym))

def initializeListOfAllMolecules():
    global listOfAllMolecules
    # get from a directory the list of all molecules,
    # append each one to the list
    import glob
    import os
    from copy import deepcopy
    
    path = 'MoleculeHeaderFiles'
    moleculeIndex = 0
    localMolecule = ["Name: xx","Atoms: xx", "Filename"]
    for filename in glob.glob(os.path.join(path,'*.h')):
        print("Filename: ", filename)
        f = open(filename, 'r')
        lines = f.readlines()
        endIsAt = len(lines)
        fileType = ''
        # scan through to build up a molecule, then add it to the structure when done
        for index in range (0,endIsAt):
            if (printing ==True) : print("Index=:", index)
            if (printing ==True) : print("lines[index] " + lines[index])
            if('Name:') in lines[index]:
                localMolecule[0] = lines[index]
            if('Atoms:') in lines[index]:
                if (printing ==True) : print(localMolecule)
                #remove commas    ??  below . . .            
                localMolecule[1] = lines[index].split()
            if("FileType:") in lines[index]:
                fileType = lines[index].split()[1] 

        # but listOfAllMolecules is not long enough yet - so append something, then do a deep copy
        baseName = filename.split('.')[0]
        if ('/' in baseName):
            baseName = baseName.split('/')[1]
        localMolecule[2] = baseName + fileType
        #localMolecule[2] =  localMolecule[0].split()[1]      
        listOfAllMolecules.append([1,2,3])
        listOfAllMolecules[moleculeIndex] = deepcopy(localMolecule)
        moleculeIndex +=1
        if (printing ==True) : print("internal ", listOfAllMolecules)
    if (printing ==True) : print(listOfAllMolecules)
    

    # The following lines are test code. Should be removed "eventually"
    # atoms = ["Atoms:", "C", "S", "H", "O", "Si", "N"]
    # response = createListOfPossibleMolecules(atoms)
    # print("Number of possible molecules", len(response)) 
    # print("List of possible molecules: " + str(response))
                

def createListOfPossibleMolecules(atoms):
    listOfPossibleMolecules = []

    for(molecule) in listOfAllMolecules:
        possible = True
        print("Molecule: "+ str(molecule[0]))
        for atom in molecule[1]:
            if (printing ==True) : print("original ",atom)
            # remove commas
            filtered = atom.replace (',','')
            if (printing ==True) : print("commas removed ",filtered)
            if filtered in atoms:
                if (printing ==True) : print ("present " + str(filtered))
            else:
                if (printing ==True) : print ("not present " + str(filtered
                                            ))
                possible = False
        if(possible):
            print("possible\n")
            listOfPossibleMolecules.append(molecule)
        else:
            print("Not possible\n")
    print("Number of possible molecules", len(listOfPossibleMolecules)) 
    print("List of possible molecules: " + str(listOfPossibleMolecules)) 
    return(listOfPossibleMolecules)
    
           
def molecularLinesMatchTest(molecule):
    print ("Calling molecularLinesMatchTest - ")
    print ("this hasn't been written yet")
        # fetch cat file for moleculr
        # get lines from file
        # sort by intensity
        # Try to match first n lines
        # for x = 1 to n
        #       if (lineIsPresent)
        #           weightingFunction += 1/x
        #       else
        #           if lineWasObscured don't do anything
        #           else itShouldHAveBeenThereButWasn't
        #               weightingFunction -= 1/x

        # if(weightingFunction>limit)():
        #   molecule is present - mark lines in list
        #   so there's either a 2 D list of freq + on/off + which_molecule + ?(intensity . . . ), or
        #   a parallel data structure that keeps the flag for each one -
        #   the 2D structure doesn't seem to go very well in Python . . .  


root = Tk()
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=openFile)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)

initializeListOfAllMolecules()



myapp = MyApp(root)
root.mainloop()
