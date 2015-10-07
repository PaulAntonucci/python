#!/usr/bin/env python3
from tkinter import *

root = Tk()

def key(event):
    print ('key is F# major', repr(event.char ))
    
def callback(event):
    frame.focus_set()
    print ('x = ' ,event.x)
    print ('y = ', event.y)
    
def buttonAlive():
    print ('Button Clicked')
    


frame = Frame(root, width = 300, height=300)
B = Button(root, text = "hello Button", command = buttonAlive)
B.pack()

#tkinter.
frame.bind("<Key>", key)
frame.bind("<Button-1>", callback)
frame.bind("<1>", buttonAlive)
frame.pack()

root.mainloop()
    
