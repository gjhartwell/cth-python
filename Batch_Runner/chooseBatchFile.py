# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 10:42:26 2018

@author: Greg
"""

# choose batch file
# asks user for the batchfile name

import tkinter as tk 
from tkinter import filedialog
import os

def chooseBatchFile():
    
    #check if enviroment variable RECONBASEDIR exists
    if "RECONBASEDIR" in os.environ:
        reconBaseDir = os.environ["RECONBASEDIR"]
    else:
        reconBaseDir="/"
    
    # first ask for the base directory where the reconstruction folders
    # will be placed 
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    filename = filedialog.askopenfilename(initialdir = reconBaseDir,
                                          parent=root,
                                 title = "Select a batch.cthsl type file",
                                 filetypes=(("CTH Files","*.cthsl"),
                                            ("Text File", "*.*")))
    #set RECONBASEDIR to latest path
    os.environ["RECONBASEDIR"]=os.path.dirname(filename)
    return filename


# testing routine
#file=chooseBatchFile()
#if not file:
#    print("no file chosen")
#else: 
#print(file)