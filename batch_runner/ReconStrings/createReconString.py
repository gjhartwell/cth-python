# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 14:27:17 2020

@author: hartwgj
"""
# createReconString
# 
from ReconstructionString import ReconstructionString
import vmecData

def createReconString(shot,timeSlice,vmecClassData,v3fitClassData):
    
    rs=ReconstructionString(0)
    rs.writeVMECHeader(shot,time)
    rs.writeVMECParameters(vmecClassData):
    
# testing

#
#shotNumber=16121246
#time=1.61
#filetype='vmec'
#rs=ReconstructionString(0)
#rs.writeVMECHeader(shotNumber,time)
#rs.addComment("This is a test")
#rs.addBool("T or F",True)
#rs.addInt8("INT8",8)
#rs.addInt16("INT16",16)
#rs.addInt32("INT32",32)
#rs.addInt64("INT64",64)
#rs.addFloat("FLOAT",time)
#rs.addDouble("Double",time)
#rs.addBoolArray1D("Boolean Array",[True,True,False,True])
#rs.addInt8Array1D("Int8Array",[1,2,3,4])
#rs.addInt16Array1D("Int16Array",[1,2,3,4])
#rs.addInt32Array1D("Int32Array",[1,2,3,4])
#rs.addInt64Array1D("Int64Array",[1,2,3,4])
#rs.addFloatArray1D("Float Array",[1,2,3,4])
#rs.addDoubleArray1D("Double Array",[1.1,2.2,3.3,4.4])
#rs.addDoubleArray1D("single entry double array test",'6.6')
#rs.addStringArray1D('Currents',['HF','TVF','OH'])
#rs.addEOF()
#rs.print()
    
    

