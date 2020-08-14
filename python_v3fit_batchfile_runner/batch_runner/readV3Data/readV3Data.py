# --------------------------------------
# ReadV3Data - Reads in the V3Data file
# 
# BatchRunner Python project
# 
#
# Defines:
#   class ReconCTHData - subset of CTHData class
#   ReadV3DataFile(preProcessedFile,shot,debug)
#   ParseV3DataLine(line,debug)  
#   InterpretV3DataLine(shot,values,shotData,dataNames,debug)
# 
#	
# Greg Hartwell
# 2017-11-27
# 2020-7-28 - Added debug input to print messages only when in debug=True 
#           mode
#----------------------------------------------------------------------------
#
#import ChannelInfo
#from ChannelInfo import *
    # defines channelToBoard
    # defines class ChannelInfo 
from cthmds.CTHdata import CTHData
import numpy as np
from readV3Data.vmecData import VMECData
from readV3Data.v3fitData import V3FITData


#this class is similar to the CTHData class, but with less information
#this is used internally in the Batch Runner programs
class ReconCTHData(object):
    def __init__(self,name):
        self.name=name
        
    def addData(self,data):
        self.data=data
        
    def addTaxis(self,taxis):
        self.taxis=taxis
        
    def getName(self):
        return self.name
    
    def getData(self):
        return self.data
    
    def multiply(self,scale_factor):
        self.data=self.data*scale_factor
        
    def add(self,offset):
        self.data=self.data+offset

def ReadV3DataFile(preProcessedFile,shot,debug):
    # This should get the data for a single shot in the batch file

    nline=0
    allData=[]
    dataNames=[]
    VMECclassData=VMECData()
    V3FITclassData=V3FITData()
    if debug:
        print("==============================================================")
        print("In ReadV3Data.ReadV3DataFile")
        print("Data for shot ",shot.shotnumber)
        print("==============================================================")
    #shotData=[shot.shotnumber]+[shot.time]
    shotData=[]
    with open(preProcessedFile) as fp:
        for line in fp:
            if debug:
                print("------------------------------------------------------")
            nline += 1
            chars=list(line)
            if chars[0]  != '#': # not a comment
                if not line.isspace():
                    if debug: print(nline,line)
                    parsedLine=ParseV3DataLine(line,debug)
                    if debug: print("Parsed Line -- ",parsedLine)
                    if parsedLine[0] == "var":
                        (shotData,dataNames)=InterpretV3DataLine(shot,
                                                     parsedLine,
                                                     shotData,
                                                     dataNames,
                                                     debug)
                    elif parsedLine[0] == "class" \
                            and parsedLine[1]=='vmec_data':
                        VMECclassData.VMECmoveToClass(shot,
                                              parsedLine,
                                              shotData,
                                              dataNames,
                                              debug)
                    elif parsedLine[0] == "class" \
                            and parsedLine[1]=='v3fit_data':
                        V3FITclassData.V3FITmoveToClass(shot,
                                                        parsedLine,
                                                        shotData,
                                                        dataNames,
                                                        debug)
                    else:
                        print (parsedLine[0]," not handled yet")
    allData=allData+shotData
    
    return (VMECclassData,V3FITclassData)
#-----------------------------------------------------------------------------
#   End of ReadV3DataFile
#----------------------------------------------------------------------------- 
    
def ParseV3DataLine(line,debug):
    # takes a line of integers, float, and characters
    # and parses it
    if debug: print("in ParseV3DataLine--- ",line)
    values=[]
    values2=[]
    # remove return and new line characters
    line=line.strip(' \r\n')
    # remove white space
    words=line.split(" ")
    for w in words:
        w=w.strip()
        if w != "":
            values.append(w)
    #print("values 1 -- ",values)
    # pull out commas from strings 
    for idx, v in enumerate(values):
        if "," in v:
            w=v.split(",")
            values2.append(w[0])
            if w[1] != "":
                values2.append(w[1])
            #values2.append(",") removed this line to get rid of commas
        else:
            values2.append(v)
    #print("values 2 -- ",values2)
    # remove parentheses
    table=str.maketrans(dict.fromkeys('()'))
    for idx,v in enumerate(values2):
        values2[idx]=v.translate(table)
    # remove brackets
    table=str.maketrans(dict.fromkeys('{}'))
    for idx,v in enumerate(values2):
        values2[idx]=v.translate(table)
    while 'NUMBER' in values2: values2.remove('NUMBER')
    while '=' in values2: values2.remove('=') 
    while '' in values2: values2.remove('')
    return values2
