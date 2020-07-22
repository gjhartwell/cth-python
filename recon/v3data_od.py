# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 08:47:03 2018

@author: James Kring
@email:  jdk0026@auburn.edu
"""

import numpy as np
import pandas as pd
from cthdata import CTHData
import matplotlib.pyplot as plt


class V3Data:
    def __init__(self, shot):
        self.data = {}
        self.shot = shot
        
        
    def find_closest_index(self, array, value):
        new_array = abs(array - value)
        try:
            index = new_array.argmin()
        except:
            print('Invalid Array')
            index = 0    
        return int(index)

    
    def raw_currents(self):
        # Get magnetic coil currents
        
        time = CTHData(self.shot, 119, channel_number=True).time
        self.ind2 = self.find_closest_index(time, time[0] + 0.001)
        
        #p_time_ind = self.find_closest_index(time, 1.61)        
        
        #self.ind2 = self.find_closest_index(time, time[p_time_ind]-0.001)
        
        
        def zero_beginning(array):
            value = np.mean(array[0:self.ind2])
            #value = np.mean(array[self.ind2:p_time_ind])
            return (array - value)
            #return array
        
        
        def rm_mut(raw_array, coil_array, mutual_array):
            #mutual_array is the array of mutual inductances
            new_array = raw_array
            for i in range(len(coil_array)):
                new_array = new_array - (coil_array[i] * mutual_array[i])
            
            return new_array                 
        
        

        oh_current = CTHData(self.shot, '\I_OH').data
        hf_ovf_current = CTHData(self.shot, '\I_HFOVF')
        tvf_current = CTHData(self.shot, 1, channel_number=True)
        svf_current = CTHData(self.shot, 2, channel_number=True)
        rf_ef_current1 = CTHData(self.shot, 4, channel_number=True)
        rf_ef_current2 = CTHData(self.shot, 7, channel_number=True)
        tf_current = CTHData(self.shot, 3, channel_number=True)

        hf_ovf_current = np.interp(time, hf_ovf_current.time, hf_ovf_current.data)
        tvf_current = np.interp(time, tvf_current.time, tvf_current.data)
        svf_current = zero_beginning(np.interp(time, svf_current.time, svf_current.data))
        rf_ef_current1 = np.interp(time, rf_ef_current1.time, rf_ef_current1.data)
        rf_ef_current2 = np.interp(time, rf_ef_current2.time, rf_ef_current2.data)
        rf_ef_current = rf_ef_current1 + rf_ef_current2
        
        tf_current = np.interp(time,tf_current.time, tf_current.data)        

        coil_currents = [hf_ovf_current, tvf_current, oh_current, svf_current,
                         rf_ef_current, tf_current]        

        vloop1 = zero_beginning(CTHData(self.shot, 108, channel_number=True).data)
        vloop2 = zero_beginning(CTHData(self.shot, 109, channel_number=True).data)
        vloop3 = zero_beginning(CTHData(self.shot, 110, channel_number=True).data)
        vloop4 = zero_beginning(CTHData(self.shot, 111, channel_number=True).data)
        
        vloop = (vloop1 + vloop2 + vloop3 + vloop4)
        
        PI264  = CTHData(self.shot, 171, channel_number=True).data 

        PI264  = rm_mut(PI264, coil_currents, [1.065E-1, 2.26E-1, 9.38E-4,
                                               2.76E-1, 1.789E-8, 5.475E-1])        
        PI264  = zero_beginning(PI264)        
        
        vv_current = ((vloop * 355.9) + (33.3 + (PI264 * 0.048446)))
        
        curtor =  (PI264 - (vv_current * 0.022))
        
        phiedge = ((-2.216E-5*tvf_current) + (3.264E-5*svf_current) + (-2.192E-7*curtor)) + -1.576E-2
        
        rbc = [((-4.807E-5*tvf_current) + (9.497E-5*svf_current) + (1.117E-6*curtor)) + 0.7338,
               ((0*tvf_current) + (-6.695E-5*svf_current) + (9.69E-7*curtor)) + 9.653E-2]
        
        zbs = [0*hf_ovf_current, 0.2 + 0 * hf_ovf_current]
        
        hcf40 = CTHData(self.shot, 40, channel_number=True).data
        hcf41 = CTHData(self.shot, 41, channel_number=True).data
        hcf36 = CTHData(self.shot, 36, channel_number=True).data
        hcf37 = CTHData(self.shot, 37, channel_number=True).data
        hcf38 = CTHData(self.shot, 38, channel_number=True).data
        hcf39 = CTHData(self.shot, 39, channel_number=True).data
        hcf32 = CTHData(self.shot, 32, channel_number=True).data
        hcf33 = CTHData(self.shot, 33, channel_number=True).data
        hcf34 = CTHData(self.shot, 34, channel_number=True).data
        hcf35 = CTHData(self.shot, 35, channel_number=True).data

        hcf40 = rm_mut(hcf40, coil_currents, [-0.08469, 1.23E-1, 1.67E-3,
                                              6.85E-4, -3.47E-3, 2.41E-1])
        hcf41 = rm_mut(hcf41, coil_currents, [0.05288, -1.23E-1, -6.19E-4,
                                              -8.15E-3, -2.62E-2,-6.31E-1])      
        hcf36 = rm_mut(hcf36, coil_currents, [-0.1435, -9.42E-2, 7.56E-4,
                                              9.26E-3, -1.88E-2, 1.80E-1]) 
        hcf37 = rm_mut(hcf37, coil_currents, [-0.07036, 9.27E-2, 2.52E-3,
                                              -1.32E-2, -2.31E-2, 1.77E-1])
        hcf38 = rm_mut(hcf38, coil_currents, [-0.03124, 1.13E-1, 1.34E-3,
                                              7.76E-3, 6.24E-3, 1.62E-1])         
        hcf39 = rm_mut(hcf39, coil_currents, [0.02473, -1.57E-1, 8.48E-4,
                                              -4.22E-3, -9.56E-3, -2.66E-1])
        hcf32 = rm_mut(hcf32, coil_currents, [0.1161, -6.08E-3, -3.16E-3,
                                              9.97E-3, 4.16E-3, -1.39E-1])
        hcf33 = rm_mut(hcf33, coil_currents, [-0.2028, -1.61E-1, 2.19E-3,
                                              -5.49E-4, -2.21E-2, 1.85E-1])
        hcf34 = rm_mut(hcf34, coil_currents, [-0.07523, -8.99E-2, 2.11E-3,
                                              -8.77E-3, 2.74E-2, 2.57E-2])
        hcf35 = rm_mut(hcf35, coil_currents, [0.1193, 6.58E-2, 3.25E-3,
                                              2.29E-3, -1.05E-2, -2.17E-1])
        
        hcf_current = np.mean([hcf40, hcf41, hcf36, hcf37, hcf38, hcf39, hcf32,
                               hcf33, hcf34, hcf35], axis=0)

        currents = [curtor, hf_ovf_current, tvf_current, oh_current, svf_current,
                    rf_ef_current, tf_current, vv_current, hcf_current,
                    phiedge, rbc[0], rbc[1], zbs[0], zbs[1]]
        

        self.currents = [ hf_ovf_current, tvf_current, oh_current, svf_current,
                             rf_ef_current, tf_current, vv_current, hcf_current, curtor]
        
        return currents, time
        
        
    def raw_magnetics(self):
        # Function to grab the magnetic diagnostic signals and correct for
        # mutual inductances.
        #
        # From Mark:
        # Each diagnostic signal is corrected by the following method.
        #
        # Define some terms:
        #   M_e : Experimentally measured mutual inductance values. Vector Quanity
        #   M_m : Modeled mutual inductance values. Vector Quanity
        #
        #   t   : Reconstruction time.
        #   t_a : Time before the OH fires. It is assumed at this time there is no plasma current.
        #       : t_a is set to 1.61 in this python script - 5/2/19 James Kring
        #
        #   a   : Conversion factor to tesla for M_e.
        #
        #   I   : Vector of coil currents.
        #
        #   S_0 : Raw signal read from the tree.
        #   S_1 : Corrected signal.
        #
        # Math Symbols:
        #   * : MULIPLY
        #   . : DOT_PRODUCT
        #   / : DIVIDE
        #
        # Raw Signals are corrected by.
        #
        # S_1(t) = a(S_0(t)/100 - I(t).M_e(t) - S(t_a)/100 + I(t_a).M_e(t_a) + I(t).M_m(t))
        #
        # The following correction are performed by correcting the experimental mutual inductance
        # over the entire shot. The residuale before the OH fires is then removed by ZERO_BEGINNING.
        # The the modeled multual inductance is added.



        time = CTHData(self.shot, 171, channel_number=True).time  
        self.ind2 = self.find_closest_index(time, time[0] + 0.001)
        
        p_time_ind = self.find_closest_index(time, 1.61)        
        
        self.ind1 = self.find_closest_index(time, time[p_time_ind]-0.0005)
        self.ind2 = self.find_closest_index(time, time[p_time_ind]+0.0005)        
        
        
        
        def zero_beginning(array):
            value = np.mean(array[self.ind1:self.ind2])
            return (array - value)


        def rm_mut(raw_array, coil_array, mutual_array):
            #mutual_array is the array of mutual inductances
            
            array1 = np.zeros(len(raw_array))
            
        
            for i in range(len(coil_array)):
                array1 = array1 + (coil_array[i] * mutual_array[i])
            
            new_array = raw_array - array1 + array1[p_time_ind]
            
            return new_array
        
        
        def dot(coil_array, mutual_array):
            new_array = coil_array[0] * mutual_array[0]
            for i in range(1, len(coil_array)):
                new_array = new_array + (coil_array[i] * mutual_array[i])            
            
            return new_array
        

        currents = self.currents[0:7]
        curtor = self.currents[8]
        
       
        PI096A = CTHData(self.shot, 180, channel_number=True).data
        PI096A = zero_beginning(rm_mut(PI096A/100, 
                                       currents, 
                                       [6.13E-7, 1.45E-6, 1.91E-9,
                                        -1.54E-7, 2.37E-7, 1.17E-7,
                                        0, 0]))
        PI096A = 35.501*(PI096A + dot(currents, [6.69E-7, 1.41E-6, 2.41E-9,
                                                 -1.49E-7, 4.42E-7, 5.93E-10,
                                                 -2.68E-9, -9.94E-8]))

        PI096B = CTHData(self.shot, 181, channel_number=True).data
        PI096B = zero_beginning(rm_mut(PI096B/100, 
                                       currents, 
                                       [5.06E-7, 1.43E-6, 9.16E-10,
                                        -7.49E-8, 1.16E-7, 6.38E-8,
                                        0, 0]))
        PI096B = 33.820*(PI096B + dot(currents, [5.25E-7, 1.47E-6, 1.23E-9,
                                                 -7.43E-8, 2.38E-7, 8.58E-8,
                                                 -3.75E-9, -1.57E-8]))
        
        PI096C = CTHData(self.shot, 182, channel_number=True).data
        PI096C = zero_beginning(rm_mut(PI096C/100, 
                                       currents, 
                                       [3.95E-7, 1.38E-6, 1.11E-10,
                                        -6.19E-8, -3.67E-8, -8.34E-8,
                                        0, 0]))
        PI096C = 33.952*(PI096C + dot(currents, [3.99E-7, 1.43E-6, 5.40E-10,
                                                 -5.97E-8, -8.30E-8, -7.02E-8,
                                                 -6.22E-9, -9.45E-9]))

        PI096D = CTHData(self.shot, 183, channel_number=True).data
        PI096D = zero_beginning(rm_mut(PI096D/100, 
                                       currents, 
                                       [-9.55E-8, 1.43E-6, 6.71E-10,
                                        -9.22E-8, -1.77E-7, 1.74E-7,
                                        0, 0]))
        PI096D = 36.725*(PI096D + dot(currents, [-9.66E-8, 1.39E-6, 1.92E-9,
                                                 -9.53E-8, -3.33E-7, 1.25E-7,
                                                 -2.37E-9, -3.58E-8]))      
        
        PI096E = CTHData(self.shot, 184, channel_number=True).data
        PI096E = zero_beginning(rm_mut(PI096E/100, 
                                       currents, 
                                       [-4.70E-7, 1.25E-6, 2.22E-10,
                                        -2.18E-7, -2.48E-7, -2.90E-7,
                                        0, 0]))
        PI096E = 36.452*(PI096E + dot(currents, [-5.01E-7, 1.22E-6, 1.58E-9,
                                                 -2.15E-7, -4.71E-7, -4.47E-8,
                                                 -3.63E-9, -8.83E-8]))           
        
        PI096F = CTHData(self.shot, 185, channel_number=True).data
        PI096F = zero_beginning(rm_mut(PI096F/100, 
                                       currents, 
                                       [-1.98E-6, 5.49E-7, -5.36E-9,
                                        -5.16E-7, -2.14E-7, 1.85E-7,
                                        0, 0]))
        PI096F = 34.257*(PI096F + dot(currents, [-1.91E-6, 5.31E-7, -2.95E-9,
                                                 -5.15E-7, -4.20E-7, 1.06E-7,
                                                 -2.88E-9, -1.87E-9]))     

        PI096G = CTHData(self.shot, 186, channel_number=True).data
        PI096G = zero_beginning(rm_mut(PI096G/100, 
                                       currents, 
                                       [-1.95E-6, -3.33E-7, -8.55E-9, 
                                        -7.77E-7, -1.12E-7, 4.63E-7,
                                        0, 0]))
        PI096G = 34.538*(PI096G + dot(currents, [-1.84E-6, -3.27E-7, -4.62E-9,
                                                 -7.73E-7, -2.31E-7, 3.67E-7,
                                                 -3.39E-9, 1.31E-8]))             
        
        PI096H = CTHData(self.shot, 187, channel_number=True).data
        PI096H = zero_beginning(rm_mut(PI096H/100, 
                                       currents, 
                                       [-1.66E-7, -1.07E-6, -4.83E-9, 
                                        -4.01E-7, -4.29E-8, -3.84E-9,
                                        0, 0]))
        PI096H = 34.041*(PI096H + dot(currents, [-1.67E-7, -1.10E-6, -2.15E-9,
                                                 -3.74E-7, -8.35E-8, -1.04E-7,
                                                 3.05E-9, 5.27E-8]))    

        PI096I = CTHData(self.shot, 188, channel_number=True).data
        PI096I = zero_beginning(rm_mut(PI096I/100, 
                                       currents, 
                                       [1.01E-6, -1.46E-6, 1.98E-9, 
                                        6.27E-7, -8.80E-9, -7.16E-8,
                                        0, 0]))
        PI096I = 35.513*(PI096I + dot(currents, [9.13E-7, -1.44E-6, 1.33E-9,
                                                 6.51E-7, -1.03E-8, 4.29E-8,
                                                 7.44E-9, 5.92E-8]))    

        PI096J = CTHData(self.shot, 189, channel_number=True).data
        PI096J = zero_beginning(rm_mut(PI096J/100, 
                                       currents, 
                                       [1.47E-6, -1.41E-6, 9.34E-9,
                                        1.40E-6, 5.21E-9, -1.83E-7,
                                        0, 0]))
        PI096J = 34.769*(PI096J + dot(currents, [1.28E-6, -1.41E-6, 4.41E-9,
                                                 1.39E-6, -6.12E-9, 4.79E-8,
                                                 6.33E-9, 8.89E-9])) 

        PI096K = CTHData(self.shot, 190, channel_number=True).data
        PI096K = zero_beginning(rm_mut(PI096K/100, 
                                       currents, 
                                       [2.14E-7, -1.40E-6, 1.06E-8,
                                        1.37E-6, -4.45E-9, -3.01E-7,
                                        0, 0]))
        PI096K = 34.455*(PI096K + dot(currents, [2.41E-7, -1.39E-6, 4.36E-9,
                                                 1.38E-6, -1.74E-9, -9.37E-8,
                                                 7.94E-9, 8.81E-9])) 
        ind1 = self.find_closest_index(time, 1.61)
        PI096K = PI096K - np.mean(PI096K[ind1-10:ind1+10])
        
        PI096L = CTHData(self.shot, 191, channel_number=True).data
        PI096L = zero_beginning(rm_mut(PI096L/100, 
                                       currents, 
                                       [-2.38E-7, -1.50E-6, 4.52E-9,
                                        6.93E-7, 1.74E-9, -3.19E-7,
                                        0, 0]))
        PI096L = 34.567*(PI096L + dot(currents, [-5.91E-7, -1.51E-6, 1.47E-9,
                                                 7.02E-7, -9.47E-10,-4.94E-9,
                                                 7.43E-9, 7.06E-8])) 
        
        PI096M = CTHData(self.shot, 192, channel_number=True).data
        PI096M = zero_beginning(rm_mut(PI096M/100, 
                                       currents, 
                                       [-5.72E-7, -1.11E-6, -1.97E-9,
                                        -3.67E-7, 3.52E-8, 9.58E-9,
                                        0, 0]))
        PI096M = 35.297*(PI096M + dot(currents, [-5.72E-7, -1.10E-6, -2.02E-9,
                                                 -3.68E-7, 6.56E-8, -5.24E-8,
                                                 3.88E-9, 5.44E-8])) 
        
        PI096O = CTHData(self.shot, 194, channel_number=True).data
        PI096O = zero_beginning(rm_mut(PI096O/100, 
                                       currents, 
                                       [6.08E-7, 5.46E-7, -3.96E-9,
                                        -5.13E-7, 2.06E-7, 8.47E-8,
                                        0, 0]))
        PI096O = 35.784*(PI096O + dot(currents, [6.85E-7, 5.43E-7, -3.05E-9,
                                                 -5.14E-7, 4.04E-7, -1.29E-7,
                                                 -2.36E-9, -5.10E-9]))  
        #65.581?
        PI096P = CTHData(self.shot, 195, channel_number=True).data
        PI096P = zero_beginning(rm_mut(PI096P/100, 
                                       currents, 
                                       [5.65E-7, 5.58E-7, 5.73E-10,
                                        -1.51E-7, 1.27E-7, -4.09E-7,
                                        0, 0]))
        PI096P = 35.581*(PI096P + dot(currents, [4.04E-7, 5.85E-7, 2.92E-10,   
                                                 -1.54E-7, 2.67E-7, -3.50E-8,
                                                 -2.36E-9, -2.02E-8]))  

        PI096P = CTHData(self.shot, 195, channel_number=True).data
        PI096P = zero_beginning(rm_mut(PI096P/100, 
                                       currents, 
                                       [5.65E-7, 5.58E-7, 5.73E-10,
                                        -1.51E-7, 1.27E-7, -4.09E-7,
                                        0, 0]))
        PI096P = 65.581*(PI096P + dot(currents, [4.04E-7, 5.85E-7, 2.92E-10,
                                                 -1.54E-7, 2.67E-7, -3.50E-8,
                                                 -2.36E-9, -2.02E-8]))          
        
        # 14 part inner rogowski at phi=324
        PI32A  = CTHData(self.shot, 51, channel_number=True).data
        PI32A  = zero_beginning(rm_mut(PI32A/100, 
                                       currents, 
                                       [5.88E-7, 1.51E-6, 3.98E-9,
                                        -1.05E-7, 1.72E-7, -2.045E-8,
                                        0, 0]))
        PI32A  = 33.330*(PI32A + dot(currents, [5.64E-7, 1.51E-6, 1.93E-9,
                                                 -1.02E-7, 3.40E-7, 3.20E-8,
                                                 -3.37E-9, -3.75E-8]))          
        
        PI32B  = CTHData(self.shot, 52, channel_number=True).data
        PI32B  = zero_beginning(rm_mut(PI32B/100, 
                                       currents, 
                                       [5.58E-7, 1.38E-6, 4.18E-9,
                                        -2.28E-7, 2.59E-7, -7.08E-8,
                                        0, 0]))
        PI32B  = 33.815*(PI32B + dot(currents, [5.54E-7, 1.40E-6, 1.86E-9,
                                                -2.25E-7, 4.99E-7, -2.58E-8,
                                                -4.20E-9, -9.60E-8]))            
        PI32C  = CTHData(self.shot, 53, channel_number=True).data
        PI32C  = zero_beginning(rm_mut(PI32C/100, 
                                       currents, 
                                       [-4.16E-8, 5.56E-7, -1.09E-9,
                                        -5.08E-7, 2.12E-7, -3.96E-8,
                                        0, 0]))
        PI32C  = 35.428*(PI32C + dot(currents, [-4.43E-8, 5.48E-7, -2.96E-9,
                                                -5.07E-7, 4.10E-7, -6.61E-8,
                                                -2.46E-9, -5.55E-9]))   
        
        PI32D  = CTHData(self.shot, 54, channel_number=True).data
        PI32D  = zero_beginning(rm_mut(PI32D/100, 
                                       currents, 
                                       [-2.39E-7, -4.21E-8, -1.75E-9,  #-2.39E-7, -4.21E-8, -1.75E-9, ???
                                        -3.11E-8, 7.37E-9, 6.17E-10,
                                        0, 0]))
        PI32D  = 35.078*(PI32D + dot(currents, [-1.06E-6, -2.97E-7, -4.78E-9,
                                                -8.04E-7, 2.29E-7, 2.36E-10,
                                                -4.46E-9, 8.58E-9]))
        PI32D  = PI32D
        #PI32D = PI32D - PI32D[-1]
        
        PI32E  = CTHData(self.shot, 55, channel_number=True).data
        PI32E  = zero_beginning(rm_mut(PI32E/100, 
                                       currents, 
                                       [-1.25E-6, -1.10E-6, -1.56E-9,
                                        -3.98E-7, 3.46E-8, 1.11E-7,
                                        0, 0]))
        PI32E  = 34.091*(PI32E + dot(currents, [-1.29E-6, -1.12E-6, -2.19E-9,
                                                -3.97E-7, 7.40E-8, 1.23E-7,
                                                3.82E-9, 5.41E-8]))    
        #PI32E = PI32E - PI32E[-1]
        
        PI32F  = CTHData(self.shot, 56, channel_number=True).data
        PI32F  = zero_beginning(rm_mut(PI32F/100, 
                                       currents, 
                                       [-1.26E-7, -1.52E-6, 4.21E-10,
                                        7.00E-7, -2.48E-9, -4.96E-9,
                                        0, 0]))
        PI32F  = 34.399*(PI32F + dot(currents, [-1.34E-7, -1.52E-6, 1.41E-9,
                                                6.86E-7, -5.87E-10, 1.12E-8,
                                                7.21E-9, 7.42E-87]))    
        #PI32F = PI32F - PI32F[-1]

        PI32G  = CTHData(self.shot, 57, channel_number=True).data
        PI32G  = zero_beginning(rm_mut(PI32G/100, 
                                       currents, 
                                       [9.89E-7, -1.44E-6, -2.51E-9,
                                        1.43E-6, 3.57E-9, 5.86E-8,
                                        0, 0]))
        PI32G  = 34.571*(PI32G + dot(currents, [1.00E-6, -1.43E-6, 4.49E-9, 
                                                1.42E-6, 1.91E-10, 1.11E-8,
                                                5.97E-9, 1.16E-8]))     
        
        PI32H  = CTHData(self.shot, 58, channel_number=True).data
        PI32H  = zero_beginning(rm_mut(PI32H/100, 
                                       currents, 
                                       [7.84E-7, -1.43E-6, -1.36E-9,
                                        1.39E-6, -6.53E-9, 1.49E-7,
                                        0, 0]))
        PI32H  = 35.045*(PI32H + dot(currents, [9.18E-7, -1.41E-6, 4.17E-9,
                                                1.34E-6, -5.77E-9, -7.59E-8,
                                                8.10E-9, 1.32E-8]))
        
        PI32I  = CTHData(self.shot, 59, channel_number=True).data
        PI32I  = zero_beginning(rm_mut(PI32I/100, 
                                       currents, 
                                       [-6.58E-8, -1.49E-6, 1.05E-9,
                                        6.19E-7, -5.57E-9, -1.58E-7,
                                        0, 0]))
        PI32I  = 35.404*(PI32I + dot(currents, [-7.00E-8, -1.46E-6, 1.30E-9,
                                                6.43E-7, -6.68E-9, -2.95E-8,
                                                7.12E-9, 6.91E-8]))

        PI32J  = CTHData(self.shot, 60, channel_number=True).data
        PI32J  = zero_beginning(rm_mut(PI32J/100, 
                                       currents, 
                                       [-9.63E-7, -1.05E-6, -1.83E-9,
                                        -4.39E-7, -4.13E-8, -1.33E-7,
                                        0, 0]))
        PI32J  = 34.929*(PI32J + dot(currents, [-1.2E-6, -1.04E-6, -2.36E-9,
                                                -4.30E-7, -8.57E-8, 8.29E-8,
                                                2.89E-9, 4.59E-8])) 
        
        PI32K  = CTHData(self.shot, 61, channel_number=True).data
        PI32K  = zero_beginning(rm_mut(PI32K/100, 
                                       currents, 
                                       [-1.06E-6, -2.62E-7, -4.35E-9,
                                        -7.72E-7, -1.21E-7, 4.42E-8,
                                        0, 0]))
        PI32K  = 34.584*(PI32K + dot(currents, [-1.09E-6, -2.54E-7, -4.80E-9,
                                                -7.90E-7, -2.45E-7, 2.72E-8,
                                                -4.12E-9, 8.53E-9]))

        PI32L  = CTHData(self.shot, 62, channel_number=True).data
        PI32L  = zero_beginning(rm_mut(PI32L/100, 
                                       currents, 
                                       [-9.20E-8, 6.49E-7, -1.66E-9,
                                        -4.84E-7, -2.22E-7, 1.06E-7,
                                        0, 0]))
        PI32L  = 34.781*(PI32L + dot(currents, [-9.71E-8, 6.30E-7, -2.50E-9,
                                                -4.80E-7, -4.30E-7, 7.53E-8,
                                                -3.20E-9, -8.84E-9]))

        PI32M  = CTHData(self.shot, 63, channel_number=True).data
        PI32M  = zero_beginning(rm_mut(PI32M/100, 
                                       currents, 
                                       [5.02E-7, 1.37E-6, 3.31E-9,
                                        -1.97E-7, -2.24E-7, -4.58E-9,
                                        0, 0]))
        PI32M  = 34.545*(PI32M + dot(currents, [4.96E-7, 1.36E-6, 1.91E-9,
                                                -2.09E-7, -4.83E-7, 2.85E-8,
                                                -3.24E-9, -9.68E-8]))

        PI32N  = CTHData(self.shot, 64, channel_number=True).data
        PI32N  = zero_beginning(rm_mut(PI32N/100, 
                                       currents, 
                                       [5.24E-7, 1.48E-6, 3.25E-9,
                                        -9.52E-8, -1.55E-7, 6.67E-8,
                                        0, 0]))
        PI32N  = 35.371*(PI32N + dot(currents, [5.51E-7, 1.43E-6, 1.89E-9,
                                                -9.48E-8, -3.35E-7, -1.44E-8,
                                                -3.03E-9, -3.47E-8]))      
        
        
        #8 part inner rogowski at phi=264
        PI264A = CTHData(self.shot, 172, channel_number=True).data
        PI264A = zero_beginning(rm_mut(PI264A/100, 
                                       currents, 
                                       [1.03E-6, 3.35E-6, 4.54E-9,
                                        -1.83E-7, 5.13E-7, 1.43E-7,
                                        -9.11E-9, -7.69E-8]))
        PI264A = ((18.23047578331*PI264A) + dot(currents, 
                                                [1.97E-5, 6.00E-5, 4.58E-8,
                                                 -2.92E-6, -7.95E-6, -8.21E-7,
                                                 -1.50E-7, -9.30E-7])) 

        PI264B = CTHData(self.shot, 173, channel_number=True).data
        PI264B = zero_beginning(rm_mut(PI264B/100, 
                                       currents, 
                                       [1.44E-6, 2.01E-6, -9.50E-10,
                                        -7.94E-7, 8.74E-7, -2.95E-7,
                                        -6.76E-9, -1.96E-8]))
        PI264B = ((17.73754900137*PI264B) + dot(currents, 
                                                [2.43E-5, 3.63E-5, -3.98E-8,
                                                 -1.42E-5, -1.56E-5, -1.60E-6,
                                                 -1.19E-7, -1.32E-6])) 

        PI264C = CTHData(self.shot, 174, channel_number=True).data
        PI264C = zero_beginning(rm_mut(PI264C/100, 
                                       currents, 
                                       [-7.11E-8, -1.73E-6, -6.46E-9,
                                        -1.13E-6, 2.93E-7, -2.95E-7,
                                        -2.70E-9, 6.45E-8]))
        PI264C = ((17.12559737082*PI264C) + dot(currents, 
                                                [-2.23E-6, -2.90E-5, -1.19E-7,
                                                 -2.04E-5, -5.24E-6, -3.00E-6,
                                                 -1.02E-8, 1.07E-6]))  
        
        PI264D = CTHData(self.shot, 175, channel_number=True).data
        PI264D = zero_beginning(rm_mut(PI264D/100, 
                                       currents, 
                                       [-5.70E-7, -3.52E-6, -7.48E-10,
                                        2.00E-6, 2.36E-8, 1.88E-7,
                                        2.41E-8, 4.10E-8]))
        PI264D = ((17.36547453381*PI264D) + dot(currents, 
                                                [-9.49E-6, -6.25E-5, 8.65E-8,
                                                 3.26E-5, -4.33E-8, 1.75E-7,
                                                 2.58E-7, 1.61E-6])) 
        
        PI264E = CTHData(self.shot, 176, channel_number=True).data
        PI264E = zero_beginning(rm_mut(PI264E/100, 
                                       currents, 
                                       [2.21E-6, -3.59E-6, 6.32E-10,
                                        2.26E-6, 2.54E-8, 1.09E-8,
                                        2.13E-8, 5.39E-8]))
        PI264E = ((17.87703198128*PI264E) + dot(currents, 
                                                [4.17E-5, -6.33E-5, 1.10E-7,
                                                 3.87E-5, -2.82E-7, -9.58E-7,
                                                 2.71E-7, 1.07E-6])) 

        PI264F = CTHData(self.shot, 177, channel_number=True).data
        PI264F = zero_beginning(rm_mut(PI264F/100, 
                                       currents, 
                                       [-1.31E-6, -2.02E-6, -3.53E-9,
                                        -1.06E-6, -2.33E-7, 6.60E-8,
                                        3.34E-10, 7.28E-8]))
        PI264F = ((17.56927307609*PI264F) + dot(currents, 
                                                [-2.23E-5, 3.53E-5, -1.02E-7,
                                                 -1.74E-5, 4.13E-6, 2.11E-6,
                                                 3.84E-8, 1.54E-6])) 

        PI264G = CTHData(self.shot, 178, channel_number=True).data
        PI264G = zero_beginning(rm_mut(PI264G/100, 
                                       currents, 
                                       [-2.77E-6, 2.02E-6, 2.57E-9,
                                        -8.25E-7, -8.90E-7, 6.61E-8,
                                        -8.62E-9, -4.42E-8]))
        PI264G = ((17.94110594901*PI264G) + dot(currents, 
                                                [-5.12E-5, 3.57E-5, -4.21E-8,
                                                 -1.43E-5, 1.56E-5, 2.95E-6,
                                                 -1.21E-7, -1.26E-6]))   
        
        PI264H = CTHData(self.shot, 179, channel_number=True).data
        PI264H = zero_beginning(rm_mut(PI264H/100, 
                                       currents, 
                                       [2.57E-7, 3.50E-6, 6.24E-9,
                                        -1.86E-7, -5.94E-7, 3.29E-8,
                                        -1.03E-8, -9.84E-8]))
        PI264H = ((17.30035813767*PI264H) + dot(currents, 
                                                [3.66E-6, 6.03E-5, 5.51E-8,
                                                 -3.25E-6, 9.70E-6, 6.62E-7,
                                                 -1.31E-7, -1.41E-6]))     
        
        
        full_rog_signal = 7.168247365207E-7 * curtor
        
        #8 part addle coils
        bottom_A = CTHData(self.shot, 100, channel_number=True).data
        bottom_A = zero_beginning(rm_mut(bottom_A/400, 
                                         currents, 
                                         [-2.02E-6, 1.54E-6, 5.64E-9,
                                          1.13E-7, 3.90E-8, -2.55E-8,
                                          0, 0]))
        bottom_A = (bottom_A + dot(currents, 
                                   [-2.01E-6, 1.52E-6, 4.11E-9,
                                    1.14E-7, 7.55E-8, -1.83E-8,
                                    -1.93E-9, 2.03E-8]))           

        bottom_B = CTHData(self.shot, 101, channel_number=True).data
        bottom_B = zero_beginning(rm_mut(bottom_B/300, 
                                         currents, 
                                         [-1.77E-6, 1.75E-6, 4.99E-9,
                                          -1.66E-8, 1.27E-7, -1.78E-8,
                                          0, 0]))
        bottom_B = (bottom_B + dot(currents, 
                                   [-1.75E-6, 1.73E-6, 2.48E-9,
                                    -2.39E-8, 2.52E-7, -1.02E-8,
                                    -3.10E-9, 2.82E-8]))  

        bottom_C = CTHData(self.shot, 102, channel_number=True).data
        bottom_C = zero_beginning(rm_mut(bottom_C/300, 
                                         currents, 
                                         [-1.30E-6, 1.62E-6, 1.94E-9,
                                          -2.92E-7, 1.39E-7, -9.90E-9,
                                          0, 0]))
        bottom_C = (bottom_C + dot(currents, 
                                   [-1.28E-6, 1.59E-6, -5.50E-10,
                                    -2.96E-7, 2.67E-7, -2.68E-8,
                                    -4.98E-9, 2.72E-8]))  

        bottom_D = CTHData(self.shot, 103, channel_number=True).data
        bottom_D = zero_beginning(rm_mut(bottom_D/300, 
                                         currents, 
                                         [-6.94E-7, 1.28E-6, -3.77E-10,
                                          -7.87E-7, 1.32E-7, 4.14E-9,
                                          0, 0]))
        bottom_D = (bottom_D + dot(currents, 
                                   [-6.95E-7, 1.27E-6, -2.96E-9,
                                    -7.89E-7, 2.51E-7, 1.69E-10,
                                    -7.48E-9, 2.39E-8]))  

        top_A = CTHData(self.shot, 104, channel_number=True).data
        top_A = zero_beginning(rm_mut(top_A/300, 
                                      currents, 
                                      [-1.70E-6, 1.69E-6, 4.17E-9,
                                       -4.95E-8, -1.21E-7, -5.87E-9,
                                       0, 0]))
        top_A = (top_A + dot(currents, 
                             [-1.69E-6, 1.67E-6, 1.89E-9,
                              -5.75E-8, -2.45E-7, -2.21E-9,
                              -4.51E-9, 2.87E-8]))    
        
        top_B = CTHData(self.shot, 105, channel_number=True).data
        top_B = zero_beginning(rm_mut(top_B/300, 
                                      currents, 
                                      [-1.42E-6, 1.75E-6, 9.30E-10,
                                       -4.48E-7, -1.55E-7, 8.03E-9,
                                       0, 0]))
        top_B = (top_B + dot(currents, 
                             [-1.40E-6, 1.72E-6, -1.44E-9,
                              -4.70E-7, -3.04E-7, 4.27E-8,
                              -7.67E-9, 2.94E-8]))    
        
        top_C = CTHData(self.shot, 106, channel_number=True).data
        top_C = zero_beginning(rm_mut(top_C/300, 
                                      currents, 
                                      [-7.39E-7, 1.36E-6, -1.29E-9,
                                       -9.60E-7, -1.36E-7, 2.27E-8,
                                       0, 0]))
        top_C = (top_C + dot(currents, 
                             [-7.52E-7, 1.34E-6, -3.41E-9,
                              -9.56E-7, -2.65E-7, 6.67E-8,
                              -7.92E-9, 2.10E-8]))    

        top_D = CTHData(self.shot, 107, channel_number=True).data
        top_D = zero_beginning(rm_mut(top_D/300, 
                                      currents, 
                                      [-1.26E-7, 8.86E-7, -8.49E-10,
                                       -1.13E-6, -1.04E-7, 3.39E-8,
                                       0, 0]))
        top_D = (top_D + dot(currents, 
                             [-1.30E-7, 8.70E-7, -3.72E-9,
                              -1.12E-6, -2.08E-7, 4.10E-8,
                              -6.25E-9, 1.33E-8]))  
    
        # Cube Coils
        cube_AA = CTHData(self.shot, 88, channel_number=True).data
        cube_AA = zero_beginning(rm_mut(cube_AA/100, 
                                        currents, 
                                        [-7.74E-7, -9.06E-7, -2.23E-9,
                                         -4.46E-8, -3.61E-8, 5.58E-8,
                                         0, 0]))
        cube_AA = ((64.83288*cube_AA) + dot(currents, 
                                            [-4.95E-5, -5.96E-5, -1.31E-7,
                                             -2.56E-6, -5.34E-6, 1.04E-6,
                                             1.05E-9, 2.63E-6]))   
        
        cube_AB = CTHData(self.shot, 89, channel_number=True).data
        cube_AB = zero_beginning(rm_mut(cube_AB/100, 
                                        currents, 
                                        [4.40E-8, 3.48E-7, -1.15E-9,
                                         -1.89E-7, -9.39E-8, 1.84E-8,
                                         0, 0]))
        cube_AB = ((79.91466*cube_AB) + dot(currents, 
                                            [3.27E-6, 2.78E-5, -6.49E-8,
                                             -1.52E-5, 1.58E-5, 1.13E-7,
                                             -9.35E-8, -5.25E-7]))

        cube_BA = CTHData(self.shot, 90, channel_number=True).data
        cube_BA = zero_beginning(rm_mut(cube_BA/100, 
                                        currents, 
                                        [-4.23E-7, -7.90E-9, -3.40E-9,
                                         -4.14E-7, 8.44E-8, 1.43E-9,
                                         0, 0]))
        cube_BA = ((61.353432*cube_BA) + dot(currents, 
                                            [-2.61E-5, -3.39E-7, -1.66E-7,
                                             -2.51E-5, 1.04E-5, -1.01E-8,
                                             -2.95E-7, 1.74E-7]))     

        cube_BB = CTHData(self.shot, 91, channel_number=True).data
        cube_BB = zero_beginning(rm_mut(cube_BB/100, 
                                        currents, 
                                        [1.01E-6, 1.16E-6, -4.84E-10,
                                         -1.47E-7, 9.50E-8, -5.44E-8,
                                         0, 0]))
        cube_BB = ((53.94396*cube_BB) + dot(currents, 
                                            [5.29E-5, 6.47E-5, 2.97E-8,
                                             -6.12E-6, 9.60E-6, 6.06E-7,
                                             -1.39E-7, -2.29E-6]))   
        
        cube_CA = CTHData(self.shot, 92, channel_number=True).data
        cube_CA = zero_beginning(rm_mut(cube_CA/100, 
                                        currents, 
                                        [-3.15E-7, -8.98E-7, 3.25E-9,
                                         4.79E-7, -8.86E-8, 6.15E-8,
                                         0, 0]))
        cube_CA = ((66.58512*cube_CA) + dot(currents, 
                                            [-2.09E-5, -5.95E-5, 1.11E-7,
                                             3.10E-5, -1.11E-5, 8.84E-7,
                                             3.87E-7, 2.48E-6])) 
        
        cube_CB = CTHData(self.shot, 93, channel_number=True).data
        cube_CB = zero_beginning(rm_mut(cube_CB/100, 
                                        currents, 
                                        [-6.66E-7, -3.40E-7, -2.49E-9,
                                         -3.93E-7, 4.06E-8, -6.41E-9,
                                         0, 0]))
        cube_CB = ((65.940546*cube_CB) + dot(currents, 
                                            [-4.39E-5, -2.25E-5, -1.32E-7,
                                             -2.60E-5, 5.62E-6, 1.29E-6,
                                             2.29E-8, 5.65E-7]))  
        
        cube_DA = CTHData(self.shot, 94, channel_number=True).data
        cube_DA = zero_beginning(rm_mut(cube_DA/100, 
                                        currents, 
                                        [1.45E-7, 9.53E-7, -4.25E-9,
                                         -5.43E-7, -8.65E-8, 7.49E-8,
                                         0, 0]))
        cube_DA = ((62.58000*cube_DA) + dot(currents, 
                                            [9.18E-6, 5.92E-5, -1.08E-7,
                                             -3.12E-5, -1.08E-5, -6.29E-8,
                                             -3.34E-7, -2.51E-6]))  
        
        cube_DB = CTHData(self.shot, 95, channel_number=True).data
        cube_DB = zero_beginning(rm_mut(cube_DB/100, 
                                        currents, 
                                        [-6.65E-7, -4.23E-7, -4.15E-9, 
                                         -3.91E-7, -3.86E-8, -4.36E-8,
                                         0, 0]))
        cube_DB = ((60.17067*cube_DB) + dot(currents, 
                                            [-4.06E-5, -2.54E-5, -1.23E-7,
                                             -2.33E-5, -5.19E-6, -1.16E-7,
                                             1.85E-8, 7.40E-7]))  
        
        cube_EA = CTHData(self.shot, 96, channel_number=True).data
        cube_EA = zero_beginning(rm_mut(cube_EA/100, 
                                        currents, 
                                        [7.61E-7, 9.99E-7, -7.93E-11, 
                                         -1.16E-7, -7.71E-8, 5.38E-8,
                                         0, 0]))
        cube_EA = ((64.51998*cube_EA) + dot(currents, 
                                            [4.92E-5, 6.46E-5, 2.01E-8,
                                             -7.90E-6, -9.81E-6, -1.12E-6,
                                             -1.94E-7, -2.31E-6]))  

        cube_EB = CTHData(self.shot, 97, channel_number=True).data
        cube_EB = zero_beginning(rm_mut(cube_EB/100, 
                                        currents, 
                                        [-4.57E-7, -2.38E-8, -4.70E-9, 
                                         -4.03E-7, -8.24E-8, 6.81E-8,
                                         0, 0]))
        cube_EB = ((61.353432*cube_EB) + dot(currents, 
                                            [-2.81E-5, -1.45E-6, -1.62E-7,
                                             -2.43E-5, -1.03E-5, 6.25E-7,
                                             -2.24E-7, 2.30E-7]))  
        
        cube_FA = CTHData(self.shot, 98, channel_number=True).data
        cube_FA = zero_beginning(rm_mut(cube_FA/100, 
                                        currents, 
                                        [7.05E-7, 8.95E-7, 2.36E-9,
                                         4.38E-8, -4.35E-8, 6.78E-9,
                                         0, 0]))
        cube_FA = ((65.52126*cube_FA) + dot(currents, 
                                            [4.60E-5, 5.91E-5, 1.31E-7,
                                             2.44E-6, -5.02E-6, -3.28E-7,
                                             -3.64E-8, -2.66E-6]))
        
        cube_FB = CTHData(self.shot, 99, channel_number=True).data
        cube_FB = zero_beginning(rm_mut(cube_FB/100, 
                                        currents, 
                                        [-2.16E-8, 3.64E-7, -2.36E-9,
                                         -2.30E-7, -1.18E-7, 6.76E-8,
                                         0, 0]))
        cube_FB = ((65.871708*cube_FB) + dot(currents, 
                                            [-1.42E-6, 2.40E-5, -7.00E-8,
                                             -1.52E-5, -1.55E-5, 7.25E-7,
                                             -9.17E-8, -3.88E-7])) 
        
        magnetic_diagnostic = [PI096A, PI096B, PI096C, PI096D, PI096E, PI096F, PI096G, PI096H, PI096I, PI096J, PI096K, PI096L, PI096M, PI096O, PI096P,
                               PI32A, PI32B, PI32C, PI32D, PI32E, PI32F, PI32G, PI32H, PI32I, PI32J, PI32K, PI32L, PI32M, PI32N,
                               PI264A, PI264B, PI264C, PI264D, PI264E, PI264F, PI264G, PI264H,
                               full_rog_signal,
                               bottom_A, bottom_B, bottom_C, bottom_D, top_A, top_B, top_C, top_D,
                               cube_AA, cube_AB, cube_BA, cube_BB, cube_CA, cube_CB, cube_DA, cube_DB, cube_EA, cube_EB, cube_FA, cube_FB
                               ]

        return magnetic_diagnostic, time
    
    
    def raw_density(self):
        # Grab and scale density measurements
        
        int001 = 0.5 * CTHData(self.shot, 'processed:intfrm_1mm:int_nedl_1').data
        int002 = 0.5 * CTHData(self.shot, 'processed:intfrm_1mm:int_nedl_2').data
        int003 = 0.5 * CTHData(self.shot, 'processed:intfrm_1mm:int_nedl_3').data
        
        time = CTHData(self.shot, 'processed:intfrm_1mm:int_nedl_2').time
        int_diagnostic = [int001, int002, int003]
        
        return int_diagnostic, time
    
    
    def raw_pressure(self):
        # Function to estimate the pressure scale.
        # This estimate will need to be improved with Thomson Scattering
        
        int002 = 0.5 * CTHData(self.shot, 'processed:intfrm_1mm:int_nedl_2').data                
        time = CTHData(self.shot, 'processed:intfrm_1mm:int_nedl_2').time
        
        pres_scale = 8.60E-17*int002
        

        return [pres_scale], time
    
     
    def raw_sxr(self):
        # Function to grab the SXR Two-Color Camera Data        
        
        
        
        #1.8um sxr cameras
        #Middle Camera
        SC252_000_18_1 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252000TN1').data
        SC252_000_18_2 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252000TN2').data
        SC252_000_18_3 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252000TN3').data
        SC252_000_18_4 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252000TN4').data
        SC252_000_18_5 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252000TN5').data
        SC252_000_18_6 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252000TN6').data
        SC252_000_18_7 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252000TN7').data
        SC252_000_18_8 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252000TN8').data
        SC252_000_18_9 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252000TN9').data
        SC252_000_18_10= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252000TN10').data
        SC252_000_18_11= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252000TN11').data
        SC252_000_18_12= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252000TN12').data
        SC252_000_18_13= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252000TN13').data
        SC252_000_18_14= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252000TN14').data
        SC252_000_18_15= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252000TN15').data
        SC252_000_18_16= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252000TN16').data
        SC252_000_18_17= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252000TN17').data
        SC252_000_18_18= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252000TN18').data
        SC252_000_18_19= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252000TN19').data
        SC252_000_18_20= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252000TN20').data
        
        #Top Camera
        SC252_060_18_1 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252060TN1').data
        SC252_060_18_2 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252060TN2').data
        SC252_060_18_3 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252060TN3').data
        SC252_060_18_4 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252060TN4').data
        SC252_060_18_5 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252060TN5').data
        SC252_060_18_6 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252060TN6').data
        SC252_060_18_7 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252060TN7').data
        SC252_060_18_8 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252060TN8').data
        SC252_060_18_9 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252060TN9').data
        SC252_060_18_10= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252060TN10').data
        SC252_060_18_11= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252060TN11').data
        SC252_060_18_12= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252060TN12').data
        SC252_060_18_13= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252060TN13').data
        SC252_060_18_14= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252060TN14').data
        SC252_060_18_15= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252060TN15').data
        SC252_060_18_16= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252060TN16').data
        SC252_060_18_17= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252060TN17').data
        SC252_060_18_18= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252060TN18').data
        SC252_060_18_19= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252060TN19').data
        SC252_060_18_20= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252060TN20').data        
        
        #Bottom Camera
        SC252_300_18_1 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252300TN1').data
        SC252_300_18_2 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252300TN2').data
        SC252_300_18_3 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252300TN3').data
        SC252_300_18_4 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252300TN4').data
        SC252_300_18_5 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252300TN5').data
        SC252_300_18_6 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252300TN6').data
        SC252_300_18_7 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252300TN7').data
        SC252_300_18_8 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252300TN8').data
        SC252_300_18_9 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252300TN9').data
        SC252_300_18_10= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252300TN10').data
        SC252_300_18_11= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252300TN11').data
        SC252_300_18_12= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252300TN12').data
        SC252_300_18_13= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252300TN13').data
        SC252_300_18_14= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252300TN14').data
        SC252_300_18_15= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252300TN15').data
        SC252_300_18_16= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252300TN16').data
        SC252_300_18_17= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252300TN17').data
        SC252_300_18_18= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252300TN18').data
        SC252_300_18_19= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252300TN19').data
        SC252_300_18_20= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252300TN20').data
        
        #3.0um filter
        #Middle Camera
        SC252_000_30_1 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252000TK1').data
        SC252_000_30_2 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252000TK2').data
        SC252_000_30_3 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252000TK3').data
        SC252_000_30_4 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252000TK4').data
        SC252_000_30_5 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252000TK5').data
        SC252_000_30_6 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252000TK6').data
        SC252_000_30_7 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252000TK7').data
        SC252_000_30_8 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252000TK8').data
        SC252_000_30_9 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252000TK9').data
        SC252_000_30_10= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252000TK10').data
        SC252_000_30_11= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252000TK11').data
        SC252_000_30_12= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252000TK12').data
        SC252_000_30_13= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252000TK13').data
        SC252_000_30_14= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252000TK14').data
        SC252_000_30_15= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252000TK15').data
        SC252_000_30_16= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252000TK16').data
        SC252_000_30_17= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252000TK17').data
        SC252_000_30_18= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252000TK18').data
        SC252_000_30_19= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252000TK19').data
        SC252_000_30_20= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252000TK20').data
        
        #Top Camera
        SC252_060_30_1 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252060TK1').data
        SC252_060_30_2 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252060TK2').data
        SC252_060_30_3 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252060TK3').data
        SC252_060_30_4 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252060TK4').data
        SC252_060_30_5 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252060TK5').data
        SC252_060_30_6 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252060TK6').data
        SC252_060_30_7 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252060TK7').data
        SC252_060_30_8 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252060TK8').data
        SC252_060_30_9 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252060TK9').data
        SC252_060_30_10= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252060TK10').data
        SC252_060_30_11= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252060TK11').data
        SC252_060_30_12= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252060TK12').data
        SC252_060_30_13= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252060TK13').data
        SC252_060_30_14= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252060TK14').data
        SC252_060_30_15= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252060TK15').data
        SC252_060_30_16= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252060TK16').data
        SC252_060_30_17= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252060TK17').data
        SC252_060_30_18= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252060TK18').data
        SC252_060_30_19= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252060TK19').data
        SC252_060_30_20= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252060TK20').data        
        
        #Bottom Camera
        SC252_300_30_1 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252300TK1').data
        SC252_300_30_2 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252300TK2').data
        SC252_300_30_3 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252300TK3').data
        SC252_300_30_4 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252300TK4').data
        SC252_300_30_5 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252300TK5').data
        SC252_300_30_6 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252300TK6').data
        SC252_300_30_7 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252300TK7').data
        SC252_300_30_8 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252300TK8').data
        SC252_300_30_9 = 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252300TK9').data
        SC252_300_30_10= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252300TK10').data
        SC252_300_30_11= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252300TK11').data
        SC252_300_30_12= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252300TK12').data
        SC252_300_30_13= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252300TK13').data
        SC252_300_30_14= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252300TK14').data
        SC252_300_30_15= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252300TK15').data
        SC252_300_30_16= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252300TK16').data
        SC252_300_30_17= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252300TK17').data
        SC252_300_30_18= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252300TK18').data
        SC252_300_30_19= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252300TK19').data
        SC252_300_30_20= 1E6 * CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252300TK20').data
        
        time = CTHData(self.shot, 'PROCESSED:SXR:SXRDECONSIGS:SD252300TK20').time

        sxr_diagnostic = [SC252_000_18_1, SC252_000_18_2, SC252_000_18_3, SC252_000_18_4, SC252_000_18_5, SC252_000_18_6, SC252_000_18_7 ,SC252_000_18_8, SC252_000_18_9, SC252_000_18_10,
                          SC252_000_18_11, SC252_000_18_12, SC252_000_18_13, SC252_000_18_14, SC252_000_18_15, SC252_000_18_16, SC252_000_18_17, SC252_000_18_18, SC252_000_18_19, SC252_000_18_20,
                          SC252_060_18_1, SC252_060_18_2, SC252_060_18_3, SC252_060_18_4, SC252_060_18_5, SC252_060_18_6, SC252_060_18_7 ,SC252_060_18_8, SC252_060_18_9, SC252_060_18_10,
                          SC252_060_18_11, SC252_060_18_12, SC252_060_18_13, SC252_060_18_14, SC252_060_18_15, SC252_060_18_16, SC252_060_18_17, SC252_060_18_18, SC252_060_18_19, SC252_060_18_20,
                          SC252_300_18_1, SC252_300_18_2, SC252_300_18_3, SC252_300_18_4, SC252_300_18_5, SC252_300_18_6, SC252_300_18_7 ,SC252_300_18_8, SC252_300_18_9, SC252_300_18_10,
                          SC252_300_18_11, SC252_300_18_12, SC252_300_18_13, SC252_300_18_14, SC252_300_18_15, SC252_300_18_16, SC252_300_18_17, SC252_300_18_18, SC252_300_18_19, SC252_300_18_20,
                          SC252_000_30_1, SC252_000_30_2, SC252_000_30_3, SC252_000_30_4, SC252_000_30_5, SC252_000_30_6, SC252_000_30_7 ,SC252_000_30_8, SC252_000_30_9, SC252_000_30_10,
                          SC252_000_30_11, SC252_000_30_12, SC252_000_30_13, SC252_000_30_14, SC252_000_30_15, SC252_000_30_16, SC252_000_30_17, SC252_000_30_18, SC252_000_30_19, SC252_000_30_20,
                          SC252_060_30_1, SC252_060_30_2, SC252_060_30_3, SC252_060_30_4, SC252_060_30_5, SC252_060_30_6, SC252_060_30_7 ,SC252_060_30_8, SC252_060_30_9, SC252_060_30_10,
                          SC252_060_30_11, SC252_060_30_12, SC252_060_30_13, SC252_060_30_14, SC252_060_30_15, SC252_060_30_16, SC252_060_30_17, SC252_060_30_18, SC252_060_30_19, SC252_060_30_20,
                          SC252_300_30_1, SC252_300_30_2, SC252_300_30_3, SC252_300_30_4, SC252_300_30_5, SC252_300_30_6, SC252_300_30_7 ,SC252_300_30_8, SC252_300_30_9, SC252_300_30_10,
                          SC252_300_30_11, SC252_300_30_12, SC252_300_30_13, SC252_300_30_14, SC252_300_30_15, SC252_300_30_16, SC252_300_30_17, SC252_300_30_18, SC252_300_30_19, SC252_300_30_20
                          ]
        
        return sxr_diagnostic, time
 
    
    
    
    
    









