# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 13:52:50 2020

@author: hartwgj
"""

from netCDF4 import Dataset
import numpy as np
import math

class results_file_contents:
    def __init__(self, file_name):
        data = Dataset(file_name, 'r')
        
        #print(data.variables.keys())

        self.nsteps = data.variables['nsteps'][:]
        self.g2 = data.variables['g2'][self.nsteps]
        
        #self.signal_observed_value = data.variables['signal_observed_value'][:]
        # self.signal_sigma = data.variables['signal_sigma'][:]
        # self.signal_model_value = data.variables['signal_model_value'][:]
        
        # self.signal_name = []
        # for name in data.variables['signal_name']:
        #     self.signal_name.append(''.join(np.char.decode(name)).split())

        # self.signal_type = []
        # for name in data.variables['signal_type'][:]:
        #     self.signal_type.append(''.join(np.char.decode(name)).strip())

        # self.signal_weight = data.variables['signal_weight'][:]

        self.ne_grid = data.variables['ne_grid'][:]
        self.ne_unit = data.variables['ne_unit'][:]
        # self.ne_min = data.variables['ne_min'][:]
        
            

        self.param_value = data.variables['param_value'][:][self.nsteps]
        self.param_sigma = data.variables['param_sigma'][:][self.nsteps]
        self.param_name  = self.decode_nc_string(data.variables['param_name'][:])
        self.param_index = data.variables['param_index'][:]

            # self.derived_param_value = data.variables['derived_param_value'][:]
            # self.derived_param_sigma = data.variables['derived_param_sigma'][:]
            # self.derived_param_index = data.variables['derived_param_index'][:]

        data.close()
        

    def decode_nc_string(self, nc_array):
        new_array = []
    
        for item in nc_array:
            item_array = []
            for sub_item in item:
                decoded_sub_item = sub_item.decode("utf-8")
                item_array.append(decoded_sub_item)
            
            new_item = ''.join(item_array)
            new_array.append(new_item.rstrip())
        
        return new_array


    def g2(self, signal_low, signal_high):
        g2 = 0.0
        for i in range(signal_low - 1, signal_high):
            e = math.sqrt(self.signal_weight[i])*((self.signal_observed_value[i] - self.signal_model_value[self.nsteps - 1, i, 0])/self.signal_sigma[self.nsteps - 1, i])
            g2 += e*e
        return g2