#-----------------------------------------------------------------------------
#   End of ParseV3DataLine
#-----------------------------------------------------------------------------
    
def InterpretV3DataLine(shot,values,shotData,dataNames,debug):
    if debug: print("InterpretV3Data --- initial values: ",values)
    # create the data instance with name in values[1]
    dataName=values[1]
    for i in range(2): del values[0]
    values.reverse()
    stack=[]
    if debug: print("In InterpretV3Data ---reversed values: ",values)
    for v in values:
        tempdata=ReconCTHData("temp")
        if debug: 
            print("In IntV3Data while --- stack ",stack)
            print("value is ",v)
        if v.isdigit(): 
            if debug: print("found digit",v)
            stack.insert(0,int(v))
        
        elif "." in v:
            if debug: print("found float",v)
            stack.insert(0,float(v))
        
        elif "," in v:
            if debug: print("found comma --- probably an error")
            del values[0]
            break
        
        elif v == "LOAD_CHANNEL_NUMBER":
            if debug: print("loading channel ",stack[0])
            channelData=CTHData("temp")
            channelData.get_data(shotnum=shot.shotnumber,channel=stack.pop(0))
            tempdata.addData(channelData.data)
            tempdata.addTaxis(channelData.taxis)
            stack.insert(0,tempdata)
        
        elif v=="LOAD_CHANNEL":
            channelData=CTHData("temp")
            channelData.get_data(shotnum=shot.shotnumber,node=stack.pop(0))
            tempdata.addData(channelData.data)
            tempdata.addTaxis(channelData.taxis)
            stack.insert(0,tempdata)
            
        elif v=="ZERO_BEGINNING":
            if debug: print("zeroing data")
            numStartData=1000 # number of points to use to zero data
            tempdata=stack.pop(0)
            aveStartData=np.sum(tempdata.data[0:numStartData])/numStartData
            tempdata.data=np.subtract(tempdata.data,aveStartData)
            stack.insert(0,tempdata)
            
        elif v == "ADD":
            v1=stack.pop(0) 
            v2=stack.pop(0) 
            if debug: print(type(v1),type(v2))
            if (type(v1) is int or type(v1) is float) \
                                    and type(v2) is ReconCTHData:
                if debug: print("adding an offset")
                tempdata.addData(v2.data+v1)
                tempdata.addTaxis(v2.taxis)
                stack.insert(0,tempdata)
            elif (type(v2) is int or type(v2) is float) \
                                    and type(v1) is ReconCTHData:
                if debug: print("adding an offset")
                tempdata.addData(v1.data+v2)
                tempdata.addTaxis(v1.taxis)
                stack.insert(0,tempdata)
            else:
                if debug: print("adding two arrays")
                if len(v1.taxis) != len(v2.taxis):
                    v1.data=np.interp(v2.taxis,v1.taxis,v1.data)
                if debug: print(len(v1.data))
                tempdata.addData(v1.data+v2.data)
                tempdata.addTaxis(v2.taxis)
                stack.insert(0,tempdata)

        elif v == "SUBTRACT":
            v1=stack.pop(0)
            v2=stack.pop(0)
            if type(v2) is ReconCTHData and type(v1) is ReconCTHData:
                tempdata.addData(v1.data-v2.data)
                tempdata.addTaxis(v1.taxis)
                stack.insert(0,tempdata)
            else:
                print("Unhandled SUBTRACT in InterpretV3DataLine")
            
        elif v == "MULTIPLY":
            v1=stack.pop(0) # v1 is factor
            v2=stack.pop(0) # v2 is array
            if type(v2) is ReconCTHData and type(v1) is float:
                tempdata.addData(v2.data*v1)
                tempdata.addTaxis(v2.taxis)
                stack.insert(0,tempdata)
            elif type(v1) is ReconCTHData and type(v2) is float:
                tempdata.addData(v1.data*v2)
                tempdata.addTaxis(v1.taxis)
                stack.insert(0,tempdata)
            elif type(v1) is ReconCTHData and type(v2) is ReconCTHData:
                if len(v1.taxis) != len(v2.taxis):
                    if len(v1.taxis) < len(v2.taxis):
                        v1.data=np.interp(v2.taxis,v1.taxis,v1.data)
                    else:
                        v2.data=np.interp(v1.taxis,v2.taxis,v2.data)
                tempdata.addData(v1.data*v2.data)
                tempdata.addTaxis(v1.taxis)
                stack.insert(0,tempdata)
            else:
                print("unhandled MULTIPLY in InterpretV3Data in ReadV3Data")
        
        elif v == "DOT_PRODUCT":
            # check that arrays are same size
            if debug: print("test stack length is two", len(stack))
            stack1=stack.pop(0)
            stack2=stack.pop(0)
            lenStack1=len(stack1)
            lenStack2=len(stack2)
            if debug: 
                print("test stack length is zero", len(stack))
                print("stack item 0 length :",lenStack1)
                print("stack item 1 length :",lenStack2)
            if lenStack1==lenStack2:
                if debug: print("taking DOT product")
                for v1,v2 in zip(stack1,stack2):
                    if type(v2) is ReconCTHData and type(v1) is float:
                        tempdata.addData(v2.data*v1)
                        tempdata.addTaxis(v2.taxis)
                        stack.insert(0,tempdata)
                        if debug: print("test stack length ", len(stack))
                    elif type(v1) is ReconCTHData and type(v2) is float:
                        tempdata.addData(v1.data*v2)
                        tempdata.addTaxis(v1.taxis)
                        stack.insert(0,tempdata)
                        if debug: print("test stack length ", len(stack))
                    else:
                        print("unhandled DOT PRODUCT")
                tempData=stack.pop(0) 
                if debug: print("test stack length ", len(stack))
                for i in range(lenStack1-1):
                    tempData.data+=stack.pop(0).data
                    if debug: print("test stack length ", len(stack))
                if debug: print("test stack length is zero", len(stack))    
                stack.insert(0,tempData)    
                if debug: print("in InterpretV3Data in ReadV3Data") 
            else:
                print("error in DOT product, arrays of different lengths")
        
        elif v=="AVERAGE":
            if debug: print("Doing an average")
            elements=len(stack)
            tempdata=stack.pop(0)
            while stack:
                tempData.data+=stack.pop(0).data
            tempData.data/=elements
            stack.insert(0,tempData)
            
        elif v == "ARRAY":
            #for item in stack of same type
            arrayType=type(stack[0])
            if debug: print("Array Type = ",arrayType)
            subStack=[]
            subStack.insert(0,stack.pop(0))
            while stack and type(stack[0]) is arrayType:
                if debug: print("Element Type = ",type(stack[0]))
                subStack.insert(0,stack.pop(0))
            subStack.reverse()
            stack.insert(0,subStack)
            
        
        elif any(c.isalpha() for c in v): # then this is a variable
            #search shotData for data name
            if debug: print ("searching for data name:",v)
            if v in dataNames:
                idx=dataNames.index(v)
                if debug: print("found data %s at %d of %d" % (v,idx,len(shotData)))
                stack.insert(0,shotData[idx])
            elif 'processed' in v:
                if debug: print("using processed data")
                stack.insert(0,v)
            else:
                print("Oops, no data found for ",v)
            
            
        else:
            if debug: print("deleting next value")
            del values[0]     
    
    if debug: print("stack type --",type(stack[0]))
    if isinstance(stack[0],list):
        if debug: print("Adding Array")
        shotData.append(stack[0])
        
    elif isinstance(stack[0], ReconCTHData):
        if debug: print("Adding ReconCTHData")
        data=ReconCTHData(dataName)
        data.addData(stack[0].data)
        data.addTaxis(stack[0].taxis)
        if debug: print(data.getName())
        shotData.append(data)
    
    dataNames+=[dataName]
    return (shotData,dataNames)
#-----------------------------------------------------------------------------
#   End of InterpretV3DataLine
#-----------------------------------------------------------------------------


        
    
    
            
                    



