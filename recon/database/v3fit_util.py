# -*- coding: utf-8 -*-
"""
Created on Thu May 16 09:21:01 2019

@author: James Kring
@email:  jdk0026@auburn.edu
"""

from cthdata import CTHData
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter
import os
import subprocess
import v3fit_database as v3fit_db
#from cthsxr import SXRBolometerData
FNULL = open(os.devnull, 'w')



with open('/home/cth/cthgroup/Python/recon/scripts/geo_factor.txt', 'r') as f:
    geo_factor = [float(line.rstrip()) for line in f.readlines()]

new_g = np.concatenate([geo_factor, geo_factor, geo_factor])

def find_closest_index(array, value):
    # return the FIRST index of the array that closest matches the value
    
    new_array = abs(array - value)
    try:
        index = new_array.argmin()
    except:
        print('Invalid Array')
        index = 0    
    return int(index)
        

def get_ip_times_and_slices(shot):
    # function to grab the end times and number of slices need at 1 ms intervals
   
    ip = CTHData(shot, '\I_P')
    time, data = ip.time, ip.data    
    
    filtered_ip = savgol_filter(data, 151, 1)
    filtered_grad_ip = np.gradient(filtered_ip)
    
    end_ind1 = find_closest_index(filtered_grad_ip, -50)
    end_ind2 = find_closest_index(filtered_ip[end_ind1:], 500) + end_ind1
    
    start_time = 1.62
    end_time = round(time[end_ind2],3)
    n_slices = int((end_time - start_time)/0.001 + 1)
    
    return start_time, end_time, n_slices


def disrupt_time(time, data):
    start_ind = find_closest_index(time, 1.64)
    
    data = data[start_ind:]
    time = time[start_ind:]
    sec_grad = np.gradient(np.gradient(savgol_filter(data, 81, 1)))
    plt.plot(time, sec_grad)
    
    val_arr = [20, 15, 10, 5, 4, 3]
    pos_ind_array = []
    j = 0
    while len(pos_ind_array) < 1 and j < len(val_arr):
        pos_ind_array = [i for i in range(len(sec_grad)) if sec_grad[i] > val_arr[j]]
        j += 1

    neg_ind_array = []
    j = 0        
    while len(neg_ind_array) < 1 and j < len(val_arr):
        neg_ind_array = [i for i in range(len(sec_grad)) if sec_grad[i] < -1*val_arr[j]]
        j += 1
    
    line_times = []

    try:
        line_times.append(time[neg_ind_array[0]])
    except:
        print('Failed')
        
    try:
        line_times.append(time[pos_ind_array[0]])
    except:
        line_times.append(line_times[0] - .001)     
        

    return line_times



def send_cmd(command):
    # Simple function to pass a command to the bash shell
    try:
        subprocess.call(command, shell=True, stdout=FNULL, stderr=subprocess.STDOUT)
    except:
        print('Error Occurred')
        print('Following command not processed:', command)
        
    return


def get_param_index(recout, param):
    index = [idx for idx, name in enumerate(recout.param_name) if param in name][0]
    
    return index

def get_channel_average(shot, channel, time, window, channel_number=False):
    
    try:
        signal = CTHData(shot, channel, channel_number=channel_number)
    except:
        print(shot, channel)
        
    ind1 = find_closest_index(signal.time, time-window)
    ind2 = find_closest_index(signal.time, time+window)
    
    value = np.mean(signal.data[ind1:ind2])
    std   = np.std(signal.data[ind1:ind2],ddof=1)
    
    return [float(value),float(std)]


def get_channel_whole_then_average(shot, channel, times, window, scale, channel_number=False):
    
    try:
        signal = CTHData(shot, channel, channel_number=channel_number)
    except:
        print(shot, channel)
        
        
    results = []
        
    for time in times:
        
        
        ind1 = find_closest_index(signal.time, time-window)
        ind2 = find_closest_index(signal.time, time+window)
    
        value = np.mean(signal.data[ind1:ind2]/scale)
        std   = np.std(signal.data[ind1:ind2]/scale,ddof=1)
        
        results.append([float(value),float(std)])
    
    
    return results


