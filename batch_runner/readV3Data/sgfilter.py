# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 13:01:42 2020

@author: hartwgj
"""

from cthmds.CTHdata import CTHData
import matplotlib.pyplot as plt
from scipy import signal
from timeSubset import timeSubset
import numpy as np


def sgfilter(dat,filterfreq):
    
    datafreq=datafreq=(len(dat.taxis)-1)/(dat.taxis[-1]-dat.taxis[0])
    filterlen=int(datafreq/filterfreq)
    if (filterlen % 2) == 0: filterlen+=1
    if filterlen > 3:
        dat.data=signal.savgol_filter(dat.data,filterlen,3) 
    return dat
    
d=CTHData('temp')
d.get_data(server='mds',shotnum=20032705,channel=171)

plt.plot(d.taxis,d.data,'b')
d=sgfilter(d,2000)

dataRange=timeSubset(d.taxis,d.data,1.61,1.615)
value=np.sum(dataRange)/np.size(dataRange)

plt.plot(d.taxis,d.data-value,'r')
plt.show()


