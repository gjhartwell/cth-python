# -*- coding: utf-8 -*-
"""
Created on Sat May 25 20:40:51 2019

@author: James Kring
@email:  jdk0026@auburn.edu
"""
import sys
#sys.path.insert(0, '/home/cth/cthgroup/Python/recon/scripts')
#sys.path.insert(0, 'Z:\Python\recon\scripts')
#from v3fit_util import get_ip_times_and_slices
from scipy.signal import savgol_filter
import numpy as np

from cthdata import CTHData



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













shot = 19060721


try:
    #infrm1 = CTHData(shot, 'processed:intfrm_1mm:est_den_1')
    #infrm2 = CTHData(shot, 'processed:intfrm_1mm:est_den_2')
    infrm = CTHData(shot, 'processed:intfrm_1mm:est_den_3')
except:
    print("Interferometer not grabbed")
    infrm1 = None










plt.figure()
plt.subplot(311)
plt.plot(infrm.time, infrm.data, 'k')











#start, stop, n_slices = get_ip_times_and_slices(shot)


#print(start, stop, n_slices)






"""
shots = [14090535,14090536,15031915,15031916,15031918,15031919,
         15031929,15031930,15032006,15032007,15032008,15032009,
         15032010,15032011,15032408,15032410,15032431,15032432,
         15032515,15032616,15032617,15032618,15032620,15032621,
         15032622,15032625,15032626,15032628,15032629,15032638,15032639,15032640,15052136,15052137,15052139,15052140,15052141,15052142,15052144,15052145,15052146,15052147,15052148,15052149,15052209,15052210,15052214,15052909,15052912,15052913,15052914,15052918,15052919,15052920,15052923,15052924,15052925,15052927,15052928,15052929,15052933,15052935,15052936,15052937,15052939,15052948,15052957,15060506,15060508,15060510,15060511,15060512,15060513,15060514,15060515,15060516,15060518,15060520,15060521,15060522,15060523,15060529,15061506,15061507,15061508,15061510,15061511,15061512,15061514,15061515,15061516,15061523,15061524,15061525,15061527,15061531,15061534,15061540,15061541,15061542,15061545,15061546,15061547,15061549,15061553,15061554,15061555,15061558,15061559,15061561,15061563,15061564,15061568,15062307,15062308,15062310,15062311,15062313,15062315,15062316,15062318,15062320,15062321,15062323,15062324,15062325,15062326,15062327,15062328,15062334,15062335,15062336,15062339,15062344,15062345,15062353,15062354,15062356,15062358,15062361,15062364,15062370,15062371,15062378,15062379,15062505,15062511,15062512,15062515,15062516,15062518]

shots = [14110641,14110704,14110706,14110708,14110711,14110713,14110714,14110715,14110716,14110717,14110718,14110719,14112113,14112114,14112115,14112116,14112118,14112120,14112125,14112126,14112127]


with open('runner.sh', 'w') as file:
    for shot in shots:
        print(shot)
        line = str('nohup python iota_vacuum.py ' + 
                   str(shot) + ' ' +
                   '> output/'+str(shot)+'_161_output.txt & \n')
        
        
        
        file.writelines(line)
        
        
"""