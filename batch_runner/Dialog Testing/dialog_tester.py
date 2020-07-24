# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 12:04:39 2017

@author: Greg
"""

# this works for Windows and Linux

#from chooseBatchFile import chooseBatchFile
#filename=chooseBatchFile()
#print(filename)

import tkinter as tk

root=tk.Tk()
root.title("My Window")
root.geometry("400x200")

app = tk.Frame(root)
app.grid()
#label = tk.Label(app,text="this is a label")
#label.grid()

button1=tk.Button(app,text = "My Button")
button1.grid()

button2=tk.Button(app)
button2.grid()
button2.configure(text="button 2 text")
                  
button3=tk.Button(app)
button3.grid()                
button3["text"] = "Button 3 text"

root.mainloop() 