def process_shot(shotnumber, server='recon2'):
    # Master function to get a shotnumber and perform full shot reconstruction
    # having a time slice every 0.001 seconds.
    # Process the data in the results database for analysis
    start_time, end_time, n_slices = get_ip_times_and_slices(shotnumber)
    
    if server =='recon2':
        cmd1 = str("python full_shot_runner.py " + str(shotnumber) + " " 
                   + str(start_time) + " "
                   + str(end_time) + " "
                   + str(n_slices))
    elif server=='hopper':
        cmd1 = str("python full_shot_runner.py " + str(shotnumber) + " " 
                   + str(start_time) + " "
                   + str(end_time) + " "
                   + str(n_slices) + " "
                   + "v3fit_template=/home/inst/jdk0026/bin/templates/input.fermi_example_hopper.v3fit")

                   
                   
    send_cmd(str('cd ~/bin/ &',cmd1))

def remove_bad_channels(channels, bad_channel, end=False, beginning=False):
    print('Bad Channel',bad_channel,'removed')
    channels = np.array(channels)
    data = (channels[bad_channel - 1,:] + channels[bad_channel + 1,:])/2
    #sigma = (channels[bad_channel - 1,:] + channels[bad_channel + 1,:])/2
    
    channels[bad_channel] = data
    """
    
    if end:
        channel = channels[bad_channel - 1]
        channels[bad_channel] = channel
    elif beginning:
        channel = channels[bad_channel + 1]
        channels[bad_channel] = channel
    else:
        channel = channels[bad_channel - 1] + channels[bad_channel + 1]
        channel = channel/2
        channels[bad_channel] = channel
        
    """
    
    return channels


def get_bolo_cameras(shot, times, window, pad_times=False):
    b252_000 = np.linspace(236, 255, 20)
    b252_060 = np.linspace(716, 735, 20)
    b252_300 = np.linspace(756, 775, 20)
    
    #a = [1E6]*20
    
    
    #b036_014 = np.linspace(352, 371, 20)
    #b036_060 = np.linspace(312, 331, 20)
    
    #8, 35, 47, 49
    
    channels = np.concatenate([b252_000, b252_060, b252_300])#, b036_014, b036_060])
    

    if pad_times:
        window = times[1] -times[0]
        step = window/5
        
        new_times = []
        for time in times:
            for ii in range(0,5):
                new_times.append(time+ii*step)
                
        times = np.array(new_times)

    bolo_signals_and_std = []
    
    
    for ii, channel in enumerate(channels):
        if ii < 20:
            bolo_signals_and_std.append(get_channel_whole_then_average(shot, str(int(channel)), times, window, 1E-6*new_g[ii], channel_number=True))
        else:
            bolo_signals_and_std.append(get_channel_whole_then_average(shot, str(int(channel)), times, window, 1E-6*new_g[ii], channel_number=True))
   
    bolo_signals_and_std = remove_bad_channels(bolo_signals_and_std, 8)
    bolo_signals_and_std = remove_bad_channels(bolo_signals_and_std, 11)
         
    bolo_signals_and_std = remove_bad_channels(bolo_signals_and_std, 27)    
    bolo_signals_and_std = remove_bad_channels(bolo_signals_and_std, 39)    
    bolo_signals_and_std = remove_bad_channels(bolo_signals_and_std, 55)    

    return bolo_signals_and_std.tolist()



def get_sxr_cameras(shot, times, window, pad_times=False):
    b252_000 = np.linspace(216, 235, 20)
    b252_060 = np.linspace(696, 715, 20)
    b252_300 = np.linspace(736, 755, 20)
    
    #b036_014 = np.linspace(372, 391, 20)
    #b036_060 = np.linspace(332, 351, 20)

    if pad_times:
        window = times[1] -times[0]
        step = window/5
        
        new_times = []
        for time in times:
            for ii in range(0,5):
                new_times.append(time+ii*step)
                
        times = np.array(new_times)

    
    channels = np.concatenate([b252_000, b252_060, b252_300])#, b036_014, b036_060])
    
    sxr_signals_and_std = []
    for ii, channel in enumerate(channels):
        sxr_signals_and_std.append(get_channel_whole_then_average(shot, str(int(channel)), times, window, 1E-6*new_g[ii], channel_number=True))
    
    return sxr_signals_and_std







