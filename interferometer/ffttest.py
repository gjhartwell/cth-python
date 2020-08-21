# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 13:08:46 2020

@author: hartwgj
"""

import scipy.constants
import numpy as np
import matplotlib.pyplot as plt


pi=scipy.constants.pi
print(pi)
f=1000
length=10000
# create a sin function for 1 second
dt=1.0/length
t=np.arange(length)/length
data=np.sin(2.0*pi*f*t)

# plt.plot(t,data)
# plt.show()

datafft=np.fft.fft(data)
tfft=np.array(np.linspace(0.0,1.0/(2.0*dt),length//2))


tfft=np.concatenate((tfft,np.flip(tfft)))

#plt.plot(np.abs(datafft))
plt.plot(datafft)
plt.show()



plotdatafft=np.abs(datafft[0:length//2])*2.0/length
plottfft=np.linspace(0.0,1.0/(2.0*dt),length//2)

plt.plot(plottfft,plotdatafft)
plt.show()



