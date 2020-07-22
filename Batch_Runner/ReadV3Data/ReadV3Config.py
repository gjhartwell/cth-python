# --------------------------------------
# ReadV3Config - Reads in the V3Config file
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
# Also defines:
#   
# To do:
# 
#	
# Greg Hartwell
# 2017-11-27
#----------------------------------------------------------------------------


from vmecData import VMECData
from v3fitData import V3FITData


def ReadV3Config(bfc,vmecData,v3fitData):
    
#    V3FITclassData=V3FITData()
    

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
            print(line)
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
                print(line)
                parts=line.split(' ')
                print('parts = ',parts)
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
                        
                        elif inSignalWeight:
                            if name == 'sdo_w_spec_imin':
                                imin=parts[1]
                            elif name == 'sdo_w_spec_imax':
                                imax=parts[1]
                            elif name == 'sdo_w_spec_weight':
                                weights=getattr(v3fitData,'sdo_w_spec_weight')
                                for i in range(imax-imin):
                                    weights[i+imin]=parts[1]
                                setattr(v3fitData,'sdo_w_spec_weight',weights)
                        
                        elif inSignalSigma:
                            if name == 'sdo_s_spec_imin':
                                imin=parts[1]
                            elif name == 'sdo_s_spec_imax':
                                imax=parts[1]
                            elif name == 'sdo_s_spec_floor':
                                floors=getattr(v3fitData,'sdo_s_spec_floor')
                                for i in range(imax-imin):
                                    floors[i+imin]=parts[1]
                                setattr(v3fitData,'sdo_s_spec_floor',floors)
                            elif name == 'sdo_s_spec_fraction':
                                frac=getattr(v3fitData,'sdo_s_spec_fraction')
                                for i in range(imax-imin):
                                    frac[i+imin]=parts[1]
                                setattr(v3fitData,'sdo_s_spec_fraction',frac)
                            
                        else:
                            oldvalue=getattr(v3fitData,name)
                            setattr(v3fitData,name,value)
    return vmecData,v3fitData
                        
 # testing                
# vmecData=VMECData()
# v3fitData=V3FITData()            
# file="C:\\Users\\Greg\\Desktop\\pythoncode\\Batch_Runner\\ReconFolder\\phiedge_only_test.v3config"  
# vmecData,v3fitData=ReadV3Config(file,vmecData,v3fitData)