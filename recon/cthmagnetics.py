# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 11:21:59 2018

@author: James Kring
@email:  jdk0026@auburn.edu
"""


# =============================================================================
# Purpose: Grab and process the Magnetic Diagnostics on CTH
# 
# To Do: Include other magnetic diagnostics if needed
# =============================================================================

# =============================================================================
# #Example:      
# test = Mirnov240Data(14021473)
# test.plot_contours(1.6346, 1.6351)
# =============================================================================


import matplotlib.pyplot as plt
import MDSplus as mds
import numpy as np
import pandas as pd
from matplotlib import rc
from matplotlib.offsetbox import AnchoredText
import matplotlib.ticker as mticker
from scipy import signal

def find_closest_index(array, value):
    new_array = abs(array - value)
    try:
        index = new_array.argmin()
    except:
        print('Invalid Array')
        index = 0
        
        
    return int(index)




class Mirnov240Data:
    
    def __init__(self, shot):
        self.shot = shot
        self.calib_file = pd.read_csv('/home/cth/cthgroup/Python/recon/diagnostic_files/mirnov240_poloidal.csv')
        self.n_coils = len(self.calib_file)
        self.data = []
        self.btheta = []
        self.btheta_smooth = []
        self.btheta_fluc = []
        self.time = []
        self.channel_number =  self.calib_file['Channel']
        self.board = self.calib_file['Board']
        self.theta = self.calib_file['theta']
        
        self.get_data()
        self.process_data()
        self.sort_channels()
        self.delete_channel([ 2, 10]) #two bad probs
        self.sort_channels_theta()
        
    def get_data(self):
        tree = 't' + str(self.shot)[0:6]
                
        conn = mds.connection.Connection('mds.physics.auburn.edu')
        #conn = mds.connection.Connection('131.204.212.37')
        conn.openTree(tree, self.shot)        
        
        for i in range(self.n_coils):
            channel =str('ACQ196' + str(self.board[i]) + ':INPUT_' 
                         + str(self.channel_number[i]).zfill(2))

            raw_data = 10*conn.get(channel).data() #Tesla per second
            self.data.append(raw_data * self.calib_file['calib'][i])
                     
        time_channel = 'dim_of(' + channel + ')'
        self.time = conn.get(time_channel)
        
        conn.closeAllTrees()
        return
    
    
    def process_data(self):
        t1 = find_closest_index(self.time, 1.59)
        t2 = find_closest_index(self.time, 1.60)
        
        subt1 = find_closest_index(self.time, 1.615)
        subt2 = find_closest_index(self.time, 1.62)

        dt = self.time[1]-self.time[0]

        for i in range(self.n_coils):
            int_data = np.cumsum(np.array(self.data[i])) * dt #Teslas
            print(i)
            tfity = signal.savgol_filter(int_data, 151, 0)
            
            fit = np.polyfit(self.time[t1:t2], tfity[t1:t2], 1)

            int_data = int_data - (fit[0] * self.time + fit[1])
            
            int_data = abs(int_data - np.mean(int_data[subt1:subt2]))
            
            smooth_data = signal.savgol_filter(int_data, 151, 0)
            
            fluc_data = int_data - smooth_data
            
            #Teslas
            self.btheta.append(int_data)
            self.btheta_smooth.append(smooth_data)
            self.btheta_fluc.append(fluc_data)
            

    def sort_channels(self):
        sort_array = self.channel_number
        self.btheta_fluc = [y for x,y in sorted(zip(sort_array, self.btheta_fluc))]
        self.btheta_smooth = [y for x,y in sorted(zip(sort_array, self.btheta_smooth))]
        self.btheta = [y for x,y in sorted(zip(sort_array, self.btheta))]
        self.theta = [y for x,y in sorted(zip(sort_array, self.theta))]
        
        self.channel_number = sorted(self.channel_number)
        
        
    def sort_channels_theta(self):
        sort_array = self.theta
        self.btheta_fluc = [y for x,y in sorted(zip(sort_array, self.btheta_fluc))]
        self.btheta_smooth = [y for x,y in sorted(zip(sort_array, self.btheta_smooth))]
        self.btheta = [y for x,y in sorted(zip(sort_array, self.btheta))]
        self.theta = [y for x,y in sorted(zip(sort_array, self.theta))]
        
        self.channel_number = sorted(self.channel_number)


    def delete_channel(self, channel_numbers):
        for channel_number in channel_numbers:
            
            num = self.channel_number.index(channel_number)
            
            del self.channel_number[num]
            del self.btheta[num]
            del self.btheta_fluc[num]
            del self.btheta_smooth[num]
            del self.theta[num]
            
            
    def plot_contours(self, start_time, stop_time, shot_number=False):
        t1 = find_closest_index(self.time, start_time)
        t2 = find_closest_index(self.time, stop_time)
        
        length = t2-t1
        skip = int(length//200)
        
        a = []
        for i in range(len(self.channel_number)):
            b = self.btheta_fluc[i][t1:t2]*100
            a.append(b[::skip])
        
        time = self.time[t1:t2]
        
        #plt.figure()
        plt.tight_layout()
        
        plt.contourf((time[::skip]), self.theta, a, 20,
                     cmap = 'gnuplot2')
                
        if shot_number:
            title = 'Poloidal Array Shot: ' + str(self.shot)
        else:
            title = 'Poloidal Array'
        
        plt.xlim([start_time, stop_time])
        plt.xticks(fontsize=13,weight='bold')
        plt.yticks(fontsize=13,weight='bold')
        cbar = plt.colorbar()
        labels = [item.get_text() for item in cbar.ax.get_yticklabels()]
        cbar.ax.set_yticklabels(labels,fontsize=13, weight='bold')
        cbar.set_label('Relative Intensity', rotation=270,fontsize=13, weight='bold',labelpad=15)

        plt.title(title,fontsize = 15, weight ='bold')
        plt.xlabel('Time (s)',fontsize = 15, weight ='bold')
        plt.ylabel('Poloidal Angle (' +  r'$\theta$' + ', degrees)',fontsize = 15, weight ='bold')
        #ax1.set_yticklabels(ax1.get_yticks(), {'weight' : 'bold', 'size' : 13})
        plt.locator_params(axis='x', nbins=6)
        plt.tight_layout()
        plt.show()
        
        
        
        
class ToroidalData:
    
    def __init__(self, shot):
        self.shot = shot
        self.calib_file = pd.read_csv('/home/cth/cthgroup/Python/recon/diagnostic_files/TA_bottom.csv')
        self.n_coils = len(self.calib_file)
        self.data = []
        self.bphi = []
        self.bphi_smooth = []
        self.bphi_fluc = []
        self.time = []
        self.channel_number =  self.calib_file['channel']
        self.board = self.calib_file['board']
        self.phi = self.calib_file['phi']
        
        self.get_data()
        self.process_data()
        self.sort_channels()
        #print(self.channel_number)
        self.delete_channel([57]) #two bad probes

        self.sort_channels_phi()
        
        
    def get_data(self):
        tree = 't' + str(self.shot)[0:6]
                
        #conn = mds.connection.Connection('mds.physics.auburn.edu')
        conn = mds.connection.Connection('131.204.212.37')
        conn.openTree(tree, self.shot)        
        
        for i in range(self.n_coils):
            channel =str('ACQ196' + str(self.board[i]) + ':INPUT_' 
                         + str(self.channel_number[i]).zfill(2))

            raw_data = 10*conn.get(channel).data() #Tesla per second
            self.data.append(raw_data * self.calib_file['calib'][i])
                     
        time_channel = 'dim_of(' + channel + ')'
        self.time = conn.get(time_channel)
        
        conn.closeAllTrees()
        return
    
    
    def process_data(self):
        t1 = find_closest_index(self.time, 1.59)
        t2 = find_closest_index(self.time, 1.60)
        
        subt1 = find_closest_index(self.time, 1.615)
        subt2 = find_closest_index(self.time, 1.62)

        dt = self.time[1]-self.time[0]

        for i in range(self.n_coils):
            int_data = np.cumsum(np.array(self.data[i])) * dt #Teslas
            
            tfity = signal.savgol_filter(int_data, 151, 0)
            
            fit = np.polyfit(self.time[t1:t2], tfity[t1:t2], 1)

            int_data = int_data - (fit[0] * self.time + fit[1])
            
            int_data = abs(int_data - np.mean(int_data[subt1:subt2]))
            
            smooth_data = signal.savgol_filter(int_data, 151, 0)
            
            fluc_data = int_data - smooth_data
            
            #Teslas
            self.bphi.append(int_data)
            self.bphi_smooth.append(smooth_data)
            self.bphi_fluc.append(fluc_data)


    def sort_channels(self):
        sort_array = self.channel_number
        self.btheta_fluc = [y for x,y in sorted(zip(sort_array, self.bphi_fluc))]
        self.btheta_smooth = [y for x,y in sorted(zip(sort_array, self.bphi_smooth))]
        self.btheta = [y for x,y in sorted(zip(sort_array, self.bphi))]
        self.theta = [y for x,y in sorted(zip(sort_array, self.phi))]
        
        self.channel_number = sorted(self.channel_number)
        
        
    def sort_channels_phi(self):
        sort_array = self.phi
        self.btheta_fluc = [y for x,y in sorted(zip(sort_array, self.bphi_fluc))]
        self.btheta_smooth = [y for x,y in sorted(zip(sort_array, self.bphi_smooth))]
        self.btheta = [y for x,y in sorted(zip(sort_array, self.bphi))]
        self.theta = [y for x,y in sorted(zip(sort_array, self.phi))]
        
        self.channel_number = sorted(self.channel_number)


    def delete_channel(self, channel_numbers):
        for channel_number in channel_numbers:
            num = self.channel_number.index(channel_number)

            del self.channel_number[num]
            del self.bphi[num]
            del self.bphi_fluc[num]
            del self.bphi_smooth[num]
            del self.phi[num]
            
            
    def plot_contours(self, start_time, stop_time, shot_number=True):
        t1 = find_closest_index(self.time, start_time)
        t2 = find_closest_index(self.time, stop_time)
        
        length = t2-t1
        skip = int(length//200)
        
        a = []
        for i in range(len(self.channel_number)):
            b = self.bphi_fluc[i][t1:t2]*10000
            a.append(b[::skip])
        
        time = self.time[t1:t2]
        
        #plt.figure()
        plt.contourf((time[::skip])*1000, self.phi, a, 20,
                     cmap = 'gnuplot2')#'RdGy'
        
        plt.colorbar()
        plt.locator_params(axis='x', nbins=5)
        if shot_number:
            title = 'Toroidal Array \n Shot: ' + str(self.shot)
        else:
            title = 'Toroidal Array'
            
        plt.title(title)
        plt.xlabel('Time (ms)')
        plt.ylabel('Toroidal Angle (' +  r'$\phi$' + ', degrees)')
        plt.tight_layout()
        plt.show() 
        
        

#shot = 14082141

#plt.figure()
#test = ToroidalData(shot)
#test.plot_contours(1.653, 1.654)
#plt.figure()



#shot = 20020516
#test = Mirnov240Data(shot)
#test.plot_contours(1.652, 1.6547)

