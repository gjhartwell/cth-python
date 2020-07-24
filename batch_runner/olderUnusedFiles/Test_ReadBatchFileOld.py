# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 14:00:06 2017
Last modified June 24, 2020

@author: Greg
"""
# These are testing routines for the batch file reader


from chooseBatchFile import chooseBatchFile
from readBatchFile import * 
from vmecData import VMECData
from v3fitData import V3FITData
from ReadV3Config import ReadV3Config

file=chooseBatchFile()
bfc=BatchContents(file)
bfc.readBatchFile()
bfc.print()
print('number of content files defined: ',bfc.count())
vmecData=VMECData()
v3fitData=V3FITData()            
file="C:\\Users\\Greg\\Desktop\\pythoncode\\Batch_Runner\\ReconFolder\\phiedge_only_test.v3config"  
vmecData,v3fitData=ReadV3Config(file,vmecData,v3fitData)
