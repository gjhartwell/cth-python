# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 08:23:53 2020

@author: hartwgj
"""
# -*- coding: utf-8 -*-
"""

 Testing
     

 This is a test file for the batch runner
 The solutions found here should be migrated to the PythonBatchRunner code
 This code done performs all the reconstructions in the batch file
 This is an upgrade from the program Test_ReadV3Data which only performs one
 reconstruction
 
 Greg Hartwell
 Last modified Aug 5, 2020

"""



from readBatchFile import BatchContents
from PreprocessV3DataFile import PreprocessV3DataFile
#from chooseBatchFile import chooseBatchFile
from ReadV3Data import ReadV3DataFile
from ReadV3Config import ReadV3Config
#from createReconString import createReconString
from ReconstructionString import ReconstructionString
from ReconComm import ReconComm
import os

#file=chooseBatchFile() # Call choose file GUI
file="C:\\Users\\hartwgj\\Desktop\\TestReconFiles\\batchfile.cthsl"



#if not file:
#    error="No batch or CTH shotlist given---You must provide a shotlist"
#    #callErrorDialog(error)
#else:
bfc=BatchContents(file)
debug=False
bfc.readBatchFile(debug) # read the batch file contents
if debug: bfc.print()
debug=False
ppfile=PreprocessV3DataFile(bfc.v3dataFile,debug)
bfc.makeReconDirs() 
#    create directory structure to hold reconstructions
#    only do this once
#    makeReconDirs must be run after chooseBatchFile


"""

v3config data 
    pcurr_type and pmass_type need to be converted 
    from an integer value to a string value 
    need to capture these 
    This will also be an issue when defining the parameterization of
    sxr profiles and density profiles
    
rs.writeV3FITParameters(v3fitClassData)
    need to include writes for signals
        limiter
        sxr
        int
        magnetic

"""
#port is defined in PythonBatchRunner
port=2001
#nfiles should be defined elsewehere but this gives the number of files
#send back from the server as a function of the port number
nfiles={2000:3,2001:5,2002:2}
shotnum=0
shot=bfc.shot_time_array[shotnum]
print("-------------------in Test_BatchRunner---------------------------")
print(shot.shotnumber)
print(shot.time) # this is an array of times
print(shot.dt)
# this gets ALL the data for a single shot
debug=False
vmecClassData,v3fitClassData= \
    ReadV3DataFile(ppfile,shot,debug)
vmecClassData,v3fitClassData= \
    ReadV3Config(bfc,vmecClassData,v3fitClassData,debug)

#idx will be gotten while looping
idx=0
print('idx is',idx,' and time is',shot.time[idx])
print('creating reconstruction string')
rs=ReconstructionString(idx)
rs.writeVMECHeader(shot.shotnumber,shot.time[idx])
rs.writeVMECParameters(vmecClassData)
rs.writeV3FITHeader(shot.shotnumber, shot.time[idx])
rs.writeV3FITParameters(v3fitClassData)
rs.addEOF()

print('sending reconstruction string')

message=rs.getReconString()
comm=ReconComm('recon2.physics.auburn.edu',port,300)
comm.connect()
comm.writeToServer(message)
        
print('---------------------------')
print("Error Check 1")
error=comm.checkError()
print("Error Code %s and error - %s" % error)
print('---------------------------')
print("Error Check 2")
error=comm.checkError()
print(error)
print("Error Code %s and error - %s" % error)
if not bool(error[0]):
    myfiles=nfiles[port]
    while myfiles >=1:
        file,filestuff=comm.readOutputFile()
        dirname=bfc.directoryArray[shotnum]
        if file:
            print(dirname)
            writefilename=os.path.join(dirname,file)
            print(writefilename)
            writefile = open(writefilename, "wb")
            for byte in filestuff:
                writefile.write(byte.to_bytes(1, byteorder='big'))                
            writefile.close()
        myfiles-=1
comm.close()
print('------------------out of Test_BatchRunner-----------------------------')

