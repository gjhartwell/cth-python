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
    r_positions=[1.6125,2.2313]
    BrHF=[7.000E-3,6.134E-4]
    BpHF=[2.528E-3,2.644E-4]
    BzHF=[-7.424E-3,-1.528E-3]
    
    BrTVF=[2.548e-3,-4.704e-4]
    BpTVF=[-1.35e-6,-5.457e-7]
    BzTVF=[4.849e-3,5.736e-3]
    
    BrTF=[8.083e-3,1.738e-4]
    BpTF=[7.902e-4,3.956e-6]
    BzTF=[8.922e-4,9.53e-6]
    
    BrOH=[2.974E-7,1.715e-5]
    BpOH=[-5.174e-7,-2.078e-7]
    BzOH=[-3.291e-4,-1.969e-4]
    
    # get the currents
    
    HF=CTHData('HF')
    TVF=CTHData('TVF')
    TF=CTHData('TF')
    OH=CTHData('OH')
    
    HF.get_data(shotnum=shot,node='\\I_HFOVF')
    TVF.get_data(shotnum=shot,node='\\I_TVF')
    TF.get_data(shotnum=shot,node='\\I_TF')
    OH.get_data(shotnum=shot,node='\\I_OH')
    
    
    # need to downsample the OH array
    
    HFdata = signal.resample(HF.data,len(OH.data))
    TVFdata = signal.resample(TVF.data,len(OH.data))
    TFdata = signal.resample(TF.data,len(OH.data))
    
    HFdata=np.array(HFdata)/1000.0
    TVFdata=np.array(TVFdata)/1000.0
    TFdata=np.array(TFdata)/1000.0
    OHdata=np.array(OH.data)/1000.0
    taxis=OH.taxis
    
    plt.plot(taxis,HFdata)
    plt.plot(taxis,TVFdata)
    plt.plot(taxis,TFdata)
    plt.plot(taxis,OHdata)
    plt.show()
    
    plt.xlim(xmin,xmax)
    plt.title('dBmod/dt')
    plt.show()

    print('position =',r_positions[idx])
    Br = BrHF[idx]*HFdata + BrTVF[idx]*TVFdata \
        + BrTF[idx]*TFdata + BrOH[idx]*OHdata
    Bp = BpHF[idx]*HFdata + BpTVF[idx]*TVFdata \
        + BpTF[idx]*TFdata + BpOH[idx]*OHdata
    Bz = BzHF[idx]*HFdata + BzTVF[idx]*TVFdata \
        + BzTF[idx]*TFdata + BzOH[idx]*OHdata     
    

  
    if fwidth >=5:
        Br=signal.savgol_filter(Br, fwidth, 3) # window size fwidth, polynomial order 3
        Bp=signal.savgol_filter(Bp, fwidth, 3)
        Bz=signal.savgol_filter(Bz, fwidth, 3)
    dBrdt=np.gradient(Br) /np.gradient(taxis)
    dBpdt=np.gradient(Bp)/np.gradient(taxis)
    dBzdt=np.gradient(Bz)/np.gradient(taxis)

    if fwidth >=5:
        dBrdt=signal.savgol_filter(dBrdt, fwidth, 3)
        dBpdt=signal.savgol_filter(dBpdt, fwidth, 3)
        dBzdt=signal.savgol_filter(dBzdt, fwidth, 3)
    xmin=0.0
    xmax=2.0
    print('max Br',max(dBrdt))
    print('max Bp',max(dBpdt))
    print('max Bz',max(dBzdt))
    
    maxBr=max(dBrdt)
    maxBp=max(dBpdt)
    maxBz=max(dBzdt)
    
    dbmod=np.sqrt(dBrdt**2+dBpdt**2+dBzdt**2)
    print('max bmod 2',max(dbmod))
    
    plt.plot(taxis,dbmod)
    plt.xlim(xmin,xmax)
    plt.title('dBmod/dt')
    plt.show()
    
    print('max dBmod',np.sqrt(maxBr**2+maxBp**2+maxBz**2))
    plt.plot(taxis,dBrdt)
    plt.xlim(xmin,xmax)
    plt.title("dBr/dt all coils")
    plt.show()
    
    plt.plot(taxis,dBpdt)
    plt.title("dBp/dt all coils")
    plt.xlim(xmin,xmax)
    plt.show()
    
    plt.plot(taxis,dBzdt)
    plt.title("dBz/dt all coils")
    plt.xlim(xmin,xmax)
    plt.show()
    
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
    