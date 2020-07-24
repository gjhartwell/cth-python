# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 13:15:44 2018

@author: Greg Hartwell


Notes: 
GJH Jul 24 2020
Provides a GUI interface for the batch runner code
Interface opens, but does not run vatch_runner code.

runBatchMain (line 164) is area where code would run


"""

# Python Batch Runner

import tkinter as tk
from chooseBatchFile import chooseBatchFile
import readBatchFile
from makeReconDirs import makeReconDirs

class Server(object):
    def __init__(self):
        self.address="131.204.212.162"
        self.address="recon2.physics.auburn.edu"
        self.port=2003
        self.timeout=120
    
    def print(self):
        print("Host    - ",self.address)
        print("Port    - ",self.port)
        print("Timeout - ",self.timeout)

class DataTimeInterval(object):
    def __init__(self):
        self.start=0.0
        self.stop=0.0
        
    def print(self):
        print("StartTime    - ",self.start)
        print("StopTime     - ",self.stop)

        
class BatchRunner(tk.Frame):
    
    def __init__(self,master):
        
        tk.Frame.__init__(self,master)
        self.grid()
        self.create_widgets()
        self.batchFileName=""
        self.server=Server()
        self.dataTimeInterval=DataTimeInterval()
        self.numberOutputFiles=5
        self.userName="java-client"
        self.dataHost="MDS"
        self.autoShotTime=True
        self.serverAddressEntry.insert(0,self.server.address)
        self.serverPortEntry.insert(0,str(self.server.port))
        self.serverTimeoutEntry.insert(0,str(self.server.timeout))
        self.dataStartEntry.insert(0,str(self.dataTimeInterval.start))
        self.dataStopEntry.insert(0,str(self.dataTimeInterval.stop))
        self.numberOutputFilesEntry.insert(0,str(self.numberOutputFiles))
        self.userNameEntry.insert(0,self.userName)
    
    def create_widgets(self):
        #batch file items
        self.batchFileLabel=tk.Label(self,text = "Batch File")
        self.batchFileLabel.grid(row=0,column=0,columnspan=3,
                                 padx=10,pady=1,sticky=tk.W)
        
        self.batchFileNameEntry = tk.Entry(self)
        self.batchFileNameEntry.grid(row=1,column=0,columnspan=3,
                                padx=10,sticky=tk.W)
        self.batchFileNameEntry.config(width=70)
        
        self.getBatchButton=tk.Button(self,text="Get Batch File",
                                      command=self.getBatchFile)
        self.getBatchButton.grid(row=1,column=3,sticky=tk.W)
        

        # server information
        self.serverAddressEntryLabel=tk.Label(self,text = "Server Address")
        self.serverAddressEntryLabel.grid(row=2,column=0,padx=10,sticky=tk.E)
        self.serverAddressEntry = tk.Entry(self)
        self.serverAddressEntry.grid(row=2,column=1,sticky=tk.W)
        self.serverAddressEntry.config(width=25)
        
        self.serverPortEntryLabel=tk.Label(self,text = "Port")
        self.serverPortEntryLabel.grid(row=3,column=0,padx=10,sticky=tk.E)
        self.serverPortEntry = tk.Entry(self)
        self.serverPortEntry.grid(row=3,column=1,sticky=tk.W)
        self.serverPortEntry.config(width=10)
        
        self.serverTimeoutEntryLabel=tk.Label(self,text = "Timeout(s)")
        self.serverTimeoutEntryLabel.grid(row=4,column=0,padx=10,sticky=tk.E)        
        self.serverTimeoutEntry = tk.Entry(self)
        self.serverTimeoutEntry.grid(row=4,column=1,sticky=tk.W)
        self.serverTimeoutEntry.config(width=10)
        
        # the Auto Shot Time option
        self.autoShotTimeVar=tk.IntVar()
        self.autoShotTimeCheckbutton=tk.Checkbutton(var=self.autoShotTimeVar,
                                                    text="Auto Data Time")
        self.autoShotTimeCheckbutton.grid(row=6,column=0,padx=10,sticky=tk.W)
        self.autoShotTimeVar.set(True)
        
        # data time entries
        self.dataStartEntryLabel=tk.Label(self,text = "Data Start")
        self.dataStartEntryLabel.grid(row=6,column=0,padx=10,sticky=tk.E)        
        self.dataStartEntry = tk.Entry(self)
        self.dataStartEntry.grid(row=6,column=1,sticky=tk.W)
        self.dataStartEntry.config(width=10)
        
        self.dataStopEntryLabel=tk.Label(self,text = "Data Stop")
        self.dataStopEntryLabel.grid(row=7,column=0,padx=10,sticky=tk.E)        
        self.dataStopEntry = tk.Entry(self)
        self.dataStopEntry.grid(row=7,column=1,sticky=tk.W)
        self.dataStopEntry.config(width=10)
        
        # number of output files
        self.numberOutputFilesLabel=tk.Label(self,
                                             text = "Number of Output Files")
        self.numberOutputFilesLabel.grid(row=10,column=2,padx=10,sticky=tk.E)        
        self.numberOutputFilesEntry = tk.Entry(self)
        self.numberOutputFilesEntry.grid(row=10,column=3,sticky=tk.W)
        self.numberOutputFilesEntry.config(width=10)
        
        # the run button
        self.runButton=tk.Button(self,text="Run Batch Program",
                                     command=self.runBatchMain)
        self.runButton.grid(row=3,column=3,sticky=tk.W)
        
        # the STOP button
        self.stopButton=tk.Button(self,text="STOP",
                                     command=self.runStop)
        self.stopButton.grid(row=5,column=3,sticky=tk.W)
        self.stopButton.config(bg="red")
        
        # the data server options menue
        self.dataServerLabel=tk.Label(self,text = "Data Server")
        self.dataServerLabel.grid(row=8,column=2,padx=10,sticky=tk.E)
        self.dataServerChooser=tk.StringVar(self)
        self.dataServerChooser.set("MDS")
        self.option=tk.OptionMenu(self,self.dataServerChooser,"MDS","NEIL")
        self.option.grid(row=8,column=3,sticky=tk.W)
        
        # User Name Entry
        self.userNameLabel=tk.Label(self,text = "User Name")
        self.userNameLabel.grid(row=7,column=2,padx=10,sticky=tk.E)        
        self.userNameEntry = tk.Entry(self)
        self.userNameEntry.grid(row=7,column=3,sticky=tk.W)
        self.userNameEntry.config(width=12)
        
    def runStop(self):
        root.destroy()
        root.quit()
        
    def getBatchFile(self):
        self.batchFileName=chooseBatchFile()
        self.batchFileNameEntry.insert(0,self.batchFileName)
        
    def runBatchMain(self):
        if not self.checkPBREntries():
            print("Bad inputs - Need a dialog")
        else:
            bfc=readBatchFile()
            makeReconDirs(bfc)
            
    def checkPBREntries(self):  
        #check entries given by the Python Batch Runner GUI
        if not self.batchFileName:
            # send error dialog
            self.batchFileName="temp"

        print("Server Entries")
        self.server.address=self.serverAddressEntry.get()
        self.server.port=int(self.serverPortEntry.get())
        self.server.timeout=int(self.serverTimeoutEntry.get())
        self.server.print()
        print("Time Interval Entries")
        self.dataTimeInterval.start=float(self.dataStartEntry.get())
        self.dataTimeInterval.stop=float(self.dataStopEntry.get())
        self.dataTimeInterval.print()
        print("Batch File")
        print(self.batchFileName)
        print("Number of Output Files: ",self.numberOutputFiles)
        self.dataHost=self.dataServerChooser.get()
        print("Data Host: ",self.dataHost)
        self.userName=self.userNameEntry.get()
        print("User Name: ",self.userName)
        self.autoShotTime=self.autoShotTimeVar.get()
        print("Auto Shot Time: ",bool(self.autoShotTime))
        return True
        

    def createErrorWindow(self):
        t = tk.Toplevel(self)
        t.wm_title("No Batch File Error Window")
        noBatchFileLabel=tk.Label(text = "No Batch File Given -" 
                                       "Please select a Batch.cthsl file")  
        noBatchFileLabel.grid(row=0,column=0,columnspan=3,
                                 padx=10,pady=20,sticky=tk.W)
        
        button1=tk.Button(text = "OK",command=self.gotOK())
        button1.grid(row=1,column=0,padx=50,pady=20)
        
        button2=tk.Button(text="Cancel",command=self.gotCancel())
        button2.grid(row=1,column=1,padx=10,pady=20)
        button2.configure(text="Cancel")
        
    def gotOK(self):
        print("OK")
        
        
    def gotCancel(self):
        print("Cancel")
            

# main loop stuff      
root=tk.Tk()
root.title("Python Batch Runner")
root.geometry("600x300")
app=BatchRunner(root)
root.mainloop()