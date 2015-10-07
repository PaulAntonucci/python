from tkinter import *
from tkinter import filedialog #import askopenfilename

from tkinter.filedialog import askopenfilename

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
        CB1 = IntVar()
        CB2 = IntVar()
        CB3 = IntVar()
        CB4 = IntVar()
        CBOCS = IntVar()
        CBH2O2 = IntVar()
        CBSO2 = IntVar()
        CBC = IntVar()
        CBS = IntVar()
        CBO = IntVar()
        CBH = IntVar()
        CBSi= IntVar()
        CBN = IntVar()
        
        self.myParent = myParent
        self.myContainer1 = Frame(myParent)
        #self.myContainer1.grid()
        self.myContainer1.grid(
            ipadx = buttons_frame_ipadx,
            ipady = buttons_frame_ipady,
            padx = buttons_frame_padx,
            pady = buttons_frame_pady)

        Label(self.myContainer1, text="Current File", height=3, width = 20).grid(row = 0, column = 0)
        e1 = Entry(self.myContainer1, bg = 'white')
        e1.grid(row = 0, column = 1)
        Label(self.myContainer1, text="Frequency Range", height =3).grid(row = 1, column = 0)
        cb1 = Spinbox(self.myContainer1, values = ("4 - 8 GHz", "8 - 18 GHz", "18 - 26GHz"), bg = 'white', width = 15)
        cb1.grid(row = 1, column = 1)
        
        self.button1 = Button(self.myContainer1, command = self.createFT)
        self.button1['text'] = 'Create FT'
        self.button1['background'] = button_background
        self.button1.configure (
            width = button_width,
            padx = button_padx,
            pady = button_pady)
        self.button1.grid(row=2, column=0)
        self.button1.focus_force()
        #self.button1.bind('<Button-1>', self.createFT)
        self.button1.bind('<Return>', self.createFT_withEvent)
        
        self.checkBox1 = Checkbutton(self.myContainer1, text = "FT Done", variable = CB1, onvalue=1,offvalue=0)#height=3,width=20)
        self.checkBox1.grid(row=2, column = 1, sticky = W) #note sticky = W has no effect if using height=, width=
        #Label(self.myContainer1, text="Window").grid(row=2, column=2)
        Label(self.myContainer1, text="Window").place(x=300, y = 97
                                                      )
        cb2 =Spinbox(self.myContainer1, width = 8, values=("Gaussian","Rectangle","Hann", "Hamming", "Cosine"), bg = 'white').grid(row=2,column=3)
        


        self.button2 = Button(self.myContainer1)
        self.button2.configure(text = "Remove Artifacts ")
        self.button2.configure(background = button_background)#'tan')
        self.button2.configure( width = button_width, padx = button_padx, pady = button_pady)
        self.button2.grid(row=10, column =0)
        self.button2.bind("<Button-1>", self.removeArtifacts)
        self.button2.bind("<Return>", self.removeArtifacts)

        self.checkBox2 = Checkbutton(self.myContainer1, text = "Artifacts Removed", variable = CB2,\
                                     onvalue=1,offvalue=0,height=3,width=20)
        self.checkBox2.grid(row=10, column = 1)

        

        self.button3 = Button(self.myContainer1, text = "Remove Contaminants")
        self.button3.configure(background = button_background)
        self.button3.configure( width = button_width, padx = button_padx, pady = button_pady)
        self.button3.grid(row=20, column = 0)
        self.button3.bind("<Button-1>", self.removeContaminants)
        self.button3.bind("<Return>", self.removeContaminants)

        self.checkBox3 = Checkbutton(self.myContainer1, text = "Contaminents Removed", variable = CB3,\
                                     onvalue=1,offvalue=0,height=1,width=20)
        self.checkBox3.grid(row=20, column = 1)

        self.checkBox4 = Checkbutton(self.myContainer1, text = "OCS", variable = CBOCS, onvalue=1,offvalue=0).grid(row=21,column=0, sticky = W)
        self.checkBox5 = Checkbutton(self.myContainer1, text = "(H2O)2", variable = CBH2O2, onvalue=1,offvalue=0).grid(row=22, column = 0, sticky = W)
        self.checkBox6 = Checkbutton(self.myContainer1, text = "SO2", variable = CBSO2, onvalue=1,offvalue=0)
        self.checkBox6.grid(row=23, column = 0, sticky = W)

        

        self.button4 = Button(self.myContainer1, text = "Remove Molecular Lines")
        self.button4.configure(background = button_background)#tan')
        self.button4.configure( width = button_width, padx = button_padx, pady = button_pady)
        self.button4.grid(row=30, column = 0)
        self.button4.bind("<Button-1>", self.removeMolecularLines)
        self.button4.bind("<Return>", self.removeMolecularLines)

        self.checkBox10 = Checkbutton(self.myContainer1, text = "Molecular Lines Removed", variable = CB4,onvalue=1,offvalue=0,height=3,width=20)
        self.checkBox10.grid(row=30, column = 1)
        self.label2 = Label(self.myContainer1, text = "Atoms Present")
        self.label2.grid(row=31, column = 0)
        self.checkBox11 = Checkbutton(self.myContainer1, text = "C", variable = CBC, onvalue=1,offvalue=0).place(x=75,y=elementsYOffset)
        self.checkBox12 = Checkbutton(self.myContainer1, text = "S", variable = CBS, onvalue=1,offvalue=0).place(x=150, y=elementsYOffset)
        self.checkBox13 = Checkbutton(self.myContainer1, text = "O", variable = CBO, onvalue=1,offvalue=0)
        #self.checkBox13.grid(row=32, column = 2)
        self.checkBox13.place(x = 225,y=elementsYOffset)
        self.checkBox14 = Checkbutton(self.myContainer1, text = "H", variable = CBH, onvalue=1,offvalue=0).place(x=75,y=elementsYOffset + 25)
        self.checkBox15 = Checkbutton(self.myContainer1, text = "Si", variable = CBSi, onvalue=1,offvalue=0).place(x=150,y=elementsYOffset + 25)
        self.checkBox16 = Checkbutton(self.myContainer1, text = "N", variable = CBN, onvalue=1,offvalue=0)
        self.checkBox16.place(x=225, y = elementsYOffset +25)

        self.label2 = Label(self.myContainer1, text = "Additional Atoms")
        self.label2.place(x=40, y = elementsYOffset + 50)
        
        cb3 = Spinbox(self.myContainer1, values = ("Choose", "He", "Li", "Be", "B", "F", "Ne", "Na", "Mg", "Al", "Si", "P", "Cl", "Ar", "K", "Ca"), width = 10)
        cb3.place (x = 75, y = elementsYOffset + 83)
        
        self.button5 = Button(self.myContainer1, text = "Add Atom", bg = button_background)
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


        

    def createFT_withEvent(self, event):
        print ('mouse = ', str(event.x), str(event.y))
        report_event(event)
        self.createFT()
        self.commonVariable1 = 1
        CB1 = 1
        self.checkBox1.select()

    def createFT(self): #, event):
        #report_event(event)
        print(' Creating FT')
        if(self.button1["background"] == "white"):
           self.button1['background'] = "gray"
        else:
           self.button1['background'] = 'white'
        if(self.commonVariable1 != 1):
            self.commonVariable1 = 2
        self.checkBox1.select()

    def removeArtifacts(self, event):
        print( ' removing Artifacts - now you know it is real ')
        self.commonVariable1 = 3
        self.checkBox2.select()

    def removeContaminants(self, event):
        print (" Removing contaminants ")
        self.commonVariable1 = 4
        self.checkBox3.select()

    def removeMolecularLines(self, event):
        print ('removing molecular lines')
        self.commonVariable1 = 5
        self.checkBox10.select()
    def addAdditionalElement(self, event):
        print ('adding additional element', self.cb3.get())
        
    def exult(self):
        print ('Exulting and exiting')
        print ('Common variable 1 and 2 are', str(self.commonVariable1), self.commonVariable2)
        self.myParent.destroy()


           
def openFile():
    filename = askopenfilename(parent=root)
    print ("Filename = ", filename)
    e1.delete(0,END)
    e1.insert(0,filename)
        

def report_event(event):
        event_name = {"2": "Keypress", "4": 'Button Press'}
        print ("Reporting event \n mouse x and y: " + str(event.x), str(event.y))
        print ("Time =", str(event.time))
        print ('type =', str(event.type), event_name[str(event.type)])
        print ('EventWidgetId' + str(event.widget), 'eventKey symbol' +str(event.keysym))
           
        



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
