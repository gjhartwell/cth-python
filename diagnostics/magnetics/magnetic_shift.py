# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 10:03:57 2020

@author: James Kring
@email:  jdk0026@auburn.edu
"""

from cthmds.cthdata_james import CTHData
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


class MagneticAxisVerticalShift:
    def __init__(self, shot):
        self.shot = shot
        self.get_data()
    
    def get_data(self):
        time = CTHData(self.shot, 90, channel_number=True).time
        self.time = time
        
        p_time_ind = self.find_closest_index(time, 1.61)        
        
        self.ind1 = self.find_closest_index(time, time[p_time_ind]-0.001)
        self.ind2 = self.find_closest_index(time, time[p_time_ind]+0.001)
        
        self.cube_BA =0.613534* CTHData(self.shot, 90, channel_number=True).data
        self.cube_EB = -0.613534*CTHData(self.shot, 97, channel_number=True).data
        
        
        def linfit(x, m, b):
            y = x*m + b
            return y


        ft1 = self.find_closest_index(time, 0)
        ft2 = self.find_closest_index(time, .1)
        time_fit = time[ft1:ft2]        
        cube_BA_fit = self.cube_BA[ft1:ft2]
        cube_EB_fit = self.cube_EB[ft1:ft2]
        
        self.BA_fit, pcov = curve_fit(linfit,time_fit, cube_BA_fit)
        self.EB_fit, pcov = curve_fit(linfit,time_fit, cube_EB_fit)
        #print(self.BA_fit, self.EB_fit)
        
        self.cube_BA = self.cube_BA - self.BA_fit[1] - self.BA_fit[0] * time
        self.cube_EB = self.cube_EB - self.EB_fit[1] - self.EB_fit[0] * time

        tm1 = self.find_closest_index(time, 1.618)
        tm2 = self.find_closest_index(time, 1.619)
        
        self.cube_BA = self.cube_BA - np.mean(self.cube_BA[tm1:tm2])
        self.cube_EB = self.cube_EB - np.mean(self.cube_EB[tm1:tm2])  
        
        z_cubeEB= 0.268
        z_cubeBA=-0.271
        a   = .29
        
        self.z = (self.cube_EB * z_cubeEB + self.cube_BA * z_cubeBA)/(self.cube_EB+self.cube_BA)
        self.delta_za = self.z / a
        return
        
        
    def rm_mut(self, raw_array, coil_array, mutual_array):
        #mutual_array is the array of mutual inductances
        new_array = raw_array
        for i in range(len(coil_array)):
            new_array = new_array - (coil_array[i] * mutual_array[i])
            
        return new_array                 


    def zero_beginning(self, array, if_coil=False):
        if if_coil:
            coil_ind2 = self.find_closest_index(self.time, self.time[0] + 0.001)
            value = np.mean(array[0:coil_ind2])
        else:
            value = np.mean(array[self.ind1:self.ind2])

        return (array - value)

        
    def dot(self, coil_array, mutual_array):
        new_array = coil_array[0] * mutual_array[0]
        for i in range(1, len(coil_array)):
            new_array = new_array + (coil_array[i] * mutual_array[i])            
            
        return new_array
    
        
    def find_closest_index(self, array, value):
        new_array = abs(array - value)
        try:
            index = new_array.argmin()
        except:
            print('Invalid Array')
            index = 0    
        return int(index)
    
    

"""
mag = MagneticAxisVerticalShift(20032705)
mag2= MagneticAxisVerticalShift(20032704)

plt.figure()
plt.plot(mag.time, mag.z,'k',label='20032705')
plt.plot(mag2.time, mag2.z,'r',label='20032704')
plt.legend()
plt.xlim([1.6, 1.7])
plt.ylim([-.1, .1])
plt.show()
#print(mag.BA_fit)
#plt.plot(mag.time, mag.BA_fit[0])
"""