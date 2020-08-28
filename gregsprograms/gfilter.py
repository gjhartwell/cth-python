# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 13:01:42 2020

@author: hartwgj
"""

#from cthmds.CTHdata import CTHData
#import matplotlib.pyplot as plt
from scipy import signal

def gfilter(dat,filterfreq):
    
    datafreq=datafreq=(len(dat.taxis)-1)/(dat.taxis[-1]-dat.taxis[0])
    print('datafreq',datafreq)
    dt=dat.taxis[1]-dat.taxis[0]
    print('dt',dt)
    
    filterlen=int(datafreq/filterfreq)+1
    print('filterlen',filterlen)
    if filterlen > 3:
        dat.data=signal.savgol_filter(dat.data,filterlen,3) 
    return d
    
# d=CTHData('temp')
# d.get_data(server='mds',shotnum=20032705,channel=171)

# plt.plot(d.taxis,d.data,'b')
# d=gfilter(d)
# plt.plot(d.taxis,d.data,'r')
# plt.show()