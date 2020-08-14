# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 09:10:24 2018

@author: Greg
"""

# Need a reconstruction CLASS
# basically a string
# and methods to add to the string
# Reconstruction Write Comment
import numpy as np
class ReconstructionString(object):
    
    def __init__(self,reconStringName):
        self.reconStringName=ReconStringName
        self.reconString=''
        
    def addComment(self,comment):
        datatype=str(np.int8(-1))
        self.reconString=self.reconString + \
                        str(len(comment)) + \
                        comment.decode('utf8') + datatype
        
    def addString(self,name,string):
        lengthStr=str(len(string))
        lengthName=str(len(name))
        stringByte=string.decode('utf8')
        nameByte=name.decode('utf8')
        datatype=str(np.int8(14))
        self.reconString=self.reconString + \
                        str(len(name)) + name.decode('utf8') + \
                        datatype + \
                        str(len(string)) + string.decode('utf8')
    
    def addInt32(self,inputName,integer32):
        
    
    