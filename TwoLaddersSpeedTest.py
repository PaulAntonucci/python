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

frequencies =[7063.9800, 7822.1260, 7105.532, 7908.580, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, \
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
numberOfALadderLines = 4 #Could be len(frequencies) if array were populated
uncertainty = 00.1

numberOfCrossLadderLines = 0
crossLadderFrequencies = [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9]
jCrossLadderQuantumIncrements=  [0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0]

j_low =  5
j_high = 15
k_low =  0
k_high = 7


# dimension of array = (j_high - j_low) * (k_high - k_low) * 2 - (j_high - j_low) - for the instances when k = 0
numberOfFiles = (j_high - j_low) * (k_high - k_low) * 2 - (j_high - j_low)
maximumNumberOfFiles = 2000 # * numberOfFiles

jQuantumIncrements=  [0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0]
kQuantumIncrements = [0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0]

jArray=[0 for i in range(maximumNumberOfFiles)]
kArray=[0 for i in range(maximumNumberOfFiles)]
kcPatchArray=[0 for i in range(maximumNumberOfFiles)]
jbArray=[0 for i in range(maximumNumberOfFiles)]
kbArray=[0 for i in range(maximumNumberOfFiles)]
kbcArray=[0 for i in range(maximumNumberOfFiles)]
rejectedArray =[ 0 for i in range(maximumNumberOfFiles)]
badLineArray  = [ 0 for i in range(maximumNumberOfFiles)] 
rmsValuesArray=[0.1 for i in range(maximumNumberOfFiles)]
rms2Array=[0.1 for i in range(maximumNumberOfFiles)]
iterationNumberArray=[0 for i in range(maximumNumberOfFiles)]
                                  
firstPlaceIndex = 0
secondPlaceIndex = 1
thirdPlaceIndex = 2
maximumNumberOfFileLines = 30
LinesToWriteToFile=["hello" for i in range (maximumNumberOfFileLines)] # ??"first line", "second line", 'etc']  # data structure to hold lines to be written to Lin file
CrossLadderJ =[0 for i in range(0,10)]
CrossLadderK =[0 for i in range(0,10)]
CrossLadderKc=[0 for i in range(0,10)]

def openfile():
   global frequencies
   global j_low
   global j_high
   global k_low
   global k_high
   global jQuantumIncrements
   global kQuantumIncrements
   global uncertainty
   global numberOfALadderLines
   global numberOfFiles
   global crossLadderFrequencies
   global jCrossLadderQuantumIncrements
   global numberOfCrossLadderLines

   filename = askopenfilename(parent=root)
   f = open(filename)
   lines = f.readlines()
   endIsAt = len(lines)
   gotJA = 0;gotCross=0;gotUncertainty=0;gotj_low=0;gotj_high=0;gotk_low=0;gotk_high=0;
   for index in range (0,endIsAt):
      if('ja ladder number of frequencies') in lines[index]:
         placesToSearch = lines[index].split()
         endOfPlacesToSearch = len(placesToSearch)
         numberOfALadderLines = int(placesToSearch[endOfPlacesToSearch - 1])
         for secondIndex in range (0, numberOfALadderLines):
            inputData = lines[index+1+secondIndex].split()
            frequencies[secondIndex] = float(inputData[0])
            jQuantumIncrements[secondIndex] = int(inputData[1])
            kQuantumIncrements[secondIndex] = int(inputData[2])
            
         index+= 1+secondIndex

      if('cross ladder frequencies and Ja') in lines[index]:
         placesToSearch = lines[index].split()
         endOfPlacesToSearch = len(placesToSearch)
         numberOfCrossLadderLines = int(placesToSearch[endOfPlacesToSearch - 1])
         for secondIndex in range (0, numberOfCrossLadderLines):
            inputData = lines[index+1+secondIndex].split()
            crossLadderFrequencies[secondIndex] = float(inputData[0])
            jCrossLadderQuantumIncrements[secondIndex] = int(inputData[1])
            # kQuantumIncrements[secondIndex] = int(inputData[2])
            print("cross ladder" + str(crossLadderFrequencies[secondIndex]))
            
         index+= 1+secondIndex

    
      if('uncertainty') in lines[index]:
         placesToSearch = lines[index].split()
         endOfPlacesToSearch = len(placesToSearch)
         uncertainty = float(placesToSearch[endOfPlacesToSearch - 1])          
         
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
         
   if(numberOfCrossLadderLines != 0):
      newNumberOfFiles = ((j_high - j_low) * (k_high - k_low) * 2 - (j_high - j_low)) * (numberOfCrossLadderLines)*8
   else:
      newNumberOfFiles = (j_high - j_low) * (k_high - k_low) * 2 - (j_high - j_low)
   if(newNumberOfFiles>maximumNumberOfFiles):
       print('Too Many files required !!  RE-dimension the arrays')
       
   print(str(crossLadderFrequencies[0]),str(crossLadderFrequencies[1]), \
   str(jCrossLadderQuantumIncrements[0]),str(jCrossLadderQuantumIncrements[1]))
   numberOfFiles = newNumberOfFiles
   f.close()
   processInputTextFile()
   
def processFitFile(fileIndex):
   # timing print('fileIndex='+str(fileIndex))

   CrossLineState = 1 # 1 if it's all fine, -1 is reversal is required
   f1=open('test.fit')
   lines = f1.readlines()     
   f1.close()
   endIsAt = len(lines)
   for index in range (0,endIsAt):
      if( 'rejected') in lines[index]:
         # timing print('rejected****************************************')
         rejectedArray[fileIndex] =1
      if( 'Bad Line') in lines[index]:
         # timing print('Bad Line****************************************')
         badLineArray[fileIndex] =1

   for index in range (endIsAt - 10,endIsAt-4):
      if( (( '10000') in lines[index]) or  (('20000') in lines[index])or (('30000') in lines[index]) )  :
         # then split the line and look for negative numbers
         placesToSearch = lines[index].split()
         endOfPlacesToSearch = len(placesToSearch)         
         if( '-') in placesToSearch[endOfPlacesToSearch -2]:
            # timing print('Need to Reverse the order of Cross line quantum numbers **********************')
            # timing print(lines[index])
            CrossLineState = -1

   for index in range (endIsAt-4,endIsAt):
      if( 'RMS ERROR=') in lines[index]:
         # timing print(lines[index])
         placesToSearch = lines[index].split()
         endOfPlacesToSearch = len(placesToSearch)
         rmsValuesArray[fileIndex] = float(placesToSearch[endOfPlacesToSearch - 1])
         rms2Array[fileIndex] = float(placesToSearch[endOfPlacesToSearch - 2])
         iterationNumberArray[fileIndex] = int(placesToSearch[endOfPlacesToSearch - 7])
         #print(str(rmsValuesArray[fileIndex]))
         #print(str(rms2Array[fileIndex]))
         #print(str(iterationNumberArray[fileIndex]))


   if((fileIndex == 113) or (fileIndex == 117) or (fileIndex == 118)):
   #    test.fit
      filename = 'test' + str(fileIndex)
      outf = open(filename, 'w')  
      for index in range (0,endIsAt):
         lineToWrite = lines[index]
         outf.write(lineToWrite)  
      outf.close()
   return(CrossLineState)


   
def writeLinFile():
   global LinesToWriteToFile
   #filename = 'test' + str(j)+'_'+str(k) + '_' +str(kcpatch)+ str(filesWritten) + '.lin'
   filename = 'test.lin'

   outf = open(filename, 'w')
   
   for index in range (0,numberOfALadderLines + numberOfCrossLadderLines):
      lineToWrite = LinesToWriteToFile[index]
      outf.write(lineToWrite)
        
   outf.close()

   # or maybe save the A lines . . . . 
                       



def writeALadderLines():
   global LinesToWriteToFile
   #filename = 'test' + str(j)+'_'+str(k) + '_' +str(kcpatch)+ '.lin'
   for index in range (0,numberOfALadderLines):
       
         lineToWrite = repr(j+1 + jQuantumIncrements[index]).rjust(3)+ str(k + kQuantumIncrements[index]).rjust(3)+ \
         str(kcpatch + j+1 + jQuantumIncrements[index] - (k + kQuantumIncrements[index]) ).rjust(3)+ \
         str(j + jQuantumIncrements[index]).rjust(3) +str(k + kQuantumIncrements[index]).rjust(3) +\
         str(kcpatch + j + jQuantumIncrements[index] -(k + kQuantumIncrements[index]   )).rjust(3)+ \
         repr(frequencies[index]).rjust(33) +  repr(uncertainty).rjust(11) + '\n'
         # can also use spaces and literals, e.g.  '  '+ str(kcpatch + j+1 + jQuantumIncrements[index] - (k + kQuantumIncrements[index]) ).rjust(3)+ '  '+ \
         LinesToWriteToFile[index] = lineToWrite

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
      elif (badLineArray[index] == 1):
         print('Bad Line found by Fitter')
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
   print('Jcross=' +str(jbArray[localIndex]))
   print('Kcross=' +str(kbArray[localIndex]))
   print('Kbcross=' +str(kbcArray[localIndex]))   
   print('RMS = ' +str(rmsValuesArray[localIndex]))
   print('rms2 = ' +str(rms2Array[localIndex]))
   print('iterations =' +str(iterationNumberArray[localIndex]))
      

      
def processInputTextFile():
    global j
    global k
    global kc
    global jArray
    global kArray
    global kcPatchArray
    global kcpatch
    global jbArray
    global kbArray
    global kbcArray
    global LinesToWriteToFile

    
    files_written = 0
    
    for j in range (j_low, j_high):
       for k in range (k_low, k_high):
          if(k !=0):
             loopLimit=2
          else:
             loopLimit = 1
          for kcpatch in range (0,loopLimit):
             kcLocal =   kcpatch + (j+jCrossLadderQuantumIncrements[0])-k
             writeALadderLines()    # puts them in the structure LinesToWriteToFile, clearing it first
             generateCrossLadderMatrix(j+jCrossLadderQuantumIncrements[0],k, kcLocal)
             for index in range (0,8):
                   # in principle, what we are doing is this:  lineToWrite = str(CrossLadderMatrix[index])
                   # but the formatting is such as mess . . .
                   lineToWrite = createCrossLadderLine(j+jCrossLadderQuantumIncrements[0],k, kcLocal, \
                                                       CrossLadderJ[index], CrossLadderK[index], CrossLadderKc[index])
                  
                   # timing print('Next Cross Ladder Line to Try: ' + lineToWrite)
                   LinesToWriteToFile[numberOfALadderLines] = lineToWrite
                   jArray[files_written]  =  j;                   kArray[files_written] = k;    kcPatchArray[files_written] = kcpatch
                   jbArray[files_written] =  CrossLadderJ[index]; kbArray[files_written] = CrossLadderK[index]
                   kbcArray[files_written]=  CrossLadderKc[index]
                   
                   writeLinFile()
                   shutil.copy('test.parameters', 'test.par') # copy the parameters file to test.par
                   subprocess.call(["spfit", 'test']) # run spfit
                   # timing print('index='+str(j)+','+str(k)+','+str(kcpatch))
                   returnValue = processFitFile(files_written) # open the test.fit file, test for various problems including
                   # negative values for A, B, C,  (in which case switch order of cross ladder lines), and get the rms value in array for sorting
                   if(returnValue == -1):
                      lineToWrite = createCrossLadderLine(CrossLadderJ[index], CrossLadderK[index], CrossLadderKc[index], j+jCrossLadderQuantumIncrements[0],k, kcLocal)
                      LinesToWriteToFile[numberOfALadderLines] = lineToWrite
                      writeLinFile()
                      shutil.copy('test.parameters', 'test.par') # copy the parameters file to test.par
                      subprocess.call(["spfit", 'test']) # run spfit
                      # timing print('Reversing Cross Ladder line - index='+str(j)+','+str(k)+','+str(kcpatch))
                      processFitFile(files_written)
                   subprocess.call(["rm", 'test.par']) # delete the text.xyz files
                   subprocess.call(["rm", 'test.bak']) # run spfit
                   subprocess.call(["rm", 'test.var']) # run spfit                          
                   files_written +=1

    print (str(files_written) + ' Files Written')   
    sort()
    print('BestFitFinderwithCrossLadder.py')
    print (str(files_written) + ' Files Written')

def generateCrossLadderMatrix(j_passed,k, kc):
         if (kc == j_passed-k):
             jb  = j_passed + 1
             kb = k + 1
             kbc = kc + 1
             # timing print ("B type transition - delta J=+1  j,k,kc,jb,kb,kbc " ,str(j_passed),str(k),str(kc),str(jb),str(kb),str(kbc))
             CrossLadderJ[0] = jb; CrossLadderK[0] = kb; CrossLadderKc[0] = kbc

         else:
             jb  = j_passed + 1
             kb = k  -1
             kbc = kc + 1
             # timing print ("B type transition - delta J=+1  j,k,kc,jb,kb,kbc " ,str(j_passed),str(k),str(kc),str(jb),str(kb),str(kbc))
             CrossLadderJ[0] = jb; CrossLadderK[0] = kb; CrossLadderKc[0] = kbc
             jb  = j_passed +1
             kb = k +1
             kbc = kc - 1
             # timing print ("B type transition - delta J=+1  j,k,kc,jb,kb,kbc " ,str(j_passed),str(k),str(kc),str(jb),str(kb),str(kbc))
             CrossLadderJ[1] = jb; CrossLadderK[1] = kb; CrossLadderKc[1] = kbc
         if (kc != j_passed-k):
             jb  = j_passed - 1
             kb = k - 1
             kbc = kc - 1
             # timing print ("B type transition - delta J=-1  j,k,kc,jb,kb,kbc " ,str(j_passed),str(k),str(kc),str(jb),str(kb),str(kbc))
             CrossLadderJ[2] = jb; CrossLadderK[2] = kb; CrossLadderKc[2] = kbc
         else:
             jb  = j_passed - 1
             kb = k  -1
             kbc = kc + 1
             # timing print ("B type transition - delta J=-1  j,k,kc,jb,kb,kbc " ,str(j_passed),str(k),str(kc),str(jb),str(kb),str(kbc))
             CrossLadderJ[1] = jb; CrossLadderK[1] = kb; CrossLadderKc[1] = kbc
             jb  = j_passed - 1
             kb = k +1
             kbc = kc - 1
             # timing print ("B type transition - delta J=-1  j,k,kc,jb,kb,kbc " ,str(j_passed),str(k),str(kc),str(jb),str(kb),str(kbc))
             CrossLadderJ[2] = jb; CrossLadderK[2] = kb; CrossLadderKc[2] = kbc
         # delta j = 0 transitions
         jb = j_passed
         kb = k - 1
         kbc = kc + 1
         # timing print ("B type transition - delta J= 0  j,k,kc,jb,kb,kbc " ,str(j_passed),str(k),str(kc),str(jb),str(kb),str(kbc))
         CrossLadderJ[3] = jb; CrossLadderK[3] = kb; CrossLadderKc[3] = kbc
         kb = k+1
         kbc = kc -1
         # timing print ("B type transition - delta J= 0  j,k,kc,jb,kb,kbc " ,str(j_passed),str(k),str(kc),str(jb),str(kb),str(kbc))
         CrossLadderJ[4] = jb; CrossLadderK[4] = kb; CrossLadderKc[4] = kbc         



         # C type transition   - delta Kc = 0 for all C type
         kbc = kc    
         jb = j_passed+1
         kb = k +1
         # timing print ("C type transition - delta J=+1  j,k,kc,jb,kb,kbc " ,str(j_passed),str(k),str(kc),str(jb),str(kb),str(kbc))
         CrossLadderJ[5] = jb; CrossLadderK[5] = kb; CrossLadderKc[5] = kbc
         jb = j_passed-1
         kb = k-1
         # timing print ("C type transition - delta J=-1  j,k,kc,jb,kb,kbc " ,str(j_passed),str(k),str(kc),str(jb),str(kb),str(kbc))
         CrossLadderJ[6] = jb; CrossLadderK[6] = kb; CrossLadderKc[6] = kbc
         if(kc == j_passed-k):
             jb = j_passed
             kb = k + 1
         else:
             jb = j_passed
             kb = k - 1
         # timing print ("C type transition - delta J= 0  j,k,kc,jb,kb,kbc " ,str(j_passed),str(k),str(kc),str(jb),str(kb),str(kbc))
         CrossLadderJ[7] = jb; CrossLadderK[7] = kb; CrossLadderKc[7] = kbc

def createCrossLadderLine(jl,kl,kcl,jbl,kbl,kbcl):
         lineToAdd = repr(jbl).rjust(3)+ str(kbl).rjust(3)+  str(kbcl).rjust(3)+ \
         str(jl).rjust(3) +str(kl).rjust(3) + str(kcl).rjust(3)+ \
         repr(crossLadderFrequencies[0]).rjust(33) +  repr(uncertainty).rjust(11) + '\n'
         # can also use spaces and literals, e.g.  '  '+ str(kcpatch + j+1 + jQuantumIncrements[index] - (k + kQuantumIncrements[index]) 
         return(lineToAdd)



root = Tk()
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=openfile)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)

