# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 10:12:09 2018

@author: Greg

Last modified Jun 25, 2020
"""

from findAverageValues import findAverageValues

rp_types=["ac","ac_aux_s","ac_aux_f",\
         "ai","ai_aux_s","ai_aux_f", \
         "am","am_aux_s","am_aux_f", \
         "bloat","extcut","curtor","phiedge","pres_scale", \
         "rbc", "rbs", "zbc", "zbs", \
         "density_max","density_tau", \
         "pp_ne_b", "pp_ne_as","pp_ne_nf" \
         "pp_sxrem_b_a","pp_sxrem_af_a", \
         "pp_te_b","pp_te_as","pp_te_af", \
         "ac_edge","am_edge","phi_offset", "z_offset"]

step_types=["sl","seg","lm"]

rp_range_types=["infinity","value", \
                "ne_unit","ne_min","pressure_fraction",\
                "ac","ac_aux_s","ac_aux_f",\
                "ai","ai_aux_s","ai_aux_f", \
                "am","am_aux_s","am_aux_f", \
                "bloat", \
                "rbc", "rbs", "zbc", "zbs", \
                "extcut","phiedge","pres_scale"
                "density_max","density_tau", \
                "pp_ne_b", "pp_ne_as","pp_ne_nf" \
                "pp_sxrem_b","pp_sxrem_af_a", \
                "pp_te_b","pp_te_as","pp_te_af", \
                "rmnc","zmns","lmns","gmnc", \
                "bsubsmns","bsubumnc","bsumvmnc", "bsupumnc","bsupvmnc", \
                "rmns","zmnc","lmnc", "gmns", \
                "bsubsmnc","bsubumns","bsubvmns","bsupumns","bsupvmns", \
                "phi","iotas","iotaf", \
                "vvc_smaleli","vvc_kappa","phi_offset", "z_offset"]

signal_types=["Limiter","Magnetic","SXR","Thompson","Density","Combination"]

derived_parameters=["rmnc","zmns","lmns","gmnc", \
                     "bsubsmns","bsubumnc","bsumvmnc", "bsupumnc","bsupvmnc", \
                     "rmns","zmnc","lmnc", "gmns", \
                     "bsubsmnc","bsubumns","bsubvmns","bsupumns","bsupvmns", \
                     "phi","iotaf","iotas", \
                     "vvc_smaleli","vvc_kappa", \
                     "betapol","betatot","betator","betaxis"]

class V3FITData(object):

    def __init__(self):
        # v3fit running paramaters
        self.nrstep = 0
        self.dg2_stop = 0.0
        self.cut_svd = 0.0
        self.cut_eff = 0.0
        self.cut_marg_eff = 0.000000
        self.cut_delta_a = 0.000000
        self.cut_dg2 = 0.000000
        self.astep_max = 0.0
        self.step_type = 0

    # derived parameters
        self.n_dp = 0
    
    # reconstruction parameters
        self.n_rp = 0
        self.rp_type = []
        self.rp_index = []
        self.rp_index2 = []
        self.rp_vrnc = []
        self.rp_range_type= []
        self.rp_range_value = []
        self.rp_range_index = []
   
    #   counters and names
        self.n_signals = 0
        self.signalNames=[]
        
    # signal weights
        self.sdo_w_spec_weight =[]
        self.sdo_w_spec_imin=[]
        self.sdo_w_spec_imax=[]
    
    # signal Sigma
        self.sdo_s_spec_floor =[]
        self.sdo_s_spec_fraction =[] 
        self.sdo_s_spec_imin=[]
        self.sdo_s_spec_imax=[]

        self.coosig_type =[]
        self.coosig_indices =[]
        self.coosig_coeff =[]
        self.coosig_name =[]
        self.coosig_units = []
       
        self.nBarLimiters=0
        self.r = []
        self.z =[]
        self.lif_on_edge =[]
        self.lif_phi_degree = []
        self.lif_sigma =[]
        self.lif_rc =[]
        self.lif_zc =[]

    # Circular Limiter Signals
        self.nCircularLimiters=0
        self.radius =[]
        self.lif_on_edge =[]
        self.lif_phi_degree = []
        self.lif_sigma =[]
        self.lif_rc =[]
        self.lif_zc =[]
    
    def V3FITmoveToClass(self,shot,parsedLine,shotData,dataNames):
        print("==============================================================")
        print("in V3FITmoveToClass")
        print(parsedLine)
        # remove 'class'
        removeItems=['class','v3fit_data']
        for item in removeItems:
            while item in parsedLine: parsedLine.remove(item)
        
        print(parsedLine)
        
        for v in parsedLine:
            print("")
            print ("searching for data name:",v)
            if v in dataNames:
                idx=dataNames.index(v)
                print("found data %s at %d of %d" % (v,idx,len(shotData)))
                data=shotData[idx]
                print(data)
                if type(data) is list:
                    print(" this is a list of length",len(data))
                    averageDataArray=[]
                    for item in data:
                        averageData=findAverageValues(item,shot)
                        averageDataArray+=[averageData]
                else:
                    averageData=findAverageValues(data,shot)
                setattr(self,v,averageData)
                
            else:
                print("Oops, no data found for ",v)
            
            
            
    
#-----------------------------------------------------------------------------
#   End of moveToClass
#-----------------------------------------------------------------------------