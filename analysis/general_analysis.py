# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 14:41:12 2020

@author: James Kring
@email:  jdk0026@auburn.edu
"""

import numpy as np
from scipy.signal import savgol_filter, find_peaks, find_peaks_cwt
from scipy.linalg import svd
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.offsetbox import AnchoredText
import matplotlib.ticker as mticker

class Analysis:
    def __init__(self):
        self.info = {}

    def find_closest_index(self, array, value):
        new_array = abs(array - value)
        try:
            index = new_array.argmin()
        except:
            print('Invalid Array')
            index = 0
                
        return int(index)
        
    def svd(self, data, modes_to_keep=[0,10]):
        
        U, s, VT = svd(data)
        s_zeros = np.zeros(s.shape)
    
    
        weight_kept = sum(s[modes_to_keep[0]:modes_to_keep[1]])/sum(s)
        
        
        n_data = self.return_svd_data(U, s, VT, data.shape, modes_to_keep[0], modes_to_keep[1])
        #s_zeros[modes_to_keep[0]:modes_to_keep[1]] = s[modes_to_keep[0]:modes_to_keep[1]]
        
        #sigma = np.zeros((data.shape[0], data.shape[1]))
        #sigma[:data.shape[0], :data.shape[0]] = np.diag(s_zeros)
        
        #n_data = U.dot(sigma.dot(VT))
        
        
        self.info['U'] = U
        self.info['s'] = s
        self.info['VT'] = VT
        
        self.info['svd filtered data'] = n_data
        self.info['svd weight kept'] = weight_kept
        self.info['svd mode strength'] = s # array of strengths for all the modes
        
        return n_data
    
    
    def return_svd_data(self, U, s, VT, shape, lower_bound, upper_bound):
        s_zeros = np.zeros(s.shape)
        s_zeros[lower_bound:upper_bound] = s[lower_bound:upper_bound]
        
        sigma = np.zeros((shape[0], shape[1]))
        sigma[:shape[0], :shape[0]] = np.diag(s_zeros)
        
        n_data = U.dot(sigma.dot(VT))        
        return n_data
    
    
    def analyze_disruption_btheta(self,
                                  btheta_fluc, btheta_time, 
                                  start_time, stop_time,
                                  time_step, time_window):
        # Function to take a SVD in each time window leading up to a disruptions
        # tracks relative and total energies, peaks in the spatial modes (topos)
        # M number of topos, 
        n_modes_to_analyze = 5
        n_steps = int((stop_time - start_time)/time_step)
        
        print(n_steps)
        times = []
        times_arr = []
        n_btheta03 = []
        n_btheta35 = []
        energies = []
        relative_energies = []
        vt_freq = []
        m_numbers = []
        sigmas = []
        
        for kk in range(0, n_steps):
            time1 = start_time+(kk*time_step)-(.5*time_window)
            time2 = start_time+(kk*time_step)+(.5*time_window)
            times.append([time1, time2])
            ts1 = self.find_closest_index(btheta_time, time1)
            ts2 = self.find_closest_index(btheta_time, time2)
            times_arr.append(btheta_time[ts1:ts2])
            n_btheta_fluc2 = self.svd(btheta_fluc[:,ts1:ts2],modes_to_keep=[3,5])
            n_btheta_fluc1 = self.svd(btheta_fluc[:,ts1:ts2],modes_to_keep=[0,3])
            
            n_btheta03.append(n_btheta_fluc1)
            n_btheta35.append(n_btheta_fluc2)
            
            E = np.sum(self.info['s']*self.info['s'])
            energies.append(E)
            
            sub_rel_en = []
            sub_sigma  = []
            sub_m_num  = []
            sub_vt_freq= []
            
            for jj in range(0, n_modes_to_analyze):
                sub_sigma.append(self.info['s'][jj])
                sub_rel_en.append((self.info['s'][jj]**2)/E)
    
                positive_peaks = self.find_peaks(self.info['U'].T[jj])
                negative_peaks = self.find_peaks(-1*self.info['U'].T[jj])
                
                sub_m_num.append(np.argmax(np.bincount([len(positive_peaks), len(negative_peaks)])))

                t_fft, t_freq, x, N = self.fft_signal(self.info['VT'][jj],time_array=btheta_time[ts1:ts2])

                max_freq = t_freq[np.abs(t_fft).argmax()]
                sub_vt_freq.append(max_freq)
                
            relative_energies.append(sub_rel_en)
            vt_freq.append(sub_vt_freq)
            m_numbers.append(sub_m_num)
            sigmas.append(sub_sigma)
            
        self.info['svd btheta03'] = np.array(n_btheta03)
        self.info['svd btheta35'] = np.array(n_btheta35)
        self.info['svd times'] = np.array(times)
        self.info['svd times array'] = np.array(times_arr)
        self.info['svd energies'] = np.array(energies)
        self.info['svd relative energies'] = np.array(relative_energies)
        self.info['svd vt frequencies'] = np.array(vt_freq)
        self.info['svd m numbers'] = np.array(m_numbers)
        self.info['svd sigmas'] = np.array(sigmas)
        return
        
    def summarize_disruption_btheta(self,                                  
                                    btheta_fluc, btheta_time, 
                                    dis_time):
        self.analyze_disruption_btheta(btheta_fluc, btheta_time,
                                       dis_time-.020, dis_time-.00025,
                                       0.00025, 0.001)
        
        # Tracking m-numbers over three time windows 
        # 1) t_dis - 20ms: t_dis - 10ms
        # 2) t_dis - 10ms: t_dis - 0ms
        # 3) t_dis - 5ms : t_dis - 0ms
        m03_tm20_10 = np.mean(self.info['svd m numbers'][:39,0:3])
        m03_tm10_0  = np.mean(self.info['svd m numbers'][39:,0:3])
        m03_tm5_0   = np.mean(self.info['svd m numbers'][59:,0:3])
        
        m35_tm20_10 = np.mean(self.info['svd m numbers'][:39,3:5])
        m35_tm10_0  = np.mean(self.info['svd m numbers'][39:,3:5])
        m35_tm5_0   = np.mean(self.info['svd m numbers'][59:,3:5])
        
        # Tracking singular values (sigmas) over three time windows 
        # 1) t_dis - 20ms: t_dis - 10ms
        # 2) t_dis - 10ms: t_dis - 0ms
        # 3) t_dis - 5ms : t_dis - 0ms       
        s03_tm20_10 = np.mean(self.info['svd sigmas'][:39,0:3])
        s03_tm10_0  = np.mean(self.info['svd sigmas'][39:,0:3])
        s03_tm5_0   = np.mean(self.info['svd sigmas'][59:,0:3])
        
        s35_tm20_10 = np.mean(self.info['svd sigmas'][:39,3:5])
        s35_tm10_0  = np.mean(self.info['svd sigmas'][39:,3:5])
        s35_tm5_0   = np.mean(self.info['svd sigmas'][59:,3:5])   
        
        # Fitting singular values (sigmas) to find growth rates 
        # over two time windows 
        # 1) t_dis - 20ms: t_dis - 10ms
        # 2) t_dis - 10ms: t_dis - 0ms        
        # Returns fit for f(a,b,t) = a*exp(b*t)
        # Returns in form: [[a,b], [del_a, del_b],timeoffset]
        sfit_tm10_0 = self.sigma_mode_growth(np.mean(self.info['svd times'][39:],axis=1),
                                             self.info['svd sigmas'][39:,0:3])[0][1]
        sfit_tm5_0  = self.sigma_mode_growth(np.mean(self.info['svd times'][59:],axis=1),
                                             self.info['svd sigmas'][59:,0:3])[0][1]
 
        # Tracking real data from first 3 modes over three time windows 
        # 1) t_dis - 20ms: t_dis - 10ms
        # 2) t_dis - 10ms: t_dis - 0ms
        # 3) t_dis - 5ms : t_dis - 0ms       
        sd03_tm20_10 = self.get_mode_ave_and_sum(self.info['svd times array'][:39],
                                                 self.info['svd btheta03'][:39])
        sd03_tm10_0  = self.get_mode_ave_and_sum(self.info['svd times array'][39:],
                                                 self.info['svd btheta03'][39:])        
        sd03_tm5_0   = self.get_mode_ave_and_sum(self.info['svd times array'][59:],
                                                 self.info['svd btheta03'][59:])    

        # Tracking real data from modes 3,4 over three time windows 
        # 1) t_dis - 20ms: t_dis - 10ms
        # 2) t_dis - 10ms: t_dis - 0ms
        # 3) t_dis - 5ms : t_dis - 0ms       

        sd35_tm20_10 = self.get_mode_ave_and_sum(self.info['svd times array'][:39],
                                                 self.info['svd btheta35'][:39])
        sd35_tm10_0  = self.get_mode_ave_and_sum(self.info['svd times array'][39:],
                                                 self.info['svd btheta35'][39:])        
        sd35_tm5_0   = self.get_mode_ave_and_sum(self.info['svd times array'][59:],
                                                 self.info['svd btheta35'][59:])    
        
        # Tracking frequencies over three time windows 
        # 1) t_dis - 20ms: t_dis - 10ms
        # 2) t_dis - 10ms: t_dis - 0ms
        # 3) t_dis - 5ms : t_dis - 0ms       
        f03_tm20_10 = np.mean(self.info['svd vt frequencies'][:39,0:3])
        f03_tm10_0  = np.mean(self.info['svd vt frequencies'][39:,0:3])
        f03_tm5_0   = np.mean(self.info['svd vt frequencies'][59:,0:3])
        
        f35_tm20_10 = np.mean(self.info['svd vt frequencies'][:39,3:5])
        f35_tm10_0  = np.mean(self.info['svd vt frequencies'][39:,3:5])
        f35_tm5_0   = np.mean(self.info['svd vt frequencies'][59:,3:5])

        self.info['btheta m numbers'] = np.array([m03_tm20_10, m03_tm10_0, m03_tm5_0,
                                                 m35_tm20_10, m35_tm10_0, m35_tm5_0])
        self.info['btheta sigmas'] = np.array([s03_tm20_10, s03_tm10_0, s03_tm5_0,
                                              s35_tm20_10, s35_tm10_0, s35_tm5_0])
        self.info['btheta frequencies'] = np.array([f03_tm20_10, f03_tm10_0, f03_tm5_0,
                                                   f35_tm20_10, f35_tm10_0, f35_tm5_0])  
        self.info['btheta growth'] = np.array([sfit_tm10_0, sfit_tm5_0])
        self.info['btheta real ave'] = np.array([sd03_tm20_10[0], sd03_tm10_0[0], sd03_tm5_0[0],
                                                 sd35_tm20_10[0], sd35_tm10_0[0], sd35_tm5_0[0]])
        self.info['btheta real sum'] = np.array([sd03_tm20_10[1], sd03_tm10_0[1], sd03_tm5_0[1],
                                                 sd35_tm20_10[1], sd35_tm10_0[1], sd35_tm5_0[1]])

        return
    
    def analyze_disruption_sxr(self,
                                  sxr_fluc, sxr_time, 
                                  start_time, stop_time,
                                  time_step, time_window):
        # Function to take a SVD in each time window leading up to a disruptions
        # tracks relative and total energies, peaks in the spatial modes (topos)
        # M number of topos, 
        n_modes_to_analyze = 3
        n_steps = int((stop_time - start_time)/time_step)
        
        
        times = []
        energies = []
        relative_energies = []
        vt_freq = []
        sigmas = []
        
        for kk in range(0, n_steps):
            time1 = start_time+(kk*time_step)-(.5*time_window)
            time2 = start_time+(kk*time_step)+(.5*time_window)
            times.append([time1, time2])
            ts1 = self.find_closest_index(sxr_time, time1)
            ts2 = self.find_closest_index(sxr_time, time2)
            
            n_sxr_fluc = self.svd(sxr_fluc[:,ts1:ts2])
            
            E = np.sum(self.info['s']*self.info['s'])
            energies.append(E)
            
            sub_rel_en = []
            sub_sigma  = []
            sub_vt_freq= []
        
            for jj in range(0, n_modes_to_analyze):
                sub_sigma.append(self.info['s'][jj])
                sub_rel_en.append((self.info['s'][jj]**2)/E)
                
                t_fft, t_freq, x, N = self.fft_signal(self.info['VT'][jj],time_array=sxr_time[ts1:ts2])

                max_freq = t_freq[np.abs(t_fft).argmax()]
                sub_vt_freq.append(max_freq)
                #positive_peaks = self.find_peaks(self.info['U'].T[jj])
                #negative_peaks = self.find_peaks(-1*self.info['U'].T[jj])
                
                #sub_m_num.append(np.argmax(np.bincount([len(positive_peaks), len(negative_peaks)])))
                
            relative_energies.append(sub_rel_en)
            vt_freq.append(sub_vt_freq)
            sigmas.append(sub_sigma)
            
        self.info['svd times'] = np.array(times)
        self.info['svd energies'] = np.array(energies)
        self.info['svd relative energies'] = np.array(relative_energies)
        self.info['svd vt frequencies'] = np.array(vt_freq)
        self.info['svd sigmas'] = np.array(sigmas)
        return            


    def sigma_mode_growth(self, time, svd_sigmas):
        def exp_func(x, a, b):
            y = a*np.exp(b*(x))
            return y
        
        px1 = np.ndarray.flatten(np.concatenate([time, time, time]))
        py2 = np.ndarray.flatten(np.concatenate(svd_sigmas))

        arr1inds = px1.argsort()
        px2 = px1[arr1inds]
        py3 = py2[arr1inds]
        
        time_offset = np.mean(px2)
        
        px3 = px2 - time_offset
        try:
            popt, pcov = curve_fit(exp_func, px3, py3)
            perr = np.sqrt(np.diag(pcov))
        except:
            popt = [np.nan, np.nan]
            perr = [np.nan, np.nan]
            
        return np.array([popt.tolist(), perr.tolist(), time_offset])


    def get_mode_amplitudes(self, times, datas):
        
        p_times = []
        p_data  = []

        for ii in range(0, len(times)):
            #peaks = find_peaks(abs(datas[ii]))[0]
            
            p_data.append(abs(datas[ii]))#[peaks]))
            p_times.append(times[ii])#[peaks])
        
        p_times = np.array(p_times)
        p_data = np.array(p_data)
        #print(p_times.shape, p_data.shape)
           
        p_times = np.ndarray.flatten(np.concatenate(p_times))
        p_data  = np.ndarray.flatten(np.concatenate(p_data))
        #print(p_times.shape, p_data.shape)
        pind = p_times.argsort()
        p_times2 = p_times[pind]
        p_data2  = p_data[pind]        
        
        return p_times2, p_data2
        
    
    def get_mode_ave_and_sum(self, times, datas):
        #print(times.shape, datas.shape)
        ave_list = []
        sum_list = []
        for ii in range(len(datas[0])):
            n_times, n_datas = self.get_mode_amplitudes(times, datas[:,ii,:])
            ave_list.append(np.mean(n_datas))
            sum_list.append(np.sum(n_datas))
            
        ave = np.mean(ave_list)
        sums= np.sum(sum_list)
        return ave, sums
    
        
    def mode_growth(self, time, svd_temp):
        def exp_func(x, a, b):
            y = a*np.exp(b*(x))
            return y
        
        peaks = find_peaks(abs(svd_temp))[0]
        
        px1 = time[peaks]
        py1 = svd_temp[peaks] 
        
        max_ind = py1.argmax()
        
        time_offset = np.mean(px1)
        
        px2 = px1[:max_ind] - time_offset
        py2 = py1[:max_ind]
        
        try:
            popt, pcov = curve_fit(exp_func, px2, py2)
            perr = np.sqrt(np.diag(pcov))
        except:
            popt = [np.nan, np.nan]
            perr = [np.nan, np.nan]
            
        return [popt, perr, time_offset]
    
    
    def max_two(self, array):
        id1 = array.argmax()
        array2 = np.delete(array, id1)
        id2 = array2.argmax()
        return [id1,id2]
    
    def find_peaks(self, data):
        min1 = abs(data).argmin()
        data2 = data.tolist()[min1-2:] + data.tolist()[:min1+2]
        data2 = np.array(data2)
        x2 = np.linspace(1, len(data2), len(data2))
        x3 = np.linspace(1, len(data2), len(data2)*20)
        dfunc = interp1d(x2, data2,kind='cubic')
        
        data3 = dfunc(x3)
        #data2 = savgol_filter(data2, 5, 2)
        peaks = find_peaks(data2,width=2,distance=4)
        return peaks[0]
      
    def ind_check(self,id1,id2, val):
        s_check = (id1 <= id2 + val and id1 >= id2 - val)
        return s_check
        
    
    def flucs(self, data):
        s_data, f_data = [], []
        
        
        for channel in data:
            smooth_channel = savgol_filter(channel, 151, 0)
            s_data.append(smooth_channel)
            f_data.append(channel - smooth_channel)
            
            
        self.info['smooth data'] = s_data
        self.info['fluc data'] = f_data
        
        return f_data
    
        
    def subtract_cameras(self, camera1, camera2):
        sub_cam = []
        
        for jj, channel in enumerate(camera1):
            sub_cam.append(channel - camera2[jj])
            
        return sub_cam


    def plot_camera(self, time_array, data, time=[1.62, 1.70],
                    save=False, save_dir='',title='', cbar_label=None,
                    if_y_channels=False, y_channels=None):
        
        id1 = self.find_closest_index(time_array,time[0])
        id2 = self.find_closest_index(time_array,time[1])
        cmap1='gnuplot2'
        if if_y_channels:
            channels = y_channels 
            plt.yticks(y_channels,fontsize=13,weight='bold')   
        else:
            channels = np.linspace(1,len(data),len(data)).tolist()
            plt.yticks([1, 5, 10, 15, 20], fontsize=13,weight='bold')   
            
        plt.contourf(time_array.tolist()[id1:id2],channels,np.array(data)[:,id1:id2],cmap=cmap1)
        plt.title(title,fontsize = 15, weight ='bold')
        plt.xlabel('Time (sec)',fontsize = 15, weight ='bold')
        plt.ylabel('Channel',fontsize = 15, weight ='bold')
        plt.xticks(fontsize=13,weight='bold')
        #plt.yticks([1, 5, 10, 15, 20], fontsize=13,weight='bold')   
        plt.gca().invert_yaxis()
        plt.locator_params(axis='x', nbins=5)
        
        cbar = plt.colorbar()
        labels = [item.get_text() for item in cbar.ax.get_yticklabels()]
        cbar.ax.set_yticklabels(labels,fontsize=13, weight='bold')
        
        if cbar_label:            
            cbar.set_label(cbar_label, rotation=270,fontsize=13, weight='bold', labelpad=15)
        else:
            cbar.set_label('Relative Intensity', rotation=270,fontsize=13, weight='bold',labelpad=-15)

        if save:
            filename = str(save_dir+'_.png')
            plt.savefig(filename, format='png', dpi = 1000,  bbox_inches='tight')
            plt.close()
   
    
    def interp_and_find(self, x, y, value_to_find):    
        x_i = np.linspace(x[0], x[-1],len(x)*20)

        y_i = [np.interp(x_i, x, y_chan) for y_chan in y]

        ind = [self.find_closest_index(y_i_row, value_to_find) for y_i_row in y_i]
    
        x_p = [x_i[ind_t]  for ii, ind_t in enumerate(ind)]# if (value_to_find*.8 <= y_i[ii][ind_t] <= value_to_find*1.2)]
        y_p = [y_i[ii][ind_t]  for ii, ind_t in enumerate(ind)]# if (value_to_find*.8 <= y_i[ii][ind_t] <= value_to_find*1.2)]
    
        x_p = [x_p1 if (x_p1 != x_i[-1] and x_p1 != x_i[0]) else np.nan for x_p1 in x_p]
    
        return x_p#, y_p    
    
    
    def find_edge(self, camera, num_of_zones=1, edge_fraction=.1):
        t_camera = camera.transpose()
        x = np.linspace(1, len(camera), len(camera))
        #print(t_camera.shape)
        edge_value = max([max(row) for row in t_camera]) * edge_fraction
    
        edge = []
    
        if num_of_zones==1:
            t1 = t_camera
            x1 = x
        
            edge.append(self.interp_and_find(x1, t1, edge_value))        
        
        elif num_of_zones==2:
            t1 = t_camera[:,:11]
            t2 = t_camera[:,10:]
        
            x1 = x[:11]
            x2 = x[10:]
            
            edge.append(self.interp_and_find(x1, t1, edge_value))  
            edge.append(self.interp_and_find(x2, t2, edge_value))  
 
        elif num_of_zones==4:
            t1 = t_camera[:,:6]
            t2 = t_camera[:,5:11]
            t3 = t_camera[:,10:16]
            t4 = t_camera[:,15:]
        
            x1 = x[:6]
            x2 = x[5:11]       
            x3 = x[10:16]      
            x4 = x[15:]
        
            edge.append(self.interp_and_find(x1, t1, edge_value))  
            edge.append(self.interp_and_find(x2, t2, edge_value))  
            edge.append(self.interp_and_find(x3, t3, edge_value))  
            edge.append(self.interp_and_find(x4, t4, edge_value))  
  

        return edge    
    
    
    
    def fft_signal(self, signal, time_array=None):
        N = len(signal)
        x = np.linspace(0, 1, N)
        #freq = np.linspace(0, 1/(x[1] - x[0]), N)


        if np.array(time_array).any():
            dT = time_array[-1] - time_array[0]            
            freq = np.fft.rfftfreq(N)#, d=1/(time_array[1]-time_array[0]))
            freq = (freq*N)/dT
        else:
            freq = np.fft.rfftfreq(N)
            
            
        fft = np.fft.rfft(signal)
        fft = (fft*1/N)
        return fft, freq, x, N
    
    
    def filter_signal(self, signal, time_array=None, noise_fft_bounds=[0, 10]):
        id1 = noise_fft_bounds[0]
        id2 = noise_fft_bounds[1]
        #dT = time_array[-1] - time_array[0]

        if time_array.any():
            fft, freq, x, N = self.fft_signal(signal, time_array=time_array)  
        else:
            fft, freq, x, N = self.fft_signal(signal)
            
        #freq = (freq*N)/dT
        n_fft = np.zeros(fft.shape,dtype=np.complex_)
        n_freq= np.zeros(freq.shape)

        n_fft[id1:id2] = fft[id1:id2]
        n_freq[id1:id2] = freq[id1:id2]
        
        cutoff = [freq[id1], freq[id2]]
        filtered_data = np.fft.irfft(n_fft)

        return filtered_data, cutoff, n_fft, freq
    
    
    def filter_cammera(self, time_array, camera, noise_fft_bounds = [0,10]):
        filtered_camera =[]
        n_fft_array = []
        
        for channel in camera:
            filtered_channel, cutoff, n_fft, n_freq = self.filter_signal(channel, time_array=time_array, noise_fft_bounds=noise_fft_bounds)
            filtered_camera.append(filtered_channel)
            n_fft_array.append(abs(n_fft))
        
        self.info['fft cutoff'] = cutoff
        self.info['filtered camera'] = np.array(filtered_camera)
        self.info['fft spectrum'] = sum(n_fft_array)
        self.info['fft freq'] = n_freq

        return np.array(filtered_camera)
        
    
    def keep_freq(self, time_array, camera, freqs_to_keep = [0,12], freq_half_window=1):
        max_freq = len(time_array)//2 - 1
        noise_fft_bounds =[0, max_freq]

        filtered_channel, cutoff, n_fft, n_freq = self.filter_signal(camera[0], time_array=time_array, noise_fft_bounds=noise_fft_bounds)
        
        start_ind = []
        stop_ind = []
        
        for freq in freqs_to_keep:
            start_ind.append(self.find_closest_index(n_freq, freq-freq_half_window))
            stop_ind.append(self.find_closest_index(n_freq, freq+freq_half_window)+1)
            
        print(start_ind, stop_ind)
            
        filtered_camera =[]
        n_fft_array = []
        
        for channel in camera:
            filtered_channel = np.zeros(len(filtered_channel))
            n_fft = np.zeros(len(n_fft))
            cutoff = []
            
            for ii in range(len(freqs_to_keep)):
                sub_filtered_channel, sub_cutoff, sub_n_fft, n_freq = self.filter_signal(channel, 
                                                                                 time_array=time_array, 
                                                                                 noise_fft_bounds=[start_ind[ii], stop_ind[ii]])

                filtered_channel = filtered_channel + sub_filtered_channel

                n_fft = n_fft + sub_n_fft
                cutoff.append(sub_cutoff)
            
            filtered_camera.append(filtered_channel)
            n_fft_array.append(abs(n_fft))         
        
        self.info['filtered camera'] = np.array(filtered_camera)
        self.info['fft spectrum'] = sum(n_fft_array)
        self.info['fft ind spectrum'] = n_fft_array
        self.info['fft cutoff'] = cutoff        
        self.info['fft freq'] = n_freq
        
        return np.array(filtered_camera)
        
    
    def plot_fft(self, freq, amplitude, cutoff, scale=None, title=''):        
        min_x = round(min([min(row) for row in cutoff])/1000, 0) - .5
        max_x = round(max([max(row) for row in cutoff])/1000, 0) + .5
        
        
        plt.xticks(fontsize=13,weight='bold')
        plt.yticks(fontsize=13,weight='bold')      
        
        plt.title(title,fontsize = 15, weight ='bold')        
        
        if scale:
            plt.yscale(scale) # 'linear'
        else:    
            plt.yscale('log')        
        
        plt.xlabel('Frequency (kHz)',fontsize = 15, weight ='bold')
        plt.ylabel('Amplitude',fontsize = 15, weight ='bold') 
        plt.xlim([-.5, max_x])
        
        plt.bar(freq/1000, amplitude, color='r', width=.5, edgecolor='k')
        
        return
        
    def plot_ip_and_density(self,ip, density, 
                            title=None, anchored_shot=None, time_line=None):
        # ip = [ip.time, ip.data]
        # density = [density.time, density.data]
        f = mticker.ScalarFormatter(useOffset=False, useMathText=True)
        g = lambda x,pos : "${}$".format(f._formatSciNotation('%1.1e' % x))
        font = {'weight' : 'bold',
                'size'   : 13}

        rc('font', **font)
        #fig, ax1 = plt.subplots()
        ax1 = plt.gca()
        color = 'k'

        ax1.set_xlabel('Time (s)',fontsize = 15, weight ='bold')
        ax1.set_ylabel('Curernt (kA)',fontsize = 15, weight ='bold')
        ax1.plot(ip[0], ip[1]/1000, color=color)
        ax1.set_xlim(1.62, 1.66)

        ax1.tick_params(axis='y', labelcolor = color)
        #ax1.set_xticklabels(ax1.get_xticks(), {'weight' : 'bold', 'size' : 13})
        ax1.set_ylim(bottom=0)
        ax1.set_yticklabels(ax1.get_yticks(), {'weight' : 'bold', 'size' : 13})

        ax2 = ax1.twinx()
        plt.yticks(fontsize=13,weight='bold')
    
        color = 'r'
    
        ax2.set_ylabel(str('Density ('+r'$m^{-3}$' +')'),color=color,fontsize = 15, weight ='bold')

        ax2.plot(density[0], density[1],color=color)
        ax2.tick_params(axis='y', labelcolor=color)
        ax2.set_ylim(bottom=0)

        ax2.set_yticklabels(ax2.get_yticks(),{'weight' : 'bold', 'size' : 13})
        ax2.yaxis.set_major_formatter(mticker.FuncFormatter(g))
    
        if title:
            plt.title(title,fontsize = 15, weight ='bold')
        else:
            title = str('Plasma Current and Density')
            #plt.title(title,fontsize = 15, weight ='bold')
            
        if anchored_shot:
            anchored_text = AnchoredText(str('Shot: ' + str(anchored_shot)),prop=font,
                                        loc=2, frameon=False)

            ax1.add_artist(anchored_text)   
            
        if time_line:
            ax1.axvline(x=time_line,color='b',linestyle='--', linewidth=2)            
            
            
        plt.tight_layout()        
        
        
        
    