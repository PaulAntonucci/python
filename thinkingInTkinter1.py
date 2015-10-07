from tkinter import *


class MyApp:
    def __init__(self, myParent):
        button_width = 20
        button_padx = "2m"
        button_pady = "1m"

        buttons_frame_padx = "3m"
        buttons_frame_pady = '5m'
        buttons_frame_ipadx = '30m'
        buttons_frame_ipady = '1m'
        
        self.commonVariable1 = 0
        self.commonVariable2 = None
        self.myParent = myParent
        self.myContainer1 = Frame(myParent)
        #self.myContainer1.pack()
        self.myContainer1.pack(
            ipadx = buttons_frame_ipadx,
            ipady = buttons_frame_ipady,
            padx = buttons_frame_padx,
            pady = buttons_frame_pady)
        
        self.button1 = Button(self.myContainer1, command = self.createFT)
        self.button1['text'] = 'Create FT'
        self.button1['background'] = 'white'
        self.button1.configure (
            width = button_width,
            padx = button_padx,
            pady = button_pady)
        self.button1.pack(side = TOP)
        self.button1.focus_force()
        #self.button1.bind('<Button-1>', self.createFT)
        self.button1.bind('<Return>', self.createFT_withEvent)       

        self.button2 = Button(self.myContainer1)
        self.button2.configure(text = "Remove Artifacts ")
        self.button2.configure(background = 'tan')
        self.button2.configure( width = button_width, padx = button_padx, pady = button_pady)
        self.button2.pack(side = TOP)
        self.button2.bind("<Button-1>", self.removeArtifacts)
        self.button2.bind("<Return>", self.removeArtifacts)

        self.button3 = Button(self.myContainer1, text = "Remove Contaminants")
        self.button3.configure(background = 'grey')
        self.button3.configure( width = button_width, padx = button_padx, pady = button_pady)
        self.button3.pack(side = TOP)
        self.button3.bind("<Button-1>", self.removeContaminants)
        self.button3.bind("<Return>", self.removeContaminants)    

        self.button4 = Button(self.myContainer1, text = "Remove Molecular Lines")
        self.button4.configure(background = 'tan')
        self.button4.configure( width = button_width, padx = button_padx, pady = button_pady)
        self.button4.pack(side = TOP)
        self.button4.bind("<Button-1>", self.removeMolecularLines)
        self.button4.bind("<Return>", self.removeMolecularLines)

        self.button5 = Button(self.myContainer1, text = 'Exit Button', command = self.exult)
        self.button5.pack(side = TOP)
        

    def createFT_withEvent(self, event):
        print ('mouse = ', str(event.x), str(event.y))
        report_event(event)
        self.createFT()
        self.commonVariable1 = 1

    def createFT(self): #, event):
        #report_event(event)
        print(' Creating FT')
        if(self.button1["background"] == "white"):
           self.button1['background'] = "tan"
        else:
           self.button1['background'] = 'white'
        if(self.commonVariable1 != 1):
            self.commonVariable1 = 2

    def removeArtifacts(self, event):
        print( ' removing Artifacts - now you know it is real ')
        self.commonVariable1 = 3

    def removeContaminants(self, event):
        print (" Removing contaminants ")
        self.commonVariable1 = 4

    def removeMolecularLines(self, event):
        print ('removing molecular lines')
        self.commonVariable1 = 5
        
    def exult(self):
        print ('Exulting and exiting')
        print ('Common variable 1 and 2 are', str(self.commonVariable1), self.commonVariable2)
        self.myParent.destroy()


def report_event(event):
    event_name = {"2": "Keypress", "4": 'Button Press'}
    print ("Reporting event \n mouse x and y: " + str(event.x), str(event.y))
    print ("Time =", str(event.time))
    print ('type =', str(event.type), event_name[str(event.type)])
    print ('EventWidgetId' + str(event.widget), 'eventKey symbol' +str(event.keysym))
           
           
           
        



root = Tk()

#myContainer1 = Frame(root)
#myContainer1.pack()
#button1 = Button(myContainer1)
#button1["text"] = "thi sis text too \n and more \n text"
#button1["background"] = 'green'
#button1.pack()
#root.mainloop()


myapp = MyApp(root)
root.mainloop()
