# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 22:37:37 2018

@author: James Kring
@email:  jdk0026@auburn.edu
"""
from vmec import wout_file
from pathlength import Pathlength2D
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

# =============================================================================
# Purpose: Given a particular wout file and toroidal location (phi) find the 
# pathlengths given the viewing chords. Thses pathlengths are then inverted 
# with the chord values to give the profile in flux coordinates.:
# 
#     Note: The Moore–Penrose inverse (np.linalg.pinv) is used to invert the 
#     non-square length matrix.
#     
# To Do: Test this with actual data.
# ============================================================================



class InvertChords:
    
    def __init__(self, wout_filename, phi_location, chords, chord_values, pad=0):
        self.wout = wout_filename
        self.phi = phi_location #toroidal component
        self.chords = chords
        self.chord_values = chord_values
    
        self.pad = pad        
        self.inv_values, self.s = self.get_inverted_values()
        self.get_smoothed_values()
        
    
    def get_inverted_values(self):
        self.length_matrix, s = self.get_pathlengths()
        
        
        self.inv_length_matrix = np.linalg.pinv(self.length_matrix)

        inv_values = np.dot(self.inv_length_matrix, self.chord_values)
        
        return inv_values, s

    def get_smoothed_values(self):
        fsf_order = 2
        fsf_win = len(self.inv_values)//3

        if fsf_win % 2==0:
            fsf_win += 1
        if fsf_order >= fsf_win:
            fsf_order = fsf_win-1      
            
        
        self.inv_values[-1] = (self.inv_values[-1] + self.inv_values[-2])/2

        self.sm_inv_flux = savgol_filter(self.inv_values,fsf_win, fsf_order)
        self.sm_inv_flux2 = savgol_filter(self.sm_inv_flux,fsf_win, fsf_order)  
        
        
        
        scale = np.mean(self.inv_values/self.sm_inv_flux2)
        
        #plt.figure()
        #plt.plot(self.inv_values, 'k')
        #plt.plot(self.sm_inv_flux, 'r')
        #plt.plot(self.sm_inv_flux2, 'b')
        
        #scale = max(self.inv_values)/max(self.sm_inv_flux2)
        
        self.inv_values = scale*self.sm_inv_flux2
        return
    
    
    def get_pathlengths(self):
        vmec1 = wout_file(self.wout)
        R, Z = vmec1.get_flux_surfaces_at_phi_cyl(self.phi)
        
        self.R, self.Z = R,Z#self.pad_flux_surfaces(R, Z)
        
        paths = Pathlength2D(self.R, self.Z)
        
        
        length_matrix = paths.multi_pathlength(self.chords)
     
        #s = np.linspace(vmec1.s_half[0], vmec1.s_half[-1],len(self.R)-1)
        s = vmec1.s_half
        
        
        return length_matrix, s
    
    
    def pad_flux_surfaces(self,R, Z):
        pad = self.pad
        dif_R = []
        for ii in range(0, len(R)-1):
            dif = np.array(R[ii+1])-np.array(R[ii])
            dif_R.append(dif.tolist())
        
        dif_Z = []
        for jj in range(0, len(Z)-1):
            dif = np.array(Z[ii+1])-np.array(Z[ii])
            dif_Z.append(dif.tolist())
        
        
        
        new_R =[]
        new_R.append(R[0].tolist())
        new_Z =[]
        new_Z.append(Z[0].tolist())
        for kk in range(len(R)-1):
            for ll in range(pad):
                n_R = np.array(R[kk]) + (np.array(dif_R[kk])/(pad+1) * (ll+1))
                new_R.append(n_R.tolist())
                n_Z = np.array(Z[kk]) + (np.array(dif_Z[kk])/(pad+1) * (ll+1))
                new_Z.append(n_Z.tolist())
            
            new_R.append(R[kk+1].tolist())
            new_Z.append(Z[kk+1].tolist())
    

        return np.array(new_R), np.array(new_Z)

