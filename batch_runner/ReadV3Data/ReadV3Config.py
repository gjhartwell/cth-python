# --------------------------------------
# ReadV3Config - Reads in the V3Config file
#                Run after ReadV3Data
# 
# BatchRunner Python project
# 
#
# Parameters:
#	 
# Returns:
#
# Example:
# 
# Defines:
#     ReadV3Config(bfc,vmecData,v3fitData,debug)
#   
# 
# 
#	
# Greg Hartwell
# 2017-11-27
#
# 2020-7-28 - Added debug input to print messages only when in debug=True 
#           mode
#----------------------------------------------------------------------------


from readV3Data.vmecData import VMECData
from readV3Data.v3fitData import V3FITData
import numpy as np

#-------------------------------------------------------

def makeSigmaArray(v3fitData,debug):
    
    # put signals in one location
    debug=True

    data=np.array(v3fitData.sdo_data_a)
    v3fitData.sdo_sigma_a=data
    if debug:
        print('in makeSigmaArray')
        print(v3fitData.sdo_s_spec_imin)
        print(v3fitData.sdo_s_spec_imax)
        print(v3fitData.sdo_s_spec_floor)
        print(v3fitData.sdo_s_spec_fraction)
        print('sdo_data')
        print(v3fitData.sdo_data_a)
        print('data',data.shape)
        print(data)
   
    
    for idx1,idx2,floor,frac in zip(v3fitData.sdo_s_spec_imin,
                                    v3fitData.sdo_s_spec_imax,
                                    v3fitData.sdo_s_spec_floor,
                                    v3fitData.sdo_s_spec_fraction):
        if debug: print(idx1,idx2,floor,frac)
        for idx in range(int(idx1),int(idx2)):
            for time in range(data.shape[1]):
                if debug:print('point a',idx,time,data[idx-1][time])
                v3fitData.sdo_sigma_a[idx-1][time]= \
                    max(float(floor),float(frac)*data[idx-1][time])
    if debug:
        print('sigma')
        v3fitData.sdo_sigma_a=v3fitData.sdo_sigma_a.tolist()
        print(v3fitData.sdo_sigma_a)
   
    
    return v3fitData

def ReadV3Config(bfc,vmecData,v3fitData,debug):
    
#    V3FITclassData=V3FITData()
    

    if debug:
        print("==============================================================")
        print("Reading V3FIT CONFIG FILE")
        print("==============================================================")
    
    inVMEC=False
    inV3FIT=False
    inParameter=False
    inBarLimiter=False
    inCircularLimiter=False
    inSignalWeight=False
    inSignalSigma=False
    inCombination=False
    
    file=bfc.v3configFile.strip('\n')
    with open(file) as fp:
        for line in fp:
            if debug: print(line)
            if "BEGIN".lower() in line.lower():
                if "VMEC".lower() in line.lower(): 
                    inVMEC=True
                elif "v3fit".lower() in line.lower(): 
                    inV3FIT=True
                elif "parameter".lower() in line.lower():
                    inParameter=True
                    oldvalue=getattr(v3fitData,'n_rp')
                    setattr(v3fitData,'n_rp',oldvalue+1)
                elif "Bar".lower() in line.lower(): 
                    inBarLimiter=True
                    oldvalue=getattr(v3fitData,'n_signals')
                    setattr(v3fitData,'n_signals',oldvalue+1)
                    oldvalue=getattr(v3fitData,'nBarLimiters')
                    setattr(v3fitData,'nBarLimiters',oldvalue+1)
                    oldvalue=getattr(v3fitData,'signalNames')
                    setattr(v3fitData,'signalNames',oldvalue+["Bar Limiter"])
                elif "Circular".lower() in line.lower(): 
                    inCircularLimiter=True
                    oldvalue=getattr(v3fitData,'n_signals')
                    setattr(v3fitData,'n_signals',oldvalue+1)
                    oldvalue=getattr(v3fitData,'nCircularLimiters')
                    setattr(v3fitData,'nCircularLimiters',oldvalue+1)
                    oldvalue=getattr(v3fitData,'signalNames')
                    setattr(v3fitData,'signalNames',oldvalue+["Circular Limiter"])
                elif "Signal Weight".lower() in line.lower(): 
                    inSignalWeight=True
                elif "Signal Sigma".lower() in line.lower(): 
                    inSignalSigma=True
                elif "Combination".lower() in line.lower(): 
                    inCombination=True
            elif "END".lower() in line.lower():
                if "VMEC".lower() in line.lower(): 
                    inVMEC=False
                elif "v3fit".lower() in line.lower(): 
                    inV3FIT=False
                elif "parameter".lower() in line.lower(): 
                    inParameter=False
                elif "Bar".lower() in line.lower(): 
                    inBarLimiter=False
                elif "Circular".lower() in line.lower(): 
                    inCircularLimiter=False
                elif "Signal Weight".lower() in line.lower(): 
                    inSignalWeight=False
                elif "Signal Sigma".lower() in line.lower():
                    inSignalSigma=False
                elif "Combination".lower() in line.lower(): 
                    inCombination=False
            else:
                line=line.strip('\n')
                # remove parenthesis and interior
                d1=line.find('(')
                d2=line.find(')')
                if d1 != -1 and d2 != -1:
                    line=line[:d1]+line[d2+1:]
                if debug: print(line)
                parts=line.split(' ')
                if debug: print('parts = ',parts)
                if len(parts)!= 1:
                    if len(parts) > 2:
                        value=parts[1:]
                    else:
                       value=parts[1]
                    name=parts[0].lower()
                
                    if inVMEC:
                        setattr(vmecData,name,value)
                             
                    if inV3FIT:
                        if inParameter or inBarLimiter or \
                            inCircularLimiter or inCombination:
                            oldvalue=getattr(v3fitData,name)
                            setattr(v3fitData,name,oldvalue+[value])
                        
                        elif inSignalWeight or inSignalSigma:
                            value=getattr(v3fitData,name)
                            value.append(parts[1])
                            setattr(v3fitData,name,value)
                           
                            
                        else:
                            oldvalue=getattr(v3fitData,name)
                            setattr(v3fitData,name,value)
    # make sigma array
    v3fitData=makeSigmaArray(v3fitData,debug)
    return vmecData,v3fitData
                     
        

                   
 # testing                
# vmecData=VMECData()
# v3fitData=V3FITData()            
# file="C:\\Users\\Greg\\Desktop\\pythoncode\\Batch_Runner\\ReconFolder\\phiedge_only_test.v3config"  
# vmecData,v3fitData=ReadV3Config(file,vmecData,v3fitData)