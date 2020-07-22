# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 12:36:17 2018

@author: Greg
"""

import tkinter as tk

class Application(tk.Frame):
    
    def __init__(self,master):
        
        tk.Frame.__init__(self,master)
        self.grid()
        self.button_clicks=0
        self.button4_clicks=0
        self.create_widgets()
    
    def create_widgets(self):
        
        self.button1=tk.Button(self,text = "Button 1")
        self.button1.grid()
        
        self.button2=tk.Button(self)
        self.button2.grid()
        self.button2.configure(text="Button 2 text")
        
        self.button3=tk.Button(self)
        self.button3.grid()                
        self.button3["text"] = "Total Clicks = " + str(self.button_clicks)
        self.button3["command"]=self.update_count
        
        self.button4 = tk.Button(self)
        self.button4.grid()
        self.button4.configure(text="Button 4 clicks = "+str(self.button4_clicks))
        self.button4["command"]=self.update_count4
    
    def update_count(self):
        self.button_clicks +=1
        self.button3["text"]="Total Clicks = "+str(self.button_clicks)
    
    def update_count4(self):
        self.button4_clicks +=1
        self.button4.configure(text="Button 4 Clicks = "+str(self.button4_clicks))
        
root=tk.Tk()
root.title("More Buttons")
root.geometry("200x100")

app=Application(root)

root.mainloop()

