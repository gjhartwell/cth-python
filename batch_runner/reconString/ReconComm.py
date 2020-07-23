# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 2018
Last modified Feb 1 2018
@author: Greg Hartwell

ReconComm
handles communications between the Recon Client and the Recon Server
these routines are specific to the Reconstruction Server protocols
defines:
    ReconComm - basically a socket connection
    connect - make the connection
    close - close the connection
    writeToServer - write data to server
    checkError - check errors from server
    readOutputFile - reads the output files from the server
"""

import socket
from struct import unpack
  
class ReconComm(object):
    
    def __init__(self,server,port,timeout):
        #initializes and creates the client socket
        self.server = server
        self.port = port
        self.timeout = timeout
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   
    def connect(self):
        # connects to the server socket
        print ('connecting to %s port %s' % (self.server,self.port))
        self.sock.connect((self.server,self.port))
        #self.sock.settimeout(self.timeout)

    def close(self):
        #closes the client-server socket connection
        self.sock.close()
        
    def writeToServer(self,message):
        #print("message is of type ",type(message))
        # writes message string to server   
        print('sending "%s"' % message)
        self.sock.sendall(message)
        
    def checkError(self):      
        #handles the prescribed error checking from the server
       
        # read the Error Code
        buffer=self.readBytes(4)
        errorCode=unpack('>l',buffer)[0]
        
        # read the length of the Error Message
        buffer=self.readBytes(4)
        messageLength = unpack('>l',buffer)[0]
        if messageLength:
            #read the Error Message, length bytes long
            buffer=self.readBytes(messageLength)
            errorMessage=buffer.decode('utf-8')
        else:
            errorMessage='No Error'
        return (errorCode,errorMessage)
    
    def readOutputFile(self):
        # reads output file returned from server
        
        # read length of filename
        buffer=self.readBytes(4)
        fileNameLength=unpack('>l',buffer)[0]
        
        # read the filename
        buffer = self.readBytes(fileNameLength)
        fileName=buffer.decode('utf-8')
        
        #read the length of the file
        buffer=self.readBytes(8)
        fileLength=unpack('>l',buffer)[0]
        
        # read the file contents
        buffer=self.readBytes(fileLength)
        fileContents=buffer.decode('utf-8')
        return(fileName,fileContents)
        
    def readBytes(self,bytesToRead):
        buffer = bytearray(bytesToRead)
        view = memoryview(buffer)
        while bytesToRead:
            nbytes = self.sock.recv_into(view, bytesToRead)
            view = view[nbytes:] # slicing views is cheap
            bytesToRead -= nbytes
        return buffer       
        
from ReconstructionString import ReconstructionString       
#testing
message=rs.getReconString()
comm=ReconComm('131.204.212.162',2003,10)
comm.connect()
comm.writeToServer(message)
#print('---------------------------')
#print("Error Check 1")
#error=comm.checkError()
#print("Error Code %s and error - %s" % error)
#print('---------------------------')
#print("Error Check 2")
#error=comm.checkError()
#print("Error Code %s and error - %s" % error)
comm.close()

    