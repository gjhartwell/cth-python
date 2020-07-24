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
from chooseBatchFile import chooseBatchFile
from makeReconDirs import makeReconDirs
from ReadV3Data import ReadV3DataFile
from ReadV3Config import ReadV3Config
#from createReconString import createReconString

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
looks like this is doing one shot at a time 
need to include a debug or verbose statement to limit when messages
are being displayed in ReadV3DataFile and ReadV3Config



"""
#for shot in bfc.shot_time_array:
shot=bfc.shot_time_array[0]
print(shot.shotnumber)
print(shot.time)
print(shot.dt)
# this gets all the data for a single shot
vmecClassData,v3fitClassData=ReadV3DataFile(ppfile,shot)
vmecClassData,v3fitClassData=ReadV3Config(bfc,vmecClassData,v3fitClassData)

# need to write the vmecClassData and v3fitClassData 
# to a reconstruction string for each time in the shot

#for timeSlice in shot.time:
#createReconString(shot,timeSlice,vmecClassData,v3fitClassData)
    
    
    