# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 16:01:35 2020

@author: hartwgj
"""
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 08:48:38 2017

@author: Greg
"""

import matplotlib.pyplot as plt
from CTHdata import CTHData
import numpy as np


shot = 20032705
tvf=CTHData("atest")
tvf.get_data(shotnum=shot,tag='\\I_TVF')

curtor=CTHData("atest")
curtor.get_data(shotnum=shot,tag='\\I_P')



tvf.data=np.interp(curtor.taxis,tvf.taxis,tvf.data)
tvf.taxis=curtor.taxis

plt.plot(tvf.taxis,tvf.data)
plt.xlim(1.6,1.7)
plt.show()

plt.plot(curtor.taxis,curtor.data)
plt.xlim(1.6,1.7)
plt.show()

dat=tvf.data*(-2.216E-5)+curtor.data*(-2.192E-7)-.01576

plt.plot(curtor.taxis,dat)
plt.xlim(1.6,1.7)
plt.show()

