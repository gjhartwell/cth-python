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
vmecData=VMECData()

def ReadV3Config(bfc,vmecData): #,v3fitData):
    
#    V3FITclassData=V3FITData()
    

    print("==============================================================")
    print("Reading V3FIT CONFIG FILE")
    print("==============================================================")
    
    inVMEC=False
    inV3FIT=False
    
    keys=vmecData.__dict__.keys()
    
    with open(bfc) as fp:
        for line in fp:
            if "BEGIN".lower() in line.lower() \
                and"VMEC".lower() in line.lower(): inVMEC=True
            elif "END".lower() in line.lower() \
                and "VMEC".lower() in line.lower(): inVMEC=False
            
            elif "BEGIN".lower() in line.lower() \
                and "v3fit".lower() in line.lower(): inV3FIT=True
            elif "END".lower() in line.lower() \
                and "v3fit".lower() in line.lower(): inV3FIT=False
            else:
                if inVMEC:
                    print(line)
                    parts=line.split(' ')
                    if parts[0] in keys: 
                        print(len(parts))
                        
                             
            
file="C:/Users/hartwgj/Desktop/pythoncode/Batch_Runner/ReconFolder" + \
    "/phiedge_only_test.v3config"  
ReadV3Config(file,vmecData)