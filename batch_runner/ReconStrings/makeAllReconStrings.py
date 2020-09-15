# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 16:27:51 2020

@author: hartwgj
"""

from readV3Data.readV3Data import ReadV3DataFile
from readV3Data.readV3Config import ReadV3Config
from reconStrings.ReconstructionString import ReconstructionString

def makeAllReconStrings(bfc,ppfile):
    
    allReconStrings=[]
    for shotidx,shot in enumerate(bfc.shot_time_array):
        print("in makeAllReconStrings")
        print(shot.shotnumber)
        print(shot.time) # this is an array of times
        print(shot.dt)
        # this gets ALL the data for a single shot
        debug=False
        vmecClassData,v3fitClassData= \
            ReadV3DataFile(ppfile,shot,debug)
        vmecClassData,v3fitClassData= \
            ReadV3Config(bfc,vmecClassData,v3fitClassData,debug)
    
        for idx,time in enumerate(shot.time):
            if debug:
                print('idx is',idx,' and time is',shot.time[idx])
                print('creating reconstruction string')
            rs=ReconstructionString(idx)
            rs.writeVMECHeader(shot.shotnumber,shot.time[idx])
            rs.writeVMECParameters(vmecClassData)
            rs.writeV3FITHeader(shot.shotnumber, shot.time[idx])
            rs.writeV3FITParameters(v3fitClassData)
            rs.addEOF()
            allReconStrings.append(rs)
    return allReconStrings