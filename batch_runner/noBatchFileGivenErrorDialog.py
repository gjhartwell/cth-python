# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 08:15:42 2018

@author: Greg
"""

# noBatchFileGivenErrorDialog
import tkinter as tk

def noBatchFileGivenErrorDialog(window):
        
    noBatchFileLabel=tk.Label(text = "No Batch File Given -" 
                                       "Please select a Batch.cthsl file")  
    noBatchFileLabel.grid(row=0,column=0,columnspan=3,
                             padx=10,pady=20,sticky=tk.W)
    
    button1=tk.Button(text = "OK",command=gotOK)
    button1.grid(row=1,column=0,padx=50,pady=20)
    
    button2=tk.Button(text="Cancel",command=gotCancel)
    button2.grid(row=1,column=1,padx=10,pady=20)
    button2.configure(text="Cancel")
    

def gotOK():
    print("got OK")
    tryAgain=True
    destroy()
    quit()
    
def gotCancel():
    print("got Cancel")
    tryAgain=False
    destroy()
    quit()
        


    nBFGED=tk.Tk()
    nBFGED.title("No Batch File Given")
    nBFGED.geometry("300x150")
    noBatchFileGivenErrorDialogWindow(nBFGED)
    nBFGED.mainloop()
    return app.tryAgain
    
print(noBatchFileGivenErrorDialog())
