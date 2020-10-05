# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 10:12:09 2018

@author: Greg

Last modified Jun 25, 2020
"""

from readV3Data.findAverageValues import findAverageValues

rp_types=["ac","ac_aux_s","ac_aux_f",\
         "ai","ai_aux_s","ai_aux_f", \
         "am","am_aux_s","am_aux_f", \
         "bloat","extcut","curtor","phiedge","pres_scale", \
         "rbc", "rbs", "zbc", "zbs", \
         "density_max","density_tau", \
         "pp_ne_b", "pp_ne_as","pp_ne_af", \
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
        self.dp_type=''
    
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
        self.n_mag_signals = 0
        self.n_sxr_signals = 0
        self.n_int_signals = 0
        # signalNames may be magnetic,sxr,int,bar_limiter,circular_limiter
        # coosig
        self.signalNames=[]
    
    # signals
        self.sdo_data_a=[]
        self.magnetic_data=[]
        self.sxr_data=[]
        self.int_data=[]
        
    # signal weights
        self.sdo_w_spec_weight =[]
        self.sdo_w_spec_imin=[]
        self.sdo_w_spec_imax=[]
    
    # signal Sigma
        self.sdo_s_spec_floor =[]
        self.sdo_s_spec_fraction =[] 
        self.sdo_s_spec_imin=[]
        self.sdo_s_spec_imax=[]
        self.sdo_sigma_a=[]

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
        self.lif_arz=[]
    
   # Magnetics information
        self .mdsig_list_filenema=''
   
   # SXR information
        self.sxrch_dot_file=''
        self.num_sxrem_p = 0
        self.pp_sxrem_p_types=['two_power','power_series','akima_spline',
                          'cubic_spline','line_segment','two_power_gs']
        self.model_sxrem_type=["two_power"]
        self.pp_sxrem_as=[]
        self.pp_sxrem_af=[]
        self.pp_sxrem_ptype=[]
        self.pp_sxrem_b=[]
    
   # Interferometer information
        self.ne_pp_unit=0.0
        self.ne_min=0.0
        self.pp_ne_types=['two_power','power_series','akima_spline',
                          'cubic_spline','line_segment','two_power_gs']
        self.pp_ne_ptype="two_power"
        self.pp_ne_b=[]
        self.pp_ne_as=[]
        self.pp_ne_af=[]
        self.int_file=''
    
   # Thomson Scattering information     
    
    
    def V3FITmoveToClass(self,shot,parsedLine,shotData,dataNames,debug):
        if debug:
            print("==========================================================")
            print("in V3FITmoveToClass")
            print(parsedLine)
        # remove 'class'
        removeItems=['class','v3fit_data','int_diagnostic']
        for item in removeItems:
            while item in parsedLine: parsedLine.remove(item)
        
        if debug: print(parsedLine)
        
        for v in parsedLine:
            if debug: 
                print("")
                print ("In V3FITmoveToClass - searching for data name:",v)
            if v in dataNames:
                idx=dataNames.index(v)
                if debug:
                    print("found data %s at %d of %d" % (v,idx,len(shotData)))
                data=shotData[idx]
                if debug: print(data)
                if type(data.getData()) is str:
                    setattr(self,v,data.getData())
                else:
                    if type(data) is list:
                        if debug: print(" this is a list of length",len(data))
                        averageDataArray=[]
                        for item in data:
                            averageData=findAverageValues(item,shot)
                            averageDataArray+=[averageData]
                    else:
                        averageData=findAverageValues(data,shot)
                    setattr(self,v,averageData)
                
            else:
                print("In V3FITmoveToClass, no data found for ",v)
                
    def V3FITmoveToClass2(self,shot,parsedLine,shotData,dataNames,debug):
        if debug:
            print("==========================================================")
            print("in V3FITmoveToClass2")
            print(parsedLine)
        # remove 'class'
        removeItems=['class','v3fit_data']
        for item in removeItems:
            while item in parsedLine: parsedLine.remove(item)
        
        if debug: print(parsedLine)
        inMagSig=False
        inSXRSig=False
        inIntSig=False
        for v in parsedLine:
            if debug: 
                print("")
                print ("In V3FITmoveToClass2 - searching for data name:",v)
            if v=='magnetic_diagnostic':
                inMagSig=True
            elif v=='sxr_diagnostic':
                inMagSig=False
                inSXRSig=True
            elif v=='int_diagnostic':
                inSXRSig=False
                inIntSig=True
            
            elif v in dataNames:
                idx=dataNames.index(v)
                if debug:
                    print("found data %s at %d of %d" % (v,idx,len(shotData)))
                data=shotData[idx]
                if debug: print(data)
                if type(data.getData()) is str:
                    setattr(self,v,data.getData())
                else:
                    averageData=findAverageValues(data,shot)
                    self.n_signals+=1
                    if inMagSig: 
                        self.magnetic_data.append(averageData)
                        self.n_mag_signals+=1
                        self.sdo_data_a.append(averageData)
                        self.signalNames.append('magnetic')
                        self.n_signals+=1
                    elif inSXRSig:
                        self.sxr_data.append(averageData)
                        self.n_sxr_signals+=1
                        self.sdo_data_a.append(averageData)
                        self.signalNames.append('sxr')
                        self.n_signals+=1
                    elif inIntSig: 
                        self.int_data.append(averageData)
                        self.n_int_signals+=1
                        self.sdo_data_a.append(averageData)
                        self.signalNames.append('int')
                        self.n_signals+=1
                        
                        
                
            else:
                print("In V3FITmoveToClass2, no data found for ",v)
            
    
#-----------------------------------------------------------------------------
#   End of moveToClass
#-----------------------------------------------------------------------------