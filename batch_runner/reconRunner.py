# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 10:29:23 2020

@author: hartwgj
"""
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

from readBatchFile import BatchContents
from readV3Data.PreprocessV3DataFile import PreprocessV3DataFile
#from ReconstructionString import ReconstructionString
from reconStrings.ReconComm import ReconComm
from reconStrings.makeAllReconStrings import makeAllReconStrings
import os
import multiprocessing as mp

########################################################################
class Server(object):
    def __init__(self):
        self.address="recon2.physics.auburn.edu"
        self.port=2001
        self.timeout=600

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
def doReconRunner(file,server):


    print("in do recon_runner")
    bfc=BatchContents(file)
    debug=False
    bfc.readBatchFile(debug) # read the batch file contents
    if debug: bfc.print()
    debug=False
    ppfile=PreprocessV3DataFile(bfc.v3dataFile,debug)
    bfc.makeReconDirs() 


    allReconStrings=makeAllReconStrings(bfc,ppfile)
    dirnames=bfc.directoryArray
    return dirnames,allReconStrings

#########################################################################
 
def reconRunnerMultiProcessor(file,reconserver):   
    if __name__ == '__main__':
        print("in reconRunnerMultiProcessor")

        dirnames,allReconStrings=doReconRunner(file,reconserver)
        
        jobs=[]
        for idx,rs in enumerate(allReconStrings):
            dirname=dirnames[idx]
            p = mp.Process(target=sendToServer,args=(reconserver,rs,dirname))
            jobs.append(p)
        for j in jobs:
            j.start()
        for j in jobs:
            j.join()
            
########################################################################
            
        
reconserver=Server()
file="C:\\Users\\hartwgj\\Desktop\\TestReconFiles\\batchfile.cthsl"
reconRunnerMultiProcessor(file,reconserver) 
# dirnames,allReconStrings=doReconRunner(file,reconserver)
# rs=allReconStrings[0]
# dirname=dirnames[0]
# sendToServer(reconserver,rs,dirname)