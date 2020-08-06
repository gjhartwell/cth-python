# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 10:59:18 2018

@author: Greg
"""

from findAverageValues import findAverageValues
from ReconstructionString import ReconstructionString

class VMECData(object):
    
    # This class stores the information for a single shot/time slice pair
    # if multiple time slices are associated with a shot, there will be
    # multiple instances of this class
    
    def __init__(self):

    # these become the default execution parameters
    # need to create a method to change these if a
        # self.LFORBAL = False
        # self.LFREEB = True
        # self.DELT = 0.0
        # self.TCON0 = 0.0
        # self.NFP = 0
        # self.NS_ARRAY = [0]
        # self.FTOL_ARRAY = [1.0E-20]
        # self.NITER = 0
        # self.NSTEP = 0
        # self.NTOR = 0
        # self.MPOL = 0
        # self.NZETA = 0
        # self.NVACSKIP = 0
        # self.MGRID_FILE = ""
        # self.LASYM = False
        # self.OMP_NUM_THREADS = 1
        
        self.lforbal = False
        self.lfreeb = True
        self.delt = 0.0
        self.tcon0 = 0.0
        self.nfp = 0
        self.ns_array = [0]
        self.ftol_array = [1.0E-20]
        self.nitier = 0
        self.nstep = 0
        self.ntor = 0
        self.mpol = 0
        self.nzeta = 0
        self.nvacskip = 0
        self.mgrid_file = ""
        self.lasym = False
        self.omp_num_threads = 1


    #Coil Currents
        self.hf_ovf_current=0.0
        self.tvf_current=0.0
        self.oh_current=0.0
        self.svf_current=0.0
        self.rf_ef_current=0.0
        self.tf_current=0.0
        self.vv_current=0.0
        self.hcf_current=0.0

    # Plasma Current Related
        self.pcurr_types=['gauss_trunc', 'two_power','sum_atan',
                          'power_series_I','Akima_spline_Ip','AAkima_spline_I',
                          'cubic_spline_Ip','cubic_spline_I','pedestal',
                          'rational','power_series', 'two_power_gs',
                          'line_segment_Ip','line_segmen_I']
        self.ncurr=0
        self.curtor=0.0
        self.ac=[]
        self.pcurr_type="two_power"
        self.ac_aux_s=[]
        self.ac_aux_f=[]

    # Plasma Pressure Related
        self.pmass_types=['gauss_trunc', 'two_power', 'two_Lorentz',
                          'Akima_spline','cubic_spline','pedestal','rational',
                          'power_series','line_segment', 'two_power_gs']
        self.pres_scale=0.0
        self.spres_ped=0.0
        self.am=[]
        self.pmass_type="two_power"
        self.am_aux_s=[]
        self.am_aux_f=[]        
        
    # initial position realted
        self.rbc=[]
        self.zbs=[]
        self.raxis=0.0
        self.zaxis=0.0

    # VMEC fitting parameters
        self.phiedge=0.0
        self.gamma=0.0
        self.bloat=0.0
        
    # define setting routines
    
#-----------------------------------------------------------------------------
# end of VMECData class
#-----------------------------------------------------------------------------
    
    def VMECmoveToClass(self,shot,parsedLine,shotData,dataNames,debug):
        if debug:
            print("=========================================================")
            print("in VMECmoveToClass")
        members=['coil_currents','plasma_current','plasma_pressure',
                 'fit_parameters','positioning']
        
        if debug: print(parsedLine)
        # remove 'class'
        removeItems=['class','vmec_data']
        for item in removeItems:
            while item in parsedLine: parsedLine.remove(item)
        for item in members:
            while item in parsedLine: parsedLine.remove(item)
        

        parsedLine.reverse()
        if debug: print(parsedLine)
        stack=[]
        nameStack=[]        
        for v in parsedLine:
            if debug: 
                print("")
                print ("searching for data name:",v)
            if v in dataNames:
                idx=dataNames.index(v)
                if debug: 
                    print("found data %s at %d of %d" % (v,idx,len(shotData)))
                data=shotData[idx]
                
                if type(data) is list:
                    if debug:
                        print(" this is a list of length",len(data))
                    averageDataArray=[]
                    for item in data:
                        averageData=findAverageValues(item,shot)
                        averageDataArray+=[averageData]
                    stack.insert(0,averageDataArray)
           
                else:
                    averageData=findAverageValues(data,shot)
                    stack.insert(0,averageData)

                name=v
                value=stack.pop(0)
                if debug: 
                    print("in VMECmoveToClass",name,value)
                setattr(self,name,value)
            
            else:
                print(v," Is unrecognized in VMECmoveToClass")
            
            
    
#-----------------------------------------------------------------------------
#   End of moveToClass
#-----------------------------------------------------------------------------
    
#parsedData=['class', 'vmec_data', 'class', 'coil_currents', 'hf_ovf_current',
#            'tvf_current', 'oh_current', 'svf_current', 'rf_ef_current', 
#            'tf_current', 'vv_current', 'hcf_current', 'class', 
#            'plasma_current', 'curtor', 'class', 'plasma_pressure', 
#            'pres_scale', 'class', 'fit_parameters', 'phiedge', 'class', 
#            'positioning', 'rbc', 'zbs']
#
#mydata=VMECData()
#mydata.VMECmoveToClass(shot,parsedData,alldata,dataNames)


    
    