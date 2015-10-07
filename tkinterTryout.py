#!/usr/bin/env python3

import tkinter as tk
class Application(tk.Frame):
    def __init__(self, master = None):
        tk.Frame.__init__(self, master, width = 300, height = 300)
        self.grid_propagate(0)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
            self.anotherButton = tk.Button(self, text = "A New Button", command = self.newText)
            self.anotherButton.grid()

            self.aThirdButton = tk.Button(self, text = "A Third Button", command = self.thirdText)
            self.aThirdButton.grid()                              
            self.quitButton = tk.Button(self, text = "Quit - ", command = self.quit)
            self.quitButton.grid(row=6,column=9, columnspan = 1, sticky=tk.S, rowspan =20, ipadx =5, ipady = 10)

    def newText(self):
            print('NewText')

    def thirdText(self):
        print('The Third Button')


app = Application()
app.master.title ('who believes this')
app.mainloop()
                                        

                                        
        
