from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
import subprocess
import shutil




#variables

j =1
k =2
kc = 0
kcpatch = 0


frequencies =[7063.9800, 7822.1260, 7105.532, 7908.580]
uncertainties = [0.1, 0.1, 0.1, 0.1]

j_low =  5
j_high = 15
k_low =  0
k_high = 7
rms = 1.2345678

numberOfLines = 4 #len(frequencies)


# dimension of array = (j_high - j_low) * (k_high - k_low) * 2 - (j_high - j_low) - for the intances when k = 0
numberOfFiles = (j_high - j_low) * (k_high - k_low) * 2 - (j_high - j_low)

jQuantumIncrements=  [0,1,0,1]
kQuantumIncrements = [0,0,1,1]


jArray=[0 for i in range(numberOfFiles)]
kArray=[0 for i in range(numberOfFiles)]
kcPatchArray=[0 for i in range(numberOfFiles)]
rejectedArray =[ 0 for i in range(numberOfFiles)]
rmsValuesArray=[0.1 for i in range(numberOfFiles)]
rms2Array=[0.1 for i in range(numberOfFiles)]
iterationNumberArray=[0 for i in range(numberOfFiles)]


                                  
firstPlaceIndex = 0
secondPlaceIndex = 1
thirdPlaceIndex = 2




def openfile():
   global frequencies
   global j_low
   global j_high
   global k_low
   global k_high
   global jQuantumIncrements
   global kQuantumIncrements
   global uncertainties
   global numberOfLines
   global numberOfFiles

   filename = askopenfilename(parent=root)
   f = open(filename)
   #f.read()
   f.seek(0,2)
   fsize = f.tell()
   f.seek(max(fsize-1024,0), 0)
   lines = f.readlines()
   endIsAt = len(lines)
   for index in range (0,endIsAt):
      if('number of frequencies') in lines[index]:
         placesToSearch = lines[index].split()
         endOfPlacesToSearch = len(placesToSearch)
         numberOfLines = int(placesToSearch[endOfPlacesToSearch - 1])
         for secondIndex in range (0, numberOfLines):
            inputData = lines[index+1+secondIndex].split()
            frequencies[secondIndex] = float(inputData[0])
            jQuantumIncrements[secondIndex] = int(inputData[1])
            kQuantumIncrements[secondIndex] = int(inputData[2])
            
         index+= 1+secondIndex
      if('uncertainty') in lines[index]:
         placesToSearch = lines[index].split()
         endOfPlacesToSearch = len(placesToSearch)
         uncertainties[0] = float(placesToSearch[endOfPlacesToSearch - 1])        
         
      if('j_low') in lines[index]:
         placesToSearch = lines[index].split()
         endOfPlacesToSearch = len(placesToSearch)
         j_low = int(placesToSearch[endOfPlacesToSearch - 1])

      if('j_high') in lines[index]:
         placesToSearch = lines[index].split()
         endOfPlacesToSearch = len(placesToSearch)
         j_high = int(placesToSearch[endOfPlacesToSearch - 1])
      if('k_high') in lines[index]:
         placesToSearch = lines[index].split()
         endOfPlacesToSearch = len(placesToSearch)
         k_high = int(placesToSearch[endOfPlacesToSearch - 1])
      if('k_low') in lines[index]:
         placesToSearch = lines[index].split()
         endOfPlacesToSearch = len(placesToSearch)
         k_low = int(placesToSearch[endOfPlacesToSearch - 1])
         
   numberOfFiles = (j_high - j_low) * (k_high - k_low) * 2 - (j_high - j_low)
   
   f.close()

   
def openFitFile(fileIndex):
   print('fileIndex='+str(fileIndex))
   f1=open('test.fit')
   lines = f1.readlines()
   endIsAt = len(lines)
   for index in range (0,endIsAt):
      #line = f1.readline()
      if( 'rejected') in lines[index]:
         print('rejected*******************************************************************************')
         rejectedArray[fileIndex] =1
   for index in range (endIsAt-4,endIsAt):
      #line = f1.readline()
      if( 'RMS ERROR=') in lines[index]:
         print(lines[index])
         placesToSearch = lines[index].split()
         endOfPlacesToSearch = len(placesToSearch)
         rmsValuesArray[fileIndex] = float(placesToSearch[endOfPlacesToSearch - 1])
         rms2Array[fileIndex] = float(placesToSearch[endOfPlacesToSearch - 2])
         iterationNumberArray[fileIndex] = int(placesToSearch[endOfPlacesToSearch - 7])
         print(str(rmsValuesArray[fileIndex]))
         print(str(rms2Array[fileIndex]))
         print(str(iterationNumberArray[fileIndex]))
               
   f1.close()


   