# processInputTextFile()


##for j in range (5,8):
##    for k in range (1,3):
##        for kc in [j-k,j-k+1]:
##            # first do A type transitions - delta Kb = 0 for all A type
##            jb = j+1
##            kb = k
##            kbc = kc +1
##            print ("A type transition - new j,k,kc - delta J=+1  j,k,kc,jb,kb,kbc " ,str(j),str(k),str(kc),str(jb),str(kb),str(kbc))
##
##            # next B-type
##            if (kc == j-k):
##                jb  = j + 1
##                kb = k + 1
##                kbc = kc + 1
##
##                print ("B type transition - delta J=+1  j,k,kc,jb,kb,kbc " ,str(j),str(k),str(kc),str(jb),str(kb),str(kbc))
##            else:
##                jb  = j + 1
##                kb = k  -1
##                kbc = kc + 1
##                print ("B type transition - delta J=+1  j,k,kc,jb,kb,kbc " ,str(j),str(k),str(kc),str(jb),str(kb),str(kbc))
##           
##                jb  = j +1
##                kb = k +1
##                kbc = kc - 1
##                print ("B type transition - delta J=+1  j,k,kc,jb,kb,kbc " ,str(j),str(k),str(kc),str(jb),str(kb),str(kbc))
##
##
##
##            if (kc != j-k):
##                jb  = j - 1
##                kb = k - 1
##                kbc = kc - 1
##
##                print ("B type transition - delta J=-1  j,k,kc,jb,kb,kbc " ,str(j),str(k),str(kc),str(jb),str(kb),str(kbc))
##            else:
##                jb  = j - 1
##                kb = k  -1
##                kbc = kc + 1
##                print ("B type transition - delta J=-1  j,k,kc,jb,kb,kbc " ,str(j),str(k),str(kc),str(jb),str(kb),str(kbc))
##           
##                jb  = j - 1
##                kb = k +1
##                kbc = kc - 1
##                print ("B type transition - delta J=-1  j,k,kc,jb,kb,kbc " ,str(j),str(k),str(kc),str(jb),str(kb),str(kbc))
##
##
##            # delta j = 0 transitions
##            jb = j
##            kb = k - 1
##            kbc = kc + 1
##            print ("B type transition - delta J= 0  j,k,kc,jb,kb,kbc " ,str(j),str(k),str(kc),str(jb),str(kb),str(kbc))
##            kb = k+1
##            kbc = kc -1
##            print ("B type transition - delta J= 0  j,k,kc,jb,kb,kbc " ,str(j),str(k),str(kc),str(jb),str(kb),str(kbc))
##            
##
##
##
##            # C type transition   - delta Kc = 0 for all C type
##            kbc = kc    
##            jb = j+1
##            kb = k +1
##            print ("C type transition - delta J=+1  j,k,kc,jb,kb,kbc " ,str(j),str(k),str(kc),str(jb),str(kb),str(kbc))
##            jb = j-1
##            kb = k-1
##            print ("C type transition - delta J=-1  j,k,kc,jb,kb,kbc " ,str(j),str(k),str(kc),str(jb),str(kb),str(kbc))
##            if(kc == j-k):
##                jb = j
##                kb = k + 1
##            else:
##                jb = j
##                kb = k - 1
##            print ("C type transition - delta J= 0  j,k,kc,jb,kb,kbc " ,str(j),str(k),str(kc),str(jb),str(kb),str(kbc))
##
##            









            
            
            

 



root.mainloop()


