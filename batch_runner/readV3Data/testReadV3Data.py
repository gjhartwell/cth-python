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

########################################################################
def sendToServer(server,rs,dirname):
    
    # define the number of files based on the port
    # port 2000 - three files returned
    # port 2001 - five files returned
    # port 2002 - two files returned
    # default is 2001
    nfiles={2000:3,2001:5,2002:2}
    print('parent process:', os.getppid())
    print('process id:', os.getpid())
    
    message=rs.getReconString()
    comm=ReconComm(server.address,server.port,server.timeout)
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
        myfiles=nfiles[server.port]
        while myfiles >=1:
            file,filestuff=comm.readOutputFile()
            if file:
                writefilename=os.path.join(dirname,file)
                print(writefilename)
                writefile = open(writefilename, "wb")
                for byte in filestuff:
                    writefile.write(byte.to_bytes(1, byteorder='big'))                
                writefile.close()
            myfiles-=1
    comm.close()
    print('------------------out of Test_BatchRunner---------------------')

########################################################################

reconserver=Server()
file="C:\\Users\\hartwgj\\Desktop\\TestReconFiles\\batchfile2.cthsl"
file=r'C:\Users\hartwgj\Desktop\TestReconFilesInt\batchfile_phi_int.cthsl'
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
    debug=True
    vmecClassData,v3fitClassData= \
        ReadV3DataFile(ppfile,shot,debug)
    vmecClassData,v3fitClassData= \
        ReadV3Config(bfc,vmecClassData,v3fitClassData,debug)
        
    for idx,time in enumerate(shot.time):

        print('idx is',idx,' and time is',shot.time[idx])
        print('creating reconstruction string')
        rs=ReconstructionString(idx)
        rs.writeVMECHeader(shot.shotnumber,shot.time[idx])
        rs.writeVMECParameters(vmecClassData)
        rs.writeV3FITHeader(shot.shotnumber, shot.time[idx])
        rs.writeV3FITParameters(v3fitClassData)
        rs.addEOF()
        allReconStrings.append(rs)
dirnames=bfc.directoryArray
for idx,rs in enumerate(allReconStrings):
            dirname=dirnames[idx]
            sendToServer(reconserver,rs,dirname)
            

