# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 10:59:37 2020

@author: hartwgj
"""


import matplotlib.pyplot as plt
from vmec import wout_file
from vmec import get_iotabar


#file='C:\\Users\\hartwgj\\Documents\\Reconstructions\\shots_200327\\shot_20032705\\20032705ls\\wout_20032705_1.64_2.nc'#
#file="C:\\Users\\hartwgj\\Documents\\Reconstructions\\Steve_Recon_Pack_2016\\18102253\\wout_18102253_1.61_3.nc"
#file=r'C:\Users\hartwgj\Desktop\TestReconFiles\20032705'
file=r'C:\Users\hartwgj\Documents\Reconstructions\Nic20072944\20072944\wout_20072944_1.61_0.nc'
test=wout_file(file)

s,iotabar=get_iotabar(test)

plt.plot(s,iotabar,'ro')
plt.title('rotational transform plot')
plt.ylabel(r'iota bar - rotational transform')
plt.xlabel('s - normalized toroidal flux')
plt.show()


