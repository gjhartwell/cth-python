# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 12:37:46 2018

@author: Greg
"""

from ReconstructionString import ReconstructionString
#from vmecData import VMECData
#from v3fitData import V3FITData
#from ReadBatchFile import ReadBatchFile

def createReconString(shot,timeSlice,vmecInputs,v3fitInputs):
    
    #get index of the timeSlice
    idx=shot.time.index(timeSlice)
    shotNumber=shot.shotnumber
    rs=ReconstructionString(idx)
    rs.writeVMECHeader(shotNumber,timeSlice)
    rs.writeVMECParameters(vmecInputs)
    rs.writeV3FITHeader(shotNumber,timeSlice)
    rs.writeV3FITParameters(v3fitInputs)
    rs.addEOF()
    
    return rs

bfc.print()
shot=bfc.shot_time_array[0]
timeSlice=bfc.shot_time_array[0].time[0]

rs=createReconString(shot,timeSlice,vmecClassData,v3fitClassData)
