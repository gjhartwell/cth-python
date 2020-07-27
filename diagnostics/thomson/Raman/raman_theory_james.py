# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 15:33:26 2018

@author: James Kring
jdk0026@auburn.edu
"""

import numpy as np
import matplotlib.pyplot as plt


B_N2 = 2.48*10**-4
gamma_sq_N2 = 0.395*10**-82
L_det_1 = .0142             


def collection_optics_solid_angle(length_to_lens, radius_of_lens):
    # The solid angle that is collected by the collection 
    # optics. length_to_lens is the distance from the scattering volume to the
    # location of the collection lens. radius_of_lens is the radius of the 
    # collection lens
    value = 2*np.pi*(1-np.cos(np.arctan(radius_of_lens/length_to_lens)))
    
    return value


def laser_photons(E_pulse, laser_wavelength):
    h = 6.626*10**-34
    c = 3*10**8     
    value = E_pulse * (laser_wavelength/(h * c))
    return value


def raman_wavelength(J, laser_wavelength, B):
    h = 4.1357*10**-15
    c = 3*10**8    
    l = laser_wavelength

    l_raman = l + ((l **2)/(h * c)) * B * (4*J + 6)
    
    return l_raman
    

def raman_crosssection(J, laser_wavelength, B, gamma_sq):
    e0 = 8.854*10**-12
    l_raman = raman_wavelength(J, laser_wavelength, B)
    
    c1 = (64*np.pi**4)/45
    c2 = (3 * (J+1) * (J+2))/(2 * (2*J+1) * (2*J+3))
    
    crosssection = c1/(e0**2) * c2 * ((gamma_sq)/l_raman**4)
    
    return crosssection


def raman_gJ(J):
    if (J % 2) == 0:
        value = 6
    else:
        value = 3
           
    return value


def raman_EJ(J, B):
    EJ = B* J*(J+1)

    return EJ
    

def raman_J_density(J, B, pressure, temperature):
    kB= 1.38*10**-23
    P = pressure * 133.3224
    T = temperature/11604
    n = P/(kB * T *11604)    
    
    Q = 0
    for j in range(1,50):
        value =  raman_gJ(j) * (2*j+1) * np.exp(-raman_EJ(j, B)/(T))

        Q = Q + value
     
    nJ = (n/Q) * raman_gJ(J)* (2*J+1)*np.exp(-raman_EJ(J, B)/(T))    
    
    return nJ


def raman_photons(E_pulse, laser_wavelength, B, gamma_sq, pressure,
                  temperature, L_det, length_to_lens, radius_of_lens):
    
    n_laser = laser_photons(E_pulse, laser_wavelength)

    Omega   = .75 * collection_optics_solid_angle(length_to_lens, radius_of_lens)
    
    wavelengths = []
    strengths   = []
    
    i = 0
    for i in range(1, 50):
        l_r = raman_wavelength(i, laser_wavelength, B)
        n_J     = raman_J_density(i, B, pressure, temperature)
        cross   = raman_crosssection(i, laser_wavelength, B, gamma_sq)
        
        wavelengths.append(l_r)
        strengths.append(n_laser* n_J* L_det*cross*Omega)
        
        i += 1
        
    return np.array(wavelengths), np.array(strengths)
        
 
def raman_photons_in_wavelength_range(E_pulse, laser_wavelength, B, gamma_sq, 
                                      pressure, temperature, L_det, 
                                      length_to_lens, radius_of_lens, 
                                      min_l, max_l):

    w, s = raman_photons(E_pulse, laser_wavelength, B, gamma_sq, pressure,
                  temperature, L_det, length_to_lens, radius_of_lens)
      
    value = 0 
    for i in range(0, len(w)):
        if w[i] >= min_l:
            if w[i] <= max_l:
                value += s[i]
          
       
    return value   
       
