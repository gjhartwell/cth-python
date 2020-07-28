# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 09:10:24 2018

@author: Greg Hartwell
last edited Jan 30, 2018


# Defines the Class ReconstuctionSting and methods

addComment
addBool
addInt8, addInt16, addInt32, addInt64
addFloat, addDouble
addBoolArray1D
addInt8Array1D, addInt16Array1D, addInt32Array1D, addInt64Array1D
addFloatArray1D, addDoubleArray1D
addString
addStringArray1D

print - prints the string

"""

from struct import pack
from v3fitData import step_types,rp_types,rp_range_types,signal_types,\
            derived_parameters

class ReconstructionString(object):
    
    def __init__(self,index):
        # the Reconstruction code assumes that filetype header
        # will be vmec or v3fit
        # errors will occur if this is not the case
        
        # this just creates a blank byte string
        self.reconString=b''
        self.idx=index
# ----------------------------------------------------------------------------
#                       Basic Writing Commands
# ----------------------------------------------------------------------------
        
    def print(self):
        print(self.reconString)
        
    def getReconString(self):
        return self.reconString
        
    def addComment(self,comment):
        datatype=pack('>b',-1)
        self.reconString=self.reconString + \
                        pack('>l',len(comment)) + bytes(comment,'utf-8') + \
                        datatype
        
    def addBool(self,name,boolean):
        datatype=pack('>b',0)
        self.reconString=self.reconString + \
                        pack('>l',len(name)) + bytes(name,'utf-8') + \
                        datatype + pack('>?',boolean)


    def addInt8(self,name,integer8):
        integer8=int(integer8)
        datatype=pack('>b',1)
        self.reconString=self.reconString + \
                        pack('>l',len(name)) + bytes(name,'utf-8') + \
                        datatype + pack('>b',integer8)

    def addInt16(self,name,integer16):
        integer16=int(integer16)
        datatype=pack('>b',2)
        self.reconString=self.reconString + \
                        pack('>l',len(name)) + bytes(name,'utf-8') + \
                        datatype + pack('>h',integer16)                       

    def addInt32(self,name,integer32):
        integer32=int(integer32)
        datatype=pack('>b',3)
        self.reconString=self.reconString + \
                        pack('>l',len(name)) + bytes(name,'utf-8') + \
                        datatype + pack('>l',integer32)

    def addInt64(self,name,integer64):
        integer64=int(integer64)
        datatype=pack('>b',4)
        self.reconString=self.reconString + \
                        pack('>l',len(name)) + bytes(name,'utf-8') + \
                        datatype + pack('>q',integer64)
                        
    def addFloat(self,name,floatIn):
        floatIn=float(floatIn)
        datatype=pack('>b',5)
        self.reconString=self.reconString + \
                        pack('>l',len(name)) + bytes(name,'utf-8') + \
                        datatype + pack('>f',floatIn)

    def addDouble(self,name,doubleIn):
        doubleIn=float(doubleIn)
        datatype=pack('>b',6)
        self.reconString=self.reconString + \
                        pack('>l',len(name)) + bytes(name,'utf-8') + \
                        datatype + pack('>d',doubleIn)
                        
    def addBoolArray1D(self,name,boolArrIn):
        datatype=pack('>b',7)
        self.reconString=self.reconString + \
                        pack('>l',len(name)) + bytes(name,'utf-8') + \
                        datatype + pack('>l',len(boolArrIn))
        for boolean in boolArrIn:
            self.reconString += pack('>?',boolean)
            
    def addInt8Array1D(self,name,int8ArrIn):
        datatype=pack('>b',8)
        self.reconString=self.reconString + \
                        pack('>l',len(name)) + bytes(name,'utf-8') + \
                        datatype + pack('>l',len(int8ArrIn))
        for int8 in int8ArrIn:
            int8=int(int8)
            self.reconString += pack('>b',int8)
            
    def addInt16Array1D(self,name,int16ArrIn):
        datatype=pack('>b',9)
        self.reconString=self.reconString + \
                        pack('>l',len(name)) + bytes(name,'utf-8') + \
                        datatype + pack('>l',len(int16ArrIn))
        for int16 in int16ArrIn:
            int16=int(int16)
            self.reconString += pack('>h',int16)
            
    def addInt32Array1D(self,name,int32ArrIn):
        datatype=pack('>b',10)
        self.reconString=self.reconString + \
                        pack('>l',len(name)) + bytes(name,'utf-8') + \
                        datatype + pack('>l',len(int32ArrIn))
        for int32 in int32ArrIn:
            int32=int(int32)
            self.reconString += pack('>l',int32)
            
    def addInt64Array1D(self,name,int64ArrIn):
        datatype=pack('>b',11)
        self.reconString=self.reconString + \
                        pack('>l',len(name)) + bytes(name,'utf-8') + \
                        datatype + pack('>l',len(int64ArrIn))
        for int64 in int64ArrIn:
            int64=int(int64)
            self.reconString += pack('>q',int64)

    def addFloatArray1D(self,name,floatArrIn):
        datatype=pack('>b',12)
        
        if type(floatArrIn) is str:
            floatArrIn=[float(floatArrIn)]
        self.reconString=self.reconString + \
                       pack('>l',len(name)) + bytes(name,'utf-8') + \
                        datatype + pack('>l',len(floatArrIn))
        for flt in floatArrIn:
            flt=float(flt)
            self.reconString += pack('>f',flt)
            
    def addDoubleArray1D(self,name,doubleArrIn):
        datatype=pack('>b',13)

        if type(doubleArrIn) is str:
            doubleArrIn=[float(doubleArrIn)]
        
        self.reconString=self.reconString + \
                        pack('>l',len(name)) + bytes(name,'utf-8') + \
                        datatype + pack('>l',len(doubleArrIn))
        for double in doubleArrIn:
                double=float(double)
                self.reconString += pack('>d',double)


    def addString(self,name,string):
        datatype=pack('b',14)
        self.reconString=self.reconString + \
                        pack('>l',len(name)) + bytes(name,'utf-8') + \
                        datatype + \
                        pack('>l',len(string)) + bytes(string,'utf-8')
                        
#                        pack('l',len(name)) + stringToBytes(name) + \
#                        datatype + \
#                        pack('l',len(string)) + stringToBytes(string)
    
    def addStringArray1D(self,name,stringArrIn):
        datatype=pack('>b',15)
        self.reconString=self.reconString + \
                    pack('>l',len(name)) + bytes(name,'utf-8') + \
                    datatype + pack('>l',len(stringArrIn))
        for string in stringArrIn:
            self.reconString += pack('>l',len(string)) + bytes(string,'utf-8')
                        
    def addEOF(self):
        EOF="EOF"
        self.reconString=self.reconString + \
                        pack('>l',len(EOF)) +bytes(EOF,'utf-8')

# ----------------------------------------------------------------------------
#                        V3FIT Wrting Commands
# ----------------------------------------------------------------------------
 
    def writeV3FITHeader(self,shotNumber,shotTime):
        print("writing V3FIT Header")
        filetype='v3fit'
        self.addString("File Type",filetype)
        self.addInt32("Shot Number",shotNumber)
        self.addDouble("Time Slice",shotTime)  
        
    def writeV3FITControls(self,v3fitInputs):
        print("Writing V3FIT Controls")
        self.addComment("Reconstruction Controls")
        self.addString("my_task","reconstruct_a1")
        self.addInt64("nrstep",v3fitInputs.nrstep)
        self.addDouble("dg2_stop",v3fitInputs.dg2_stop)
        self.addDouble("cut_svd",v3fitInputs.cut_svd)
        self.addDouble("cut_marg_eff",v3fitInputs.cut_marg_eff)
        self.addDouble("cut_delta_a",v3fitInputs.cut_delta_a)
        self.addDouble("cut_eff",v3fitInputs.cut_eff)
        self.addDouble("cut_dg2",v3fitInputs.cut_dg2)
        self.addDouble("astep_max",v3fitInputs.astep_max)
        self.addString("step_type",step_types[int(v3fitInputs.step_type)])
        
        
    def writeV3FITModels(self,v3fitInputs):
        print("Writing V3FIT Models")
        self.addComment("Model Specifications")

    def writeV3FITDerivedParameters(self,v3fitInputs):
        print("Writing V3FIT Derived Parameters")
        self.addComment("Derived Parameters")
        self.addInt32("n_dp",v3fitInputs.n_dp)
        
    def writeV3FITReconParameters(self,v3fitInputs):
        print("Writing V3FIT Recon Parameters")
        self.addComment("Reconstruction Parameters")
        self.addInt32("n_rp",v3fitInputs.n_rp)
        print("n_rp = ",v3fitInputs.n_rp)
        for rp in range(v3fitInputs.n_rp):
            print("rp = ",rp)
            self.addString(self.formatTo1D("rp_type",rp+1), \
                           rp_types[int(v3fitInputs.rp_type[rp])])
            self.addDouble(self.formatTo1D("rp_vrnc",rp+1), \
                           v3fitInputs.rp_vrnc[rp])
            self.addInt32(self.formatTo1D("rp_index",rp+1), \
                          v3fitInputs.rp_index[rp])
            self.addInt32(self.formatTo1D("rp_index2",rp+1), \
                          v3fitInputs.rp_index2[rp])
            
            tempName=self.formatToND("rp_range_type",[rp+1,-1])
            tempArray=[]
            for name in v3fitInputs.rp_range_type:
                tempArray+=[name]
            self.addStringArray1D(tempName,tempArray)
            
            tempName=self.formatToND("rp_range_value",[rp+1,-1])
            tempArray=[]
            for value in v3fitInputs.rp_range_value:
                tempArray+=[value]   
            self.addDoubleArray1D(tempName,tempArray)
            
            tempName=self.formatToND("rp_range_index",[rp+1,1,-1])
            tempArray=[]
            for value in v3fitInputs.rp_range_value:
                tempArray+=[value]   
            self.addDoubleArray1D(tempName,tempArray) 
            
            # I am not sure what this is for
            tempName=self.formatToND("rp_range_index",[rp+1,2,-1])
            tempArray=[]
            for value in v3fitInputs.rp_range_value:
                tempArray+=[value]   
            self.addDoubleArray1D(tempName,tempArray) 
            
    def formatTo1D(self,string,index):
        return(string+'('+str(index)+')')
        
    def formatToND(self,string,indexes):
        for idx, index in enumerate(indexes):
            if idx == 0:
                string=string+'('
            else:
                string=string+','
            if index >=0:
                string=string+str(index)
            else:
                string=string+':'
        return string+')'
             
                
    def writeV3FITBarLimiterSignal(self,v3fitInputs,idx):
        self.addComment("Bar Limiter")
        print("writing V3FIT Bar Limiter Signals")
        #self.addDouble(0.0)
        self.addInt32(self.formatTo1D("lif_on_edge",idx))  
    
    def writeV3FITCircularLimiterSignal(self,v3fitInputs):
        self.addComment("Bar Limiter")
        print("writing V3FIT Bar Limiter Signals")
        for idx in range(v3fitInputs.numberLimiters):
            self.addInt32(self.formatTo1D("lif_on_edge",idx))  

                
    def writeV3FITReconSignals(self,v3fitInputs):
        print("writing V3FIT Recon Signals")
        self.addComment("Reconstruction Signals")
        for signal in v3fitInputs.signalNames:
            idx=v3fitInputs.signalNames.index(signal)
            if signal.lower() == 'Bar Limiter'.lower():
                self.writeV3FITBarLimiterSignal(v3fitInputs,idx)
            elif signal.lower() == 'Circular Limiter'.lower():
                self.writeV3FITCircularLimiterSignal(v3fitInputs)
        
    
    def writeV3FITParameters(self,v3fitInputs):
        self.writeV3FITControls(v3fitInputs)
        self.writeV3FITModels(v3fitInputs)
        self.writeV3FITDerivedParameters(v3fitInputs)
        self.writeV3FITReconParameters(v3fitInputs)
        #self.writeV3FITReconSignals(v3fitInputs)
        
# -------------------------------------------------------------------------
#           Start of writing VMEC Parameters 
# -------------------------------------------------------------------------        
    
    def writeVMECHeader(self,shotNumber,shotTime):
        print("writing VMEC header")
        filetype='vmec'
        self.addString("File Type",filetype)
        self.addInt32("Shot Number",shotNumber)
        self.addDouble("Time Slice",shotTime)         

    def writeVMECExecutionParameters(self,vmecInputs):
        self.addComment("VMEC Exectuion Parameters")
        self.addString("MGRID_FILE",vmecInputs.MGRID_FILE)
        self.addBool("LFORBAL",vmecInputs.LFORBAL)
        self.addBool("LFREEB",vmecInputs.LFREEB)
        self.addDouble("DELT",vmecInputs.DELT)
        self.addDouble("TCON0",vmecInputs.TCON0)
        self.addInt32("NFP",vmecInputs.NFP)
        self.addInt32Array1D("NS_ARRAY",vmecInputs.NS_ARRAY)
        self.addDoubleArray1D("FTOL_ARRAY",vmecInputs.FTOL_ARRAY)
        self.addInt32("NITER",vmecInputs.NITER)
        self.addInt32("NSTEP",vmecInputs.NSTEP)
        self.addInt32("NTOR",vmecInputs.NTOR)
        self.addInt32("MPOL",vmecInputs.MPOL)
        self.addInt32("NZETA",vmecInputs.NZETA)
        self.addInt32("NVACSKIP",vmecInputs.NVACSKIP)
        self.addBool("LASYM",vmecInputs.LASYM)
        #self.addInt32("OMP_NUM_THREADS",vmecInputs.OMP_NUM_TREADS)
        self.addInt32("OMP_NUM_THREADS",1)
    
    def writeVMECCoilCurrents(self,vmecInputs):
        self.addComment("Coil Currents. (HF, TVF, OH, SVF, RF, TF, VV, HCF")
        
        coil_currents=[vmecInputs.hf_ovf_current[self.idx],\
                       vmecInputs.tvf_current[self.idx],\
                       vmecInputs.oh_current[self.idx],\
                       vmecInputs.svf_current[self.idx],\
                       vmecInputs.rf_ef_current[self.idx],\
                       vmecInputs.tf_current[self.idx],\
                       vmecInputs.vv_current[self.idx],\
                       vmecInputs.hcf_current[self.idx]]
        # setting the RF current to zero if LASYM is true    
        if vmecInputs.LASYM:
            coil_currents[4]=0.0
            
        self.addDoubleArray1D("EXTCUR",coil_currents)
        return self
    
    def writeVMECFitParameters(self,vmecInputs):
        self.addComment("Fitting Parameters")
        self.addDouble("GAMMA",vmecInputs.gamma)
        self.addDouble("PHIEDGE",vmecInputs.phiedge[self.idx])
        self.addDouble("BLOAT",vmecInputs.bloat)

    
    def writeVMECPositionParameters(self,vmecInputs):
        self.addComment("Initial Position")
        self.addDouble("RAXIS(0)",vmecInputs.raxis)
        self.addDouble("ZAXIS(0)",vmecInputs.zaxis)
        self.addDouble("RBC(0,0)",vmecInputs.rbc[0][self.idx])
        self.addDouble("RBC(0,1)",vmecInputs.rbc[1][self.idx])
        self.addDouble("ZBS(0,0)",vmecInputs.zbs[0][self.idx])
        self.addDouble("ZBS(0,1)",vmecInputs.zbs[1][self.idx])
    
    def writeVMECPlasmaCurrent(self,vmecInputs):
        self.addComment("Plasma Current Parameters") 
        self.addInt32("NCURR",vmecInputs.ncurr)
        self.addDouble("CURTOR",vmecInputs.curtor[self.idx])
        self.addDoubleArray1D("AC",vmecInputs.ac)
        self.addString("PCURR_TYPE",vmecInputs.pcurr_type)
        self.addDoubleArray1D("ac_aux_s",vmecInputs.ac_aux_s)
        self.addDoubleArray1D("ac_aux_f",vmecInputs.ac_aux_f)
    
    def writeVMECPlasmaPressure(self,vmecInputs):
        self.addComment("Plasma Pressure Parameters")
        self.addDouble("SPRES_PED",vmecInputs.spres_ped)   
        self.addDoubleArray1D("AM",vmecInputs.am)
        self.addDouble("PRES_SCALE",vmecInputs.pres_scale[self.idx])
        self.addString("PMASS_TYPE",vmecInputs.pmass_type)
        self.addDoubleArray1D("am_aux_s",vmecInputs.am_aux_s)
        self.addDoubleArray1D("am_aux_f",vmecInputs.am_aux_f)
        
    def writeVMECParameters(self,vmecInputs):
        self.writeVMECExecutionParameters(vmecInputs)
        self.writeVMECCoilCurrents(vmecInputs)
        self.writeVMECFitParameters(vmecInputs)
        self.writeVMECPositionParameters(vmecInputs)
        self.writeVMECPlasmaCurrent(vmecInputs)
        self.writeVMECPlasmaPressure(vmecInputs)
        




# testing

#
#shotNumber=16121246
#time=1.61
#filetype='vmec'
#rs=ReconstructionString(0)
#rs.writeVMECHeader(shotNumber,time)
#rs.addComment("This is a test")
#rs.addBool("T or F",True)
#rs.addInt8("INT8",8)
#rs.addInt16("INT16",16)
#rs.addInt32("INT32",32)
#rs.addInt64("INT64",64)
#rs.addFloat("FLOAT",time)
#rs.addDouble("Double",time)
#rs.addBoolArray1D("Boolean Array",[True,True,False,True])
#rs.addInt8Array1D("Int8Array",[1,2,3,4])
#rs.addInt16Array1D("Int16Array",[1,2,3,4])
#rs.addInt32Array1D("Int32Array",[1,2,3,4])
#rs.addInt64Array1D("Int64Array",[1,2,3,4])
#rs.addFloatArray1D("Float Array",[1,2,3,4])
#rs.addDoubleArray1D("Double Array",[1.1,2.2,3.3,4.4])
#rs.addDoubleArray1D("single entry double array test",'6.6')
#rs.addStringArray1D('Currents',['HF','TVF','OH'])
#rs.addEOF()
#rs.print()

    