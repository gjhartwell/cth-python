# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 15:56:22 2018

@author: Greg
"""



# makerecondirs.py
# creates the directory structure for the reconstructions

# To Do
#
# 
# June 29, 2020 - modified to use batch file base directory
#               - instead of asking user for directory

import os
import tkinter as tk 
from tkinter import filedialog

def makeReconDirs(batch_file_contents):
    
    # first ask for the base directory where the reconstruction folders
    # will be placed  
    # -------------------
    # this section asks user for the base directory to store files.
    # I don't want to do this, so skip and use the bfc.filename to 
    # get the base directory
    # root = tk.Tk()
    # root.attributes("-topmost", True)
    # root.withdraw()
    # windowTitle="Please select a directory to store reconstructions"
    # dirname = filedialog.askdirectory(parent=root,
    #                                   initialdir=os.environ["RECONBASEDIR"],
    #                                   title=windowTitle)
    # -----
    
    dirname=os.path.dirname(os.path.abspath(batch_file_contents.filename))
    
    if dirname != '':
        # move to the base directory
        os.chdir(dirname)
        
        # get the list of shots
        # a directory is created for each shot
        shotTimeArray=batch_file_contents.getShotTimeArray()
        
        #ensure that the directories do not exist
        pathok = True
        for shot in shotTimeArray:
            newpath=os.path.join(dirname,str(shot.shotnumber))
            if os.path.exists(newpath):
                print("directory already exists: ",newpath)
                pathok = False
        
        # if directories do not exist, create them
        if pathok:
            for shot in shotTimeArray:
                newpath=os.path.join(dirname,str(shot.shotnumber))
                os.makedirs(newpath)
        # otherwise, find a new directory
        else:
            print("bad dir")
    else:
        print("need a new base directory")
        
    
        
    
