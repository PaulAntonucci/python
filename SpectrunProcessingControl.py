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

inputFilename = 'defaultInputFileName'

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
        self.comboBox1 = Spinbox(self.myContainer1, values = ("8 - 18 GHz", "6.5 - 19.6 GHz", "4 - 8 GHz", "18 - 26 GHz"), bg = 'white', width = 15)
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
        self.checkBox11 = Checkbutton(self.myContainer1, text = "C", variable = self.checkBoxC, onvalue=1,offvalue=0).place(x=75,y=elementsYOffset)
        self.checkBox12 = Checkbutton(self.myContainer1, text = "S", variable = self.checkBoxS, onvalue=1,offvalue=0).place(x=150, y=elementsYOffset)
        self.checkBox13 = Checkbutton(self.myContainer1, text = "O", variable = self.checkBoxO, onvalue=1,offvalue=0)
        #self.checkBox13.grid(row=32, column = 2)
        self.checkBox13.place(x = 225,y=elementsYOffset)
        self.checkBox14 = Checkbutton(self.myContainer1, text = "H", variable = self.checkBoxH, onvalue=1,offvalue=0).place(x=75,y=elementsYOffset + 25)
        self.checkBox15 = Checkbutton(self.myContainer1, text = "Si", variable = self.checkBoxSi, onvalue=1,offvalue=0).place(x=150,y=elementsYOffset + 25)
        self.checkBox16 = Checkbutton(self.myContainer1, text = "N", variable = self.checkBoxN, onvalue=1,offvalue=0)
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
        ClearSpectrum2.spectrum_name = baseNameThatCameIn + '.sp'
        ClearSpectrum2.file_name = baseNameThatCameIn
        ClearSpectrum2.known_freq_name = 'FromMarie/artifacts.cat'
        # ClearSpectrum2.known_name = 'artifacts' - now calculated in ClearSpectrum2.py praa Feb 10 2016
        ClearSpectrum2.readSpectrumAndLineFiles()
        ClearSpectrum2.readKnownFile()
        ClearSpectrum2.peakAssignment(False)    # False means it's not necessary to supress the plot
        ClearSpectrum2.createListsOfPeaks()
        ClearSpectrum2.clearSpectrum()
        ClearSpectrum2.exportTheClearedFiles()
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

    def removeMolecularLines(self, event):
        global inputFilename
        print ('removing molecular lines')
        self.commonVariable1 = 5
        self.checkBox10.select()
        print('inputFilename=', inputFilename)
        splitName = inputFilename.split('.')
        baseNameThatCameIn = splitName[0]
        fileType = splitName[1]  
        ClearSpectrum2.spectrum_name = baseNameThatCameIn + '.sp'
        ClearSpectrum2.file_name = baseNameThatCameIn


        path = "MoleculeCatFiles"
        for localCatFileName in os.listdir(path):
            print(localCatFileName)
            if(".cat" in localCatFileName):
                ClearSpectrum2.known_freq_name = 'MoleculeCatFiles/' + localCatFileName
                ClearSpectrum2.clearVariables()
                ClearSpectrum2.readKnownFile()
                ClearSpectrum2.peakAssignment(True) # True means doNotPlot
                ClearSpectrum2.createListsOfPeaks()
##                ClearSpectrum2.clearSpectrum()
##                ClearSpectrum2.exportTheClearedFiles()
##                ClearSpectrum2.renamedPlot()

        
        
    def addAdditionalElement(self, event):
        print ('adding additional element - ', self.comboBox3.get())
        #print(self.checkBox1Variable )
        #self.checkBox1Variable += 1
        print (' testing for check box variables ')
        
        print(str(self.checkBox1Variable.get()) )
        if( self.checkBox3Variable.get() == 0):        print (' checkbox 3 =0')
        if(self.checkBox3Variable.get() == 1):         print (' checkbox 3 =1')       
        if(self.checkBoxOCS.get() == 0):               print (' checkbox 4 =0')
        if(self.checkBoxOCS.get() == 1):               print (' checkbox 4 =1')
        if(self.checkBoxH2O2.get() == 0):              print (' checkbox 5 =0')
        if(self.checkBoxH2O2.get() == 1):              print (' checkbox 5 =1')
        if(self.checkBoxSO2.get() == 0):               print (' checkbox 6 =0')
        if(self.checkBoxSO2.get() == 1):               print (' checkbox 6 =1')

        for i in range(0,3):
            print('index = ' + str(i))
            if   ((i==0) and (self.checkBoxH2O2.get() == 1)):   ClearSpectrum2.known_freq_name = 'Contaminants/h2o_dimer.list'
            elif ((i==1) and (self.checkBoxSO2.get() == 1)):     ClearSpectrum2.known_freq_name = 'Contaminants/so2.cat'
            elif ((i==2) and (self.checkBoxOCS.get() == 1)):     ClearSpectrum2.known_freq_name = 'Contaminants/ocs.cat'
            else: ClearSpectrum2.known_freq_name = 'none'
            print(' iteration  - file name =  ', ClearSpectrum2.known_freq_name)


        
            
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




myapp = MyApp(root)
root.mainloop()
