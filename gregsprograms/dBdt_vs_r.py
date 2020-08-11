# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 09:48:48 2020

@author: hartwgj
"""
# dBdt_vs_r calculates the dB/dt given a set of B-field components for a 
# given current at a given position

from CTHdata import CTHData
import matplotlib.pyplot as plt
from scipy import signal
import numpy as np


def dBdt_vs_r(shot,fwidth,idx):
    
    #define positions and components for 1000A unit current fields
    r_positions=[1.5437,1.8,2.2]
    BrHF=[9.892e-3,2.971e-3,6.771e-4]
    BpHF=[3.351e-3,1.195e-3,2.921e-4]
    BzHF=[-9.362E-3,-4.418E-3,1.161e-3]
    
    BrTVF=[3.996e-3,3.36e-4,-4.737e-4]
    BpTVF=[-1.518e-6,-9.987e-7,-5.681e-7]
    BzTVF=[2.261e-3,7.424e-3,5.918e-3]
    
    BrTF=[1.349e-2,2.177e-3,2.044e-4]
    BpTF=[1.968e-3,8.751e-5,4.611e-6]
    BzTF=[1.594e-3,2.051e-4,1.193e-5]
    
    BrOH=[-5.852e-5,1.775e-5,1.769e-5]
    BpOH=[-5.174e-7,-3.826e-7,-2.163e-7]
    BzOH=[-3.259e-4,-3.009e-4,-2.036e-4]
    
    # get the currents
    
    HF=CTHData('HF')
    TVF=CTHData('TVF')
    TF=CTHData('TF')
    OH=CTHData('OH')
    
    HF.get_data(shotnum=shot,node='\\I_HFOVF')
    TVF.get_data(shotnum=shot,node='\\I_TVF')
    TF.get_data(shotnum=shot,node='\\I_TF')
    OH.get_data(shotnum=shot,node='\\I_OH')
    
    HFdata=HF.data[0:47999]
    TVFdata=TVF.data[0:47999]
    TFdata=TF.data[0:47999]
    
    # need to upsample the HF, TVF, TF arraya
    
    HFdata = signal.resample(HFdata,len(OH.data))
    TVFdata = signal.resample(TVFdata,len(OH.data))
    TFdata = signal.resample(TFdata,len(OH.data))
    
    #Convert to unit currents in 
    HFdata=np.array(HFdata)/1000.0
    TVFdata=np.array(TVFdata)/1000.0
    TFdata=np.array(TFdata)/1000.0
    OHdata=np.array(OH.data)/1000.0
    taxis=OH.taxis
    
    # these plot statements confirm that arrays have same time bais
    # plt.plot(taxis,HFdata)
    # plt.plot(taxis,TVFdata)
    # plt.plot(taxis,TFdata)
    
    # plt.plot(taxis,OHdata)
    # plt.show()
    
    # plt.xlim(xmin,xmax)
    # plt.title('dBmod/dt')
    # plt.show()

    print('position =',r_positions[idx])
    Br = BrHF[idx]*HFdata + BrTVF[idx]*TVFdata \
        + BrTF[idx]*TFdata + BrOH[idx]*OHdata
    Bp = BpHF[idx]*HFdata + BpTVF[idx]*TVFdata \
        + BpTF[idx]*TFdata + BpOH[idx]*OHdata
    Bz = BzHF[idx]*HFdata + BzTVF[idx]*TVFdata \
        + BzTF[idx]*TFdata + BzOH[idx]*OHdata     
    

  
    if fwidth >=5:
        # window size fwidth, polynomial order 3
        Br=signal.savgol_filter(Br, fwidth, 3) 
        Bp=signal.savgol_filter(Bp, fwidth, 3)
        Bz=signal.savgol_filter(Bz, fwidth, 3)
    dBrdt=np.gradient(Br) /np.gradient(taxis)
    dBpdt=np.gradient(Bp)/np.gradient(taxis)
    dBzdt=np.gradient(Bz)/np.gradient(taxis)

    dBrdt=np.gradient(Br)/1.0E-5
    dBpdt=np.gradient(Bp)/1.0E-5
    dBzdt=np.gradient(Bz)/1.0E-5

    # plt.plot(taxis,np.gradient(taxis))
    # plt.title('gradient')
    # plt.show()
    # print('length',len(taxis))

    if fwidth >=5:
        dBrdt=signal.savgol_filter(dBrdt, fwidth, 3)
        dBpdt=signal.savgol_filter(dBpdt, fwidth, 3)
        dBzdt=signal.savgol_filter(dBzdt, fwidth, 3)
    xmin=0.0
    xmax=2.0
    print('max d(Br)/dt',max(dBrdt))
    print('max d(Bp)/dt',max(dBpdt))
    print('max d(Bz)/dt',max(dBzdt))
    
    # maxBr=max(dBrdt)
    # maxBp=max(dBpdt)
    # maxBz=max(dBzdt)
    
    dbmod=np.sqrt(dBrdt**2+dBpdt**2+dBzdt**2)
    print('max d(bmod)/dt',max(dbmod))
    
    # plt.plot(taxis,dbmod)
    # plt.xlim(xmin,xmax)
    # plt.title('dBmod/dt')
    # plt.show()
    
    # print('max dBmod',np.sqrt(maxBr**2+maxBp**2+maxBz**2))
    # plt.plot(taxis,dBrdt)
    # plt.xlim(xmin,xmax)
    # plt.title("dBr/dt all coils")
    # plt.show()
    
    # plt.plot(taxis,dBpdt)
    # plt.title("dBp/dt all coils")
    # plt.xlim(xmin,xmax)
    # plt.show()
    
    # plt.plot(taxis,dBzdt)
    # plt.title("dBz/dt all coils")
    # plt.xlim(xmin,xmax)
    # plt.show()
    
    # ## OH only data
    # OHdata=np.array(OH.data)/1000.0
    # Br = BrOH[idx]*OHdata
    # Bp = BpOH[idx]*OHdata
    # Bz = BzOH[idx]*OHdata     
    # taxis=OH.taxis
    
    # dBrdt=np.gradient(Br)/np.gradient(taxis)
    # dBpdt=np.gradient(Bp)/np.gradient(taxis)
    # dBzdt=np.gradient(Bz)/np.gradient(taxis)
    
    # plt.plot(taxis,OH.data)
    # plt.show()
    
 
    # taxist=timeSubset(taxis,taxis,1.6,1.7)
    # dBrdt=timeSubset(taxis,dBrdt,1.6,1.7)
    # dBpdt=timeSubset(taxis,dBpdt,1.6,1.7)
    # dBzdt=timeSubset(taxis,dBzdt,1.6,1.7)
    
    # print(len(taxis),len(dBrdt))
    
    # plt.plot(taxist,dBrdt)
    # plt.title("dBr/dt OH only")
    # plt.show()
    
    # plt.plot(taxist,dBpdt)
    # plt.title("dBp/dt OH only")
    # plt.show()
    
    # plt.plot(taxist,dBzdt)
    # plt.title("dBz/dt OH only")
    # plt.show()
    