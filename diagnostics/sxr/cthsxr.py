# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 11:26:38 2018

@author: James Kring
@email:  jdk0026@auburn.edu
"""

# =============================================================================
# Purpose: Grab and process the SXR Diagnostics on CTH
# Updates: 5/21/20: Updated to apply relative calibration and phase correction
# 
# To Do: 
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
from cthdata import CTHData
import scipy.io as io


sxr_diagnotistic_file_directory = '/home/cth/cthgroup/Python/recon/diagnostic_files/'

def find_closest_index(array, value):
    new_array = abs(array - value)
    try:
        index = new_array.argmin()
    except:
        print('Invalid Array')
        index = 0
        
        
    return int(index)



def phase_correct(ydata, freqs, amps, phases,
                  set_max_freq=None):
    # Function to the phase for SXR and bolometers
    # based on phase_correct_sxr.pro by Jeff Herfindal
    # Returns the phase corrected ydata as data
    acq_freq = 5.0E5
    if set_max_freq:
        max_freq = set_max_freq
    else:
        max_freq = 30.0E3
    
    max_freq_index = find_closest_index(freqs,max_freq)
    
    freq = freqs[:max_freq_index]
    amp  = amps[:max_freq_index]
    phase= phases[:max_freq_index]
    
    fftsize = len(ydata)
    deltaFreq = acq_freq/fftsize
    freq_fft = np.linspace(0,fftsize/2,int(fftsize/2+1))*deltaFreq
    data = np.zeros(ydata.shape)

    start = find_closest_index(freq_fft,freq[0]) 
    stop  = find_closest_index(freq_fft,freq[-1])    
    
    amp_new = np.zeros(int(fftsize/2+1))
    phase_new=np.zeros(int(fftsize/2+1))    
    
    amp_new[0:start-1] = 1.0
    amp_new[stop:]= 0.0
    
    phase_new[0:start-1] = 0.0
    phase_new[stop:] = 0.0    
    
    amp_new[start:stop] = np.interp(freq_fft[start:stop], freq,amp)
    phase_new[start:stop] = np.interp(freq_fft[start:stop], freq, phase)


    # Transfer function or filter amplification functions
    # Amplifies the frequences that are attenuated by amplifier circuit
    hf = np.zeros(fftsize,dtype=np.complex)

    hf[:int(fftsize/2)] = amp_new[0:-1]*np.exp(0+1j)*phase_new[0:-1]
    hf[int(fftsize/2+1):]= np.flip(amp_new[0:-2]*np.exp(-1.0*(0+1j))*phase_new[0:len(amp_new)-2])

    # fft works differently than in IDL
    # I am sum the phase corrected fft with the original fft before
    # taking the inverse fft. This allows it to give the actual data back.
    data = np.fft.irfft((hf[:int(len(ydata)/2+1)]*np.fft.rfft(ydata)+np.fft.rfft(ydata)))

    return data
  


with open(sxr_diagnotistic_file_directory + 'geo_factor.txt', 'r') as f:
    geo_factor = [float(line.rstrip()) for line in f.readlines()]


decon = io.readsav(sxr_diagnotistic_file_directory+'SC_decon_dec_2016.sav',
                   idict=None, python_dict=False, 
                   uncompressed_file_name=None, verbose=False)

calib = io.readsav(sxr_diagnotistic_file_directory+'sxr_relative_calib.sav',
                   idict=None, python_dict=False, 
                   uncompressed_file_name=None, verbose=False)


class Bolometer:
    def __init__(self, shot, half_field=True, full_field=False):
        self.shot = shot
        
        if half_field:
            self.get_half_field_data()
        if full_field:
            self.get_full_field_data()
            
        
    def get_half_field_data(self):
        b252_000 = np.linspace(236, 255, 20)
        b252_060 = np.linspace(716, 735, 20)
        b252_300 = np.linspace(756, 775, 20)

        # =============================================================================
        # SXR Camera SC252_000_TK
        # Bad Channels: 8, 11
        # 
        # =============================================================================

        b252_000_data = []
        for i, number in enumerate(b252_000):
            data = CTHData(self.shot, str(int(number)), channel_number=True)
            ydata= (data.data*calib['sc252_000_tk_rel']['rel_cal'][0][i]/geo_factor[i])
            corrected_ydata = phase_correct(ydata,
                                            decon['elec_atten_bo']['freq'][0],
                                            decon['elec_atten_bo']['amplitude'][0],
                                            decon['elec_atten_bo']['phase_rad'][0])
            b252_000_data.append(corrected_ydata)          
    
    
        self.time = data.time

        b252_000_data[8] = (b252_000_data[7] + b252_000_data[9])/2
        b252_000_data[11] = (b252_000_data[10] + b252_000_data[12])/2

        # =============================================================================
        # SXR Camera SC252_060_TK
        # Bad Channels: 7, 19
        # 
        # =============================================================================
        
        b252_060_data = []
        for i, number in enumerate(b252_060):
            data = CTHData(self.shot, str(int(number)), channel_number=True)
            ydata= (data.data*calib['sc252_060_tk_rel']['rel_cal'][0][i]/geo_factor[i])
            corrected_ydata = phase_correct(ydata,
                                            decon['elec_atten_bo']['freq'][0],
                                            decon['elec_atten_bo']['amplitude'][0],
                                            decon['elec_atten_bo']['phase_rad'][0])
            b252_060_data.append(corrected_ydata)
            
        b252_060_data[7] = (b252_060_data[6] + b252_060_data[8])/2
        b252_060_data[19] = b252_060_data[18]

        # =============================================================================
        # SXR Camera SC252_300_TK
        # Bad Channels: 15
        # 
        # =============================================================================

        b252_300_data = []
        for i, number in enumerate(b252_300):
            data = CTHData(self.shot, str(int(number)), channel_number=True)
            ydata= (data.data*calib['sc252_300_tk_rel']['rel_cal'][0][i]/geo_factor[i])
            corrected_ydata = phase_correct(ydata,
                                            decon['elec_atten_bo']['freq'][0],
                                            decon['elec_atten_bo']['amplitude'][0],
                                            decon['elec_atten_bo']['phase_rad'][0])
            b252_300_data.append(corrected_ydata)

        b252_300_data[15] = (b252_300_data[14] + b252_300_data[16])/2

        self.b252_000 = b252_000_data
        self.b252_060 = b252_060_data
        self.b252_300 = b252_300_data

        return

        
    def get_full_field_data(self):
        b036_014 = np.linspace(352, 371, 20)
        b036_060 = np.linspace(312, 331, 20)
        
        # =============================================================================
        # SXR Camera SC036_014_TK
        # Bad Channels: 
        # 
        # =============================================================================

        b036_014_data = []
        for i, number in enumerate(b036_014):
            data = CTHData(self.shot, str(int(number)), channel_number=True)
            ydata= (data.data*calib['sc000_270_bo_rel']['rel_cal'][0][i]/geo_factor[i])
            corrected_ydata = phase_correct(ydata,
                                            decon['elec_atten_bo']['freq'][0],
                                            decon['elec_atten_bo']['amplitude'][0],
                                            decon['elec_atten_bo']['phase_rad'][0])
            b036_014_data.append(corrected_ydata)
            
        self.time = data.time

        # =============================================================================
        # SXR Camera SC036_060_TK
        # Bad Channels: 
        # 
        # =============================================================================

        b036_060_data = []
        for i,number in enumerate(b036_060):
            data = CTHData(self.shot, str(int(number)), channel_number=True)
            ydata= (data.data*calib['sc036_060_bo_rel']['rel_cal'][0][i]/geo_factor[i])
            corrected_ydata = phase_correct(ydata,
                                            decon['elec_atten_bo']['freq'][0],
                                            decon['elec_atten_bo']['amplitude'][0],
                                            decon['elec_atten_bo']['phase_rad'][0])
            b036_060_data.append(corrected_ydata)

        self.b036_014 = b036_014_data
        self.b036_060 = b036_060_data

        return
    
    
    def plot_camera(self,camera='b252_000', time=[1.62, 1.70],
                    save=False, save_dir=''):
        
        if camera=='b252_000':
            data = self.b252_000
            title = 'BO 252 000' + '\n Shot: ' + str(self.shot)
        elif camera=='b252_060':
            data = self.b252_060
            title = 'BO 252 060' + '\n Shot: ' + str(self.shot)            
        elif camera=='b252_300':
            data = self.b252_300
            title = 'BO 252 300' + '\n Shot: ' + str(self.shot)   
        elif camera=='b036_014':
            data = self.b036_014
            title = 'BO 036 014' + '\n Shot: ' + str(self.shot)
        elif camera=='b036_060':
            data = self.b036_060
            title = 'BO 036 060' + '\n Shot: ' + str(self.shot) 
        
        id1 = find_closest_index(self.time,time[0])
        id2 = find_closest_index(self.time,time[1])
        cmap1='gnuplot2'
        channels = np.linspace(1,20, 20).tolist()
        plt.contourf(self.time.tolist()[id1:id2],channels,np.array(data)[:][id1:id2],cmap=cmap1)
        plt.title(title,fontsize = 15, weight ='bold')
        plt.xlabel('Time (sec)',fontsize = 15, weight ='bold')
        plt.ylabel('Channel Number',fontsize = 15, weight ='bold')
        plt.xticks(fontsize=13,weight='bold')
        plt.yticks(fontsize=13,weight='bold')   
        plt.gca().invert_yaxis()
        
        cbar = plt.colorbar()
        labels = [item.get_text() for item in cbar.ax.get_yticklabels()]
        cbar.ax.set_yticklabels(labels,fontsize=13, weight='bold')       
        cbar.set_label('Relative Intensity', rotation=270,fontsize=13, weight='bold',labelpad=15)

        if save:
            filename = str(save_dir + str(camera) +'_' + str(self.shot) +
                           '_' + str(time[0]) + '_' + str(time[1]) + '.png')
            plt.savefig(filename, format='png', dpi = 1000,  bbox_inches='tight')
            plt.close()
            
            
class SXR_TN:
    def __init__(self, shot, half_field=True, full_field=False):
        self.shot = shot
        
        if half_field:
            self.get_half_field_data()
        if full_field:
            self.get_full_field_data()
            
        
    def get_half_field_data(self):
        tn252_000 = np.linspace(216, 235, 20)
        tn252_060 = np.linspace(696, 715, 20)
        tn252_300 = np.linspace(736, 755, 20)
        
        # =============================================================================
        # SXR Camera SC252_000_TN
        # Bad Channels: 11, 13
        # 
        # =============================================================================

        tn252_000_data = []
        for i, number in enumerate(tn252_000):
            data = CTHData(self.shot, str(int(number)), channel_number=True)
            ydata= (data.data*calib['sc252_000_tn_rel']['rel_cal'][0][i]/geo_factor[i])
            corrected_ydata = phase_correct(ydata,
                                            decon['elec_atten_tn']['freq'][0],
                                            decon['elec_atten_tn']['amplitude'][0],
                                            decon['elec_atten_tn']['phase_rad'][0])
            tn252_000_data.append(corrected_ydata)
            
        self.time = data.time

        tn252_000_data[11] = (tn252_000_data[10] + tn252_000_data[12])/2
        tn252_000_data[13] = (tn252_000_data[12] + tn252_000_data[14])/2

        # =============================================================================
        # SXR Camera SC252_060_TN
        # Bad Channels: 11
        # 
        # =============================================================================

        
        tn252_060_data = []
        for i, number in enumerate(tn252_060):
            data = CTHData(self.shot, str(int(number)), channel_number=True)
            ydata= (data.data*calib['sc252_060_tn_rel']['rel_cal'][0][i]/geo_factor[i])
            corrected_ydata = phase_correct(ydata,
                                            decon['elec_atten_tn']['freq'][0],
                                            decon['elec_atten_tn']['amplitude'][0],
                                            decon['elec_atten_tn']['phase_rad'][0])
            tn252_060_data.append(corrected_ydata)
            
        tn252_060_data[11] = (tn252_060_data[10] + tn252_060_data[12])/2

        # =============================================================================
        # SXR Camera SC252_300_TN
        # Bad Channels: 11
        # 
        # =============================================================================

        tn252_300_data = []
        for i, number in enumerate(tn252_300):
            data = CTHData(self.shot, str(int(number)), channel_number=True)
            ydata= (data.data*calib['sc252_300_tn_rel']['rel_cal'][0][i]/geo_factor[i])
            corrected_ydata = phase_correct(ydata,
                                            decon['elec_atten_tn']['freq'][0],
                                            decon['elec_atten_tn']['amplitude'][0],
                                            decon['elec_atten_tn']['phase_rad'][0])
            tn252_300_data.append(corrected_ydata)

        tn252_300_data[11] = (tn252_300_data[10] + tn252_300_data[12])/2

        self.tn252_000 = tn252_000_data
        self.tn252_060 = tn252_060_data
        self.tn252_300 = tn252_300_data

        return

        
    def get_full_field_data(self):
        tn036_014 = np.linspace(372, 391, 20)
        tn036_060 = np.linspace(322, 351, 20)
        
        # =============================================================================
        # SXR Camera SC036_014_TN
        # Bad Channels: 
        # 
        # =============================================================================
        
        tn036_014_data = []
        for i, number in enumerate(tn036_014):
            data = CTHData(self.shot, str(int(number)), channel_number=True)
            ydata= (data.data*calib['sc000_270_tn_rel']['rel_cal'][0][i]/geo_factor[i])
            corrected_ydata = phase_correct(ydata,
                                            decon['elec_atten_tn']['freq'][0],
                                            decon['elec_atten_tn']['amplitude'][0],
                                            decon['elec_atten_tn']['phase_rad'][0])
            tn036_014_data.append(corrected_ydata)
            
        self.time = data.time
        
        # =============================================================================
        # SXR Camera SC036_060_TN
        # Bad Channels: 8, 10, 11
        # 
        # =============================================================================
        
        tn036_060_data = []
        for i,number in enumerate(tn036_060):
            data = CTHData(self.shot, str(int(number)), channel_number=True)
            ydata= (data.data*calib['sc036_060_tn_rel']['rel_cal'][0][i]/geo_factor[i])
            corrected_ydata = phase_correct(ydata,
                                            decon['elec_atten_tn']['freq'][0],
                                            decon['elec_atten_tn']['amplitude'][0],
                                            decon['elec_atten_tn']['phase_rad'][0])
            tn036_060_data.append(corrected_ydata)
            
        tn036_060_data[11] = (tn036_060_data[9] + tn036_060_data[12])/2
        tn036_060_data[10] = (tn036_060_data[9] + tn036_060_data[11])/2
        tn036_060_data[8]  = (tn036_060_data[7] + tn036_060_data[9])/2


        self.tn036_014 = tn036_014_data
        self.tn036_060 = tn036_060_data

        return
    
    
    def plot_camera(self,camera='tn252_000', time=[1.62, 1.70],
                    save=False, save_dir=''):
        
        if camera=='tn252_000':
            data = self.tn252_000
            title = 'TN 252 000' + '\n Shot: ' + str(self.shot)
        elif camera=='tn252_060':
            data = self.tn252_060
            title = 'TN 252 060' + '\n Shot: ' + str(self.shot)            
        elif camera=='tn252_300':
            data = self.tn252_300
            title = 'TN 252 300' + '\n Shot: ' + str(self.shot)   
        elif camera=='tn036_014':
            data = self.b036_014
            title = 'TN 036 014' + '\n Shot: ' + str(self.shot)
        elif camera=='tn036_060':
            data = self.tn036_060
            title = 'TN 036 060' + '\n Shot: ' + str(self.shot) 
        
        id1 = find_closest_index(self.time,time[0])
        id2 = find_closest_index(self.time,time[1])
        
        
        cmap1='gnuplot2'
        channels = np.linspace(1,20, 20).tolist()
        plt.contourf(self.time.tolist()[id1:id2],channels,np.array(data)[:][id1:id2],cmap=cmap1)
        plt.title(title,fontsize = 15, weight ='bold')
        plt.xlabel('Time (sec)',fontsize = 15, weight ='bold')
        plt.ylabel('Channel Number',fontsize = 15, weight ='bold')
        plt.xticks(fontsize=13,weight='bold')
        plt.yticks(fontsize=13,weight='bold')   
        plt.gca().invert_yaxis()
        
        cbar = plt.colorbar()
        labels = [item.get_text() for item in cbar.ax.get_yticklabels()]
        cbar.ax.set_yticklabels(labels,fontsize=13, weight='bold')       
        cbar.set_label('Relative Intensity', rotation=270,fontsize=13, weight='bold',labelpad=15)

        if save:
            filename = str(save_dir + str(camera) +'_' + str(self.shot) +
                           '_' + str(time[0]) + '_' + str(time[1]) + '.png')
            plt.savefig(filename, format='png', dpi = 1000,  bbox_inches='tight')
            plt.close()




