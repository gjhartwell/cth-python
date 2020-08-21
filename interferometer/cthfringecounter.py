# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 09:26:33 2020

@author: hartwgj
"""

import numpy as np

def cthfringecounter(phase):

    length = len(phase)
    
    threshold = 3.0
    corrected_phase = np.arange(length)
    
    fringes = 0.0
    
    for p in range(length-1):
        if (phase[p+1]-phase[p]) > threshold: 
            fringes+=1
        if (phase[p+1]-phase[p]) < -1.0*threshold:
            fringes-=1
        corrected_phase[p] = phase[p] + float(fringes) * (2.0*np.pi)

    return corrected_phase