def writeLinFile():
   #filename = 'test' + str(j)+'_'+str(k) + '_' +str(kcpatch)+ '.lin'
   filename = 'test.lin'

   outf = open(filename, 'w')
   for index in range (0,numberOfLines):
         lineToWrite = repr(j+1 + jQuantumIncrements[index]).rjust(3)+ str(k + kQuantumIncrements[index]).rjust(3)+ \
         str(kcpatch + j+1 + jQuantumIncrements[index] - (k + kQuantumIncrements[index]) ).rjust(3)+ \
         str(j + jQuantumIncrements[index]).rjust(3) +str(k + kQuantumIncrements[index]).rjust(3) +\
         str(kcpatch + j + jQuantumIncrements[index] -(k + kQuantumIncrements[index]   )).rjust(3)+ \
         repr(frequencies[index]).rjust(33) +  repr(uncertainties[index]).rjust(11) + '\n'
         # can also use spaces and literals, e.g.  '  '+ str(kcpatch + j+1 + jQuantumIncrements[index] - (k + kQuantumIncrements[index]) ).rjust(3)+ '  '+ \
         outf.write(lineToWrite)
      
   outf.close()            


def sort():
   if (rmsValuesArray[0] > rmsValuesArray[1]):
      if(rmsValuesArray[2] > rmsValuesArray[0]):
         firstPlaceIndex = 2
         secondPlaceIndex = 0
         thirdPlaceIndex = 1
      elif (rmsValuesArray[2] > rmsValuesArray[1]):
         firstPlaceIndex = 0
         secondPlaceIndex = 2
         thirdPlaceIndex = 1
      else:
         firstPlaceIndex = 0
         secondPlaceIndex = 1
         thirdPlaceIndex = 2
   else:
      if(rmsValuesArray[2] > rmsValuesArray[1]):
         firstPlaceIndex = 2
         secondPlaceIndex = 1
         thirdPlaceIndex = 0
      elif (rmsValuesArray[2] > rmsValuesArray[0]):
         firstPlaceIndex = 1
         secondPlaceIndex = 2
         thirdPlaceIndex = 0
      else:
         firstPlaceIndex = 1
         secondPlaceIndex = 0
         thirdPlaceIndex = 2

   print('First = ' +str(firstPlaceIndex))
   print('Second= ' +str(secondPlaceIndex))            
   print('Third = ' +str(thirdPlaceIndex))
   print(str(numberOfFiles))
   for index in range (3,numberOfFiles):
      if(rmsValuesArray[index] <=0):
         #do nothing in the case of = 0
         print('ZERO')
      elif(rms2Array[index]/rmsValuesArray[index] > 1.25):
         print('Non matching rms and rms2')
      elif (rms2Array[index]/rmsValuesArray[index] < .75):
         print('Non matching rms and rms2')
      elif (rejectedArray[index] == 1):
         print('Rejected by Fitter')
      elif (rmsValuesArray[index] < rmsValuesArray[firstPlaceIndex]):
         thirdPlaceIndex = secondPlaceIndex
         secondPlaceIndex = firstPlaceIndex
         firstPlaceIndex = index
      elif(rmsValuesArray[index] < rmsValuesArray[secondPlaceIndex]):
         thirdPlaceIndex = secondPlaceIndex
         secondPlaceIndex = index
      elif(rmsValuesArray[index] < rmsValuesArray[thirdPlaceIndex]):
         thirdPlaceIndex = index
      #print('First = ' +str(firstPlaceIndex))
      #print('Second= ' +str(secondPlaceIndex))            
      #print('Third = ' +str(thirdPlaceIndex))
      #print('index'+str(index))
         
   print('First (index)= ' +str(firstPlaceIndex))
   printParams(firstPlaceIndex)
   print('Second= ' +str(secondPlaceIndex))
   printParams(secondPlaceIndex)
   print('Third = ' +str(thirdPlaceIndex))
   printParams(thirdPlaceIndex)


               
def printParams(localIndex):
   print("Local Index ="+str(localIndex) )
   print('J=' +str(jArray[localIndex]))
   print('K=' +str(kArray[localIndex]))
   print('Kcpatch=' +str(kcPatchArray[localIndex]))
   print('RMS = ' +str(rmsValuesArray[localIndex]))
   print('rms2 = ' +str(rms2Array[localIndex]))
   print('iterations =' +str(iterationNumberArray[localIndex]))
      
      
   


root = Tk()
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=openfile)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

subprocess.call(["ls", '-l'])

root.config(menu=menubar)

files_written = 0
for j in range (j_low, j_high):
   for k in range (k_low, k_high):
      if(k !=0):
         loopLimit=2
      else:
         loopLimit = 1
      for kcpatch in range (0,loopLimit):
         writeLinFile()
         jArray[files_written] = j
         kArray[files_written] = k
         kcPatchArray[files_written] = kcpatch

         shutil.copy('test.parameters', 'test.par') # copy the parameters file to test.par
         subprocess.call(["spfit", 'test']) # run spfit
         print('index='+str(j)+','+str(k)+','+str(kcpatch))
         openFitFile(files_written) # open the test.fit file and return the rms value
         subprocess.call(["rm", 'test.par']) # delete the text.xyz files
         subprocess.call(["rm", 'test.bak']) # run spfit
         subprocess.call(["rm", 'test.var']) # run spfit
         files_written +=1

print (str(files_written) + ' Files Written')   
sort()




root.mainloop()


