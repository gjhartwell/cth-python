# -*- coding: utf-8 -*-
"""

 Testing
     

 These are testing routines for the batch file reader
 The solutions found here should be migrated to the PythonBatchRunner code
 
 Greg Hartwell
 Last modified June 25, 2020

"""



from readBatchFile import BatchContents
from PreprocessV3DataFile import PreprocessV3DataFile
#from chooseBatchFile import chooseBatchFile
from makeReconDirs import makeReconDirs
from ReadV3Data import ReadV3DataFile
from ReadV3Config import ReadV3Config
#from createReconString import createReconString
from ReconstructionString import ReconstructionString

#from callErrorDialog import callErrorDialog

#file=chooseBatchFile() # Call choose file GUI
file="C:\\Users\\hartwgj\\Desktop\\TestReconFiles\\batchfile.cthsl"

#if not file:
#    error="No batch or CTH shotlist given---You must provide a shotlist"
#    #callErrorDialog(error)
#else:
bfc=BatchContents(file)
bfc.readBatchFile() # read the batch file contents
bfc.print()

ppfile=PreprocessV3DataFile(bfc.v3dataFile)
makeReconDirs(bfc) 
#    create directory structure to hold reconstructions
#    only do this once
#    makeReconDirs must be run after chooseBatchFile


"""

need to include a debug or verbose statement to limit when messages
are being displayed in ReadV3DataFile and ReadV3Config



"""

#for shot in bfc.shot_time_array:
shot=bfc.shot_time_array[0]
print(shot.shotnumber)
print(shot.time) # this is an array of times
print(shot.dt)
# this gets all the data for a single shot
vmecClassData,v3fitClassData=ReadV3DataFile(ppfile,shot)
vmecClassData,v3fitClassData=ReadV3Config(bfc,vmecClassData,v3fitClassData)
#for time in shot.time:
time=shot.time[0]
print(time)
# need to write the vmecClassData and v3fitClassData 
# to a reconstruction string for each time in the shot

#for timeSlice in shot.time:
#        createReconString(time,vmecClassData,v3fitClassData)

    

# testing

#
#shotNumber=16121246
#time=1.61

rs=ReconstructionString(0)
rs.writeVMECHeader(shot.shotnumber,time)
rs.writeVMECParameters(vmecClassData)
rs.writeV3FITHeader(shot.shotnumber, time)
rs.writeV3FITParameters(v3fitClassData)

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

    