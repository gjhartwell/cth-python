# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 09:32:53 2020

@author: James Kring
@email:  jdk0026@auburn.edu



"""

import numpy as np
from cthdata import CTHData


class SXR:
    
    def __init(self, shot):
        self.shot = shot
    
    
    def get_data(self):
        SC252_000_18_1 = CTHData(self.shot, 216, channel_number=True).data*1E6
        SC252_000_18_2 = CTHData(self.shot, 217, channel_number=True).data*1E6
        SC252_000_18_3 = CTHData(self.shot, 218, channel_number=True).data*1E6
        SC252_000_18_4 = CTHData(self.shot, 219, channel_number=True).data*1E6
        SC252_000_18_5 = CTHData(self.shot, 220, channel_number=True).data*1E6
        SC252_000_18_6 = CTHData(self.shot, 221, channel_number=True).data*1E6
        SC252_000_18_7 = CTHData(self.shot, 222, channel_number=True).data*1E6
        SC252_000_18_8 = CTHData(self.shot, 223, channel_number=True).data*1E6
        SC252_000_18_9 = CTHData(self.shot, 224, channel_number=True).data*1E6
        SC252_000_18_10= CTHData(self.shot, 225, channel_number=True).data*1E6
        SC252_000_18_11= CTHData(self.shot, 226, channel_number=True).data*1E6
        SC252_000_18_12= CTHData(self.shot, 227, channel_number=True).data*1E6
        SC252_000_18_13= CTHData(self.shot, 228, channel_number=True).data*1E6
        SC252_000_18_14= CTHData(self.shot, 229, channel_number=True).data*1E6
        SC252_000_18_15= CTHData(self.shot, 230, channel_number=True).data*1E6
        SC252_000_18_16= CTHData(self.shot, 231, channel_number=True).data*1E6
        SC252_000_18_17= CTHData(self.shot, 232, channel_number=True).data*1E6
        SC252_000_18_18= CTHData(self.shot, 233, channel_number=True).data*1E6
        SC252_000_18_19= CTHData(self.shot, 234, channel_number=True).data*1E6
        SC252_000_18_20= CTHData(self.shot, 235, channel_number=True).data*1E6
        
        #Top Camera
        SC252_060_18_1 = CTHData(self.shot, 696, channel_number=True).data
        SC252_060_18_2 = CTHData(self.shot, 697, channel_number=True).data
        SC252_060_18_3 = CTHData(self.shot, 698, channel_number=True).data
        SC252_060_18_4 = CTHData(self.shot, 699, channel_number=True).data
        SC252_060_18_5 = CTHData(self.shot, 700, channel_number=True).data
        SC252_060_18_6 = CTHData(self.shot, 701, channel_number=True).data
        SC252_060_18_7 = CTHData(self.shot, 702, channel_number=True).data
        SC252_060_18_8 = CTHData(self.shot, 703, channel_number=True).data
        SC252_060_18_9 = CTHData(self.shot, 704, channel_number=True).data
        SC252_060_18_10= CTHData(self.shot, 705, channel_number=True).data
        SC252_060_18_11= CTHData(self.shot, 706, channel_number=True).data
        SC252_060_18_12= CTHData(self.shot, 707, channel_number=True).data
        SC252_060_18_13= CTHData(self.shot, 708, channel_number=True).data
        SC252_060_18_14= CTHData(self.shot, 709, channel_number=True).data
        SC252_060_18_15= CTHData(self.shot, 710, channel_number=True).data
        SC252_060_18_16= CTHData(self.shot, 711, channel_number=True).data
        SC252_060_18_17= CTHData(self.shot, 712, channel_number=True).data
        SC252_060_18_18= CTHData(self.shot, 713, channel_number=True).data
        SC252_060_18_19= CTHData(self.shot, 714, channel_number=True).data
        SC252_060_18_20= CTHData(self.shot, 715, channel_number=True).data        
        
        #Bottom Camera
        SC252_300_18_1 = CTHData(self.shot, 736, channel_number=True).data
        SC252_300_18_2 = CTHData(self.shot, 737, channel_number=True).data
        SC252_300_18_3 = CTHData(self.shot, 738, channel_number=True).data
        SC252_300_18_4 = CTHData(self.shot, 739, channel_number=True).data
        SC252_300_18_5 = CTHData(self.shot, 740, channel_number=True).data
        SC252_300_18_6 = CTHData(self.shot, 741, channel_number=True).data
        SC252_300_18_7 = CTHData(self.shot, 742, channel_number=True).data
        SC252_300_18_8 = CTHData(self.shot, 743, channel_number=True).data
        SC252_300_18_9 = CTHData(self.shot, 744, channel_number=True).data
        SC252_300_18_10= CTHData(self.shot, 745, channel_number=True).data
        SC252_300_18_11= CTHData(self.shot, 746, channel_number=True).data
        SC252_300_18_12= CTHData(self.shot, 747, channel_number=True).data
        SC252_300_18_13= CTHData(self.shot, 748, channel_number=True).data
        SC252_300_18_14= CTHData(self.shot, 749, channel_number=True).data
        SC252_300_18_15= CTHData(self.shot, 750, channel_number=True).data
        SC252_300_18_16= CTHData(self.shot, 751, channel_number=True).data
        SC252_300_18_17= CTHData(self.shot, 752, channel_number=True).data
        SC252_300_18_18= CTHData(self.shot, 753, channel_number=True).data
        SC252_300_18_19= CTHData(self.shot, 754, channel_number=True).data
        SC252_300_18_20= CTHData(self.shot, 755, channel_number=True).data
        
        #3.0um filter
        #Middle Camera
        SC252_000_30_1 = CTHData(self.shot, 236, channel_number=True).data*1E6
        SC252_000_30_2 = CTHData(self.shot, 237, channel_number=True).data*1E6
        SC252_000_30_3 = CTHData(self.shot, 238, channel_number=True).data*1E6
        SC252_000_30_4 = CTHData(self.shot, 239, channel_number=True).data*1E6
        SC252_000_30_5 = CTHData(self.shot, 240, channel_number=True).data*1E6
        SC252_000_30_6 = CTHData(self.shot, 241, channel_number=True).data*1E6
        SC252_000_30_7 = CTHData(self.shot, 242, channel_number=True).data*1E6
        SC252_000_30_8 = CTHData(self.shot, 243, channel_number=True).data*1E6
        SC252_000_30_9 = CTHData(self.shot, 244, channel_number=True).data*1E6
        SC252_000_30_10= CTHData(self.shot, 245, channel_number=True).data*1E6
        SC252_000_30_11= CTHData(self.shot, 246, channel_number=True).data*1E6
        SC252_000_30_12= CTHData(self.shot, 247, channel_number=True).data*1E6
        SC252_000_30_13= CTHData(self.shot, 248, channel_number=True).data*1E6
        SC252_000_30_14= CTHData(self.shot, 249, channel_number=True).data*1E6
        SC252_000_30_15= CTHData(self.shot, 250, channel_number=True).data*1E6
        SC252_000_30_16= CTHData(self.shot, 251, channel_number=True).data*1E6
        SC252_000_30_17= CTHData(self.shot, 252, channel_number=True).data*1E6
        SC252_000_30_18= CTHData(self.shot, 253, channel_number=True).data*1E6
        SC252_000_30_19= CTHData(self.shot, 254, channel_number=True).data*1E6
        SC252_000_30_20= CTHData(self.shot, 255, channel_number=True).data*1E6
        
        #Top Camera
        SC252_060_30_1 = CTHData(self.shot, 716, channel_number=True).data   
        SC252_060_30_2 = CTHData(self.shot, 717, channel_number=True).data 
        SC252_060_30_3 = CTHData(self.shot, 718, channel_number=True).data 
        SC252_060_30_4 = CTHData(self.shot, 719, channel_number=True).data 
        SC252_060_30_5 = CTHData(self.shot, 720, channel_number=True).data 
        SC252_060_30_6 = CTHData(self.shot, 721, channel_number=True).data 
        SC252_060_30_7 = CTHData(self.shot, 722, channel_number=True).data 
        SC252_060_30_8 = CTHData(self.shot, 723, channel_number=True).data 
        SC252_060_30_9 = CTHData(self.shot, 724, channel_number=True).data 
        SC252_060_30_10= CTHData(self.shot, 725, channel_number=True).data 
        SC252_060_30_11= CTHData(self.shot, 726, channel_number=True).data 
        SC252_060_30_12= CTHData(self.shot, 727, channel_number=True).data 
        SC252_060_30_13= CTHData(self.shot, 728, channel_number=True).data 
        SC252_060_30_14= CTHData(self.shot, 729, channel_number=True).data 
        SC252_060_30_15= CTHData(self.shot, 730, channel_number=True).data 
        SC252_060_30_16= CTHData(self.shot, 731, channel_number=True).data 
        SC252_060_30_17= CTHData(self.shot, 732, channel_number=True).data 
        SC252_060_30_18= CTHData(self.shot, 733, channel_number=True).data 
        SC252_060_30_19= CTHData(self.shot, 734, channel_number=True).data 
        SC252_060_30_20= CTHData(self.shot, 735, channel_number=True).data         
        
        #Bottom Camera
        SC252_300_30_1 = CTHData(self.shot, 756, channel_number=True).data
        SC252_300_30_2 = CTHData(self.shot, 757, channel_number=True).data
        SC252_300_30_3 = CTHData(self.shot, 758, channel_number=True).data
        SC252_300_30_4 = CTHData(self.shot, 759, channel_number=True).data
        SC252_300_30_5 = CTHData(self.shot, 760, channel_number=True).data
        SC252_300_30_6 = CTHData(self.shot, 761, channel_number=True).data
        SC252_300_30_7 = CTHData(self.shot, 762, channel_number=True).data
        SC252_300_30_8 = CTHData(self.shot, 763, channel_number=True).data
        SC252_300_30_9 = CTHData(self.shot, 764, channel_number=True).data
        SC252_300_30_10= CTHData(self.shot, 765, channel_number=True).data
        SC252_300_30_11= CTHData(self.shot, 766, channel_number=True).data
        SC252_300_30_12= CTHData(self.shot, 767, channel_number=True).data
        SC252_300_30_13= CTHData(self.shot, 768, channel_number=True).data
        SC252_300_30_14= CTHData(self.shot, 769, channel_number=True).data
        SC252_300_30_15= CTHData(self.shot, 770, channel_number=True).data
        SC252_300_30_16= CTHData(self.shot, 771, channel_number=True).data
        SC252_300_30_17= CTHData(self.shot, 772, channel_number=True).data
        SC252_300_30_18= CTHData(self.shot, 773, channel_number=True).data
        SC252_300_30_19= CTHData(self.shot, 774, channel_number=True).data
        SC252_300_30_20= CTHData(self.shot, 775, channel_number=True).data
        
        time = CTHData(self.shot, 716, channel_number=True).time
        
        sxr_diagnostic = np.array([SC252_000_18_1, SC252_000_18_2, SC252_000_18_3, SC252_000_18_4, SC252_000_18_5, SC252_000_18_6, SC252_000_18_7 ,SC252_000_18_8, SC252_000_18_9, SC252_000_18_10,
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
                          ])*.01
        
        return sxr_diagnostic.tolist(), time
    
    
    def average_window(self, data_array, time_array, time, window, absolute=False):
        time = time
        ind1 = self.find_closest_index(time_array, time - window)
        ind2 = self.find_closest_index(time_array, time + window)
        
        ave_data = []
        sig_data = []
        
        for data in data_array:
            if absolute:
                value = np.mean(abs(data[ind1:ind2]))
                sigma = np.std(abs(data[ind1:ind2]),ddof=1)
            else:
                value = np.mean(data[ind1:ind2])
                sigma = np.std(data[ind1:ind2],ddof=1)
            ave_data.append(value)
            sig_data.append(sigma)
        
        
        return ave_data, sig_data
    
    
    
    
    
sxr = SXR(20021052)

data, time =sxr.get_data()

ave_data, ave_sig = sxr.average_window(data, time, 1.64, 0.001)


plt.figure()
plt.plot(ave_data, 'k')
    
    
    
    
    