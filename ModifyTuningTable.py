from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
import subprocess
import shutil




#variables

j =1
k =2

def openfile():


   filename = askopenfilename(parent=root)
   f = open(filename)
   lines = f.readlines()
   endIsAt = len(lines)

   outlines = []

   outline = "fred"   

   for index in range (0,endIsAt):
      line = lines[index]
      fields = line.split()
      print(fields)
      print(fields[1])
      test = int(fields[1])
      if(test > 3):
         outline = fields[0] + "\t" + str(test - 4) + "\n"
      else:
         outline = fields[0] + "\t" + str(test) + "\n"
      print(outline)
      outlines.append(outline)   
      
   f.close()
   filename = 'TuningTableModifiedMAr21_2016.atn'
   outf = open(filename, 'w')
   
   for index in range (0,endIsAt):
      lineToWrite = outlines[index]
      print(lineToWrite)
      outf.write(lineToWrite)
        
   outf.close()





root = Tk()
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=openfile)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)


root.mainloop()


