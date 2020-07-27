# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import matplotlib.pyplot as plt
import MDSplus as mds
import numpy as np
from scipy import signal



class Thomson:
    
    def __init__(self, shot):
        self.shot = shot
        
        
        def get_raw_data(shot):
            tree = 't' + str(shot)[0:6]
            
            #conn = mds.connection.Connection('mds.physics.auburn.edu')
            conn = mds.connection.Connection('131.204.212.37')
            conn.openTree(tree, shot)
            
            pmt_data        = -1*conn.get('thomson:ch1').data()  
            ch2_data        = -1*conn.get('thomson:ch2').data()
            diode_data      = -1*conn.get('thomson:ch3').data()
            ch4_data        = -1*conn.get('thomson:ch4').data()
        
            timebase        = conn.get('thomson:data_dt').data()
            t0 = conn.get('parameters:timing:trig_3c_dly').data()/1000.0
            
            conn.closeAllTrees()
    
            length          = len(pmt_data)
            time            = np.linspace(t0, t0 + timebase*length, length)
            time            = np.linspace(0, 200, length)
            
            return  time, pmt_data, ch2_data, diode_data, ch4_data


        [self.time, self.pmt_data, self.ch2_data, self.diode_data, 
         self.ch4_data] = get_raw_data(self.shot)
        
        
    def raw_volt_to_e(self, voltage, resistance, tau, gain):
        #takes the raw voltage and returns the number of electrons
        e = 1.60217662 * 10 **-19
    
        n = (tau * voltage)/(gain * e * resistance)
        return n

       
    def get_corrected_pmt_data(self):
        time = self.time
        R = 2 * 10**6
        mu = 2 * 10**5
        tau = 2 * 10**-9
        
        corrected_pmt_data = self.raw_volt_to_e(self.pmt_data, R, tau, mu )    
        return  time, corrected_pmt_data           


    def get_pmt_data_smooth1(self):
        time, data = self.time, self.pmt_data
        time, data = self.get_corrected_pmt_data()
        
        smooth_data = signal.savgol_filter(data, 9001, 1)
        return time, smooth_data
    
    
    def get_pmt_data_smooth2(self):
        time, data = self.get_pmt_data_smooth1()    
        smooth_data2 = signal.savgol_filter(data, 8001, 2)
        return time, smooth_data2
            
            
    def plot_pmt(self, color):
        time, thom = self.pmt_data()
        plt.subplot(1,1,1)
        plt.plot(time, thom, color)
        
    
    def plot_pmt_smooth(self, color):
        time, smooth_data = self.get_pmt_data_smooth1()      
        plt.subplot(1,1,1)
        plt.plot(time, smooth_data, color)
        
        
    def plot_pmt_smooth2(self, color):
        time, smooth_data = self.get_pmt_data_smooth2()            
        plt.subplot(1,1,1)
        plt.plot(time, smooth_data, color)

    
    def get_diode_data_smooth(self):
        time, data = self.time, self.diode_data
        smooth_data = signal.savgol_filter(data, 4001, 1)
        return time, smooth_data


    def plot_diode(self, color):
        time, data = self.time, self.diode_data
        plt.subplot(1,1,1)
        plt.plot(time, data, color)


    def plot_diode_smooth(self, color):
        time, smooth_data = self.get_diode_data_smooth()       
        plt.subplot(1,1,1)
        plt.plot(time, smooth_data, color)
    
    





