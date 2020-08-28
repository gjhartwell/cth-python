# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 11:46:45 2020

@author: hartwgj
"""
from readBatchFile import BatchContents
from readV3Data.PreprocessV3DataFile import PreprocessV3DataFile
#from ReconstructionString import ReconstructionString
from reconStrings.ReconComm import ReconComm
from reconStrings.makeAllReconStrings import makeAllReconStrings
import os
from readV3Data.readV3Data import ReadV3DataFile
from readV3Data.readV3Config import ReadV3Config
from reconStrings.ReconstructionString import ReconstructionString

class Server(object):
    def __init__(self):
        self.address="recon2.physics.auburn.edu"
        self.port=2001
        self.timeout=300

reconserver=Server()
file="C:\\Users\\hartwgj\\Desktop\\TestReconFiles\\batchfile2.cthsl"

print("read batch file")
bfc=BatchContents(file)
debug=False
bfc.readBatchFile(debug) # read the batch file contents
if debug: bfc.print()
debug=False
ppfile=PreprocessV3DataFile(bfc.v3dataFile,debug)
bfc.makeReconDirs() 


allReconStrings=[]
for shotidx,shot in enumerate(bfc.shot_time_array):
    print(shot.shotnumber)
    print(shot.time) # this is an array of times
    print(shot.dt)
    # this gets ALL the data for a single shot
    debug=False
    vmecClassData,v3fitClassData= \
        ReadV3DataFile(ppfile,shot,debug)
    