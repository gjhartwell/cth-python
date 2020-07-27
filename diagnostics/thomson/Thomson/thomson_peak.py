# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 11:12:52 2017

@author: James
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import leastsq
import thomson_plot as tp
import peakutils


def norm(x, mean, sd):
    norm = []
    for i in range(x.size):
        norm += [1.0/(sd*np.sqrt(2*np.pi))*np.exp(-(x[i] - mean)**2/(2*sd**2))]
    return np.array(norm)


def res(p, y, x):
    m1, m2, a1, a2, sd1, sd2, off = p
    
    y_fit = a1 * norm(x, m1, sd1) + a2 * norm(x, m2, sd2) + off
    err = y - y_fit
    return err


def thomson_find_peak(shot):
    time, data = tp.get_pmt_data_smooth2(shot)
    index = peakutils.indexes(data)
    
    return time, data, index
    
    
def raman_two_gaussian_fit(shot):
    time, data, index = thomson_find_peak(shot)
    time_step = (time[1] - time[0]) * 2000
    # Starting Values
    center1, center2 = time[index[0]], time[index[1]]
    scale1, scale2 = data[index[0]], data[index[0]]
    offset = data[0]
    stand_dev1, stand_dev2 = 1, 1
    parameters = [center1, center2, scale1, scale2, stand_dev1, stand_dev2, 
                  offset]
    p = parameters
    
    x = time
    y_real = data
    #y_init = p[2] * norm(x, p[0], p[4]) + p[3] * norm(x, p[1], p[5]) + p[6]
    
    plsq = leastsq(res, p, args = (y_real, x))
    
    y_est = (plsq[0][6] + plsq[0][2] * norm(x, plsq[0][0], plsq[0][4]) 
                   + plsq[0][3] * norm(x, plsq[0][1], plsq[0][5]))
    
    data_fit = y_est
    
    return time, data, data_fit, plsq
   

def raman_get_individual_gaussians(shot):
    time, data, data_fit, plsq = raman_two_gaussian_fit(shot)
    x = time
    
    g1 = plsq[0][2] * norm(x, plsq[0][0], plsq[0][4]) + plsq[0][6]
    g2 = plsq[0][3] * norm(x, plsq[0][1], plsq[0][5]) + plsq[0][6]

    return time, data, data_fit, g1, g2


def raman_integrate_gaussians(shot):
    time, data, data_fit, plsq = raman_two_gaussian_fit(shot)
    x = time
    
    g1 = plsq[0][2] * norm(x, plsq[0][0], plsq[0][4])
    g2 = plsq[0][3] * norm(x, plsq[0][1], plsq[0][5])

        
    integral1 = sum(g1)
    integral2 = sum(g2)
    
    time_step = (time[1] - time[0])
    return integral1, integral2, time_step

    
    

#print(thomson_integrate_gaussians(17081682))    
    

plt.figure()

tp.plot_pmt(17091682, 'r')
time, data, data_fit, g1, g2 = raman_get_individual_gaussians(17091682)
    

plt.plot(time, data, label = 'Smoothed Data')
plt.plot(time, data_fit, label = 'Fitted Data')   
#plt.plot(time, g1, label = 'First')
#plt.plot(time, g2, label = 'Second')
plt.title(str('Shot: 17081682 \n Processed Data'))
plt.xlabel('Time (ns)')
plt.ylabel('Electrons Detected')

plt.legend()
plt.show()     


