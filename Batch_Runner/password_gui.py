# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 13:01:17 2018

@author: Greg
"""

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
        self.create_widgets()
    
    def create_widgets(self):
        
        self.instruction=tk.Label(self,text = "Enter Password")
        self.instruction.grid(row=0,column=0,columnspan=2,sticky=tk.W)
        self.password = tk.Entry(self)
        self.password.grid(row=1,column=0,sticky="W")
        
        self.submit_button=tk.Button(self,text="Submit",command=self.reveal)
        self.submit_button.grid(row=2,column=0,sticky=tk.W)
        
        self.text = tk.Text(self,width=10,height=5,wrap=tk.WORD)
        self.text.grid(row=3,column=0,sticky=tk.W)
        
    def reveal(self):
        content=self.password.get()
        if content == "password":
            message = "You have access to the system"
        else:
            message = "Access denied"
        
        self.text.insert(0.0,message)

        
root=tk.Tk()
root.title("Python Reconstruction Batch Runner")
root.geometry("400x600")

app=Application(root)

root.mainloop()

