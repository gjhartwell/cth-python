# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 08:19:21 2018

@author: James
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from scipy.optimize import leastsq


def laser_photons(E_pulse, laser_wavelength):
    h       = 6.626*10**-34
    c       = 3*10**8     
    value   = E_pulse * (laser_wavelength/(h * c))
    return value


def collection_optics_solid_angle(length_to_lens, radius_of_lens):
    # The solid angle that is collected by the collection 
    # optics. length_to_lens is the distance from the scattering volume to the
    # location of the collection lens. radius_of_lens is the radius of the 
    # collection lens
    value = 2*np.pi*(1-np.cos(np.arctan(radius_of_lens/length_to_lens)))
    
    return value


def thomson_scattering_half_width(scattering_angle, laser_wavelength,
                                  plasma_temperature):
    T       = plasma_temperature * 11604
    theta   = scattering_angle
    c       = 3 *10**8
    kB      = 1.3806 *10**-23
    m_e     = 9.109*10**-31
    
    c1      = (8 * kB * T)/(m_e * c**2)
    c2      = (np.sin(theta/2))**2
    
    value   = (c1 * c2)**.5 * laser_wavelength
    return value


def thomson_crosssection(theta, phi):
    r_e     = 2.818*10**-15
    
    value   = r_e**2 * (1 - np.sin(theta)**2 * np.cos(phi)**2)
    return value

    
def thomson_photons(wavelength, E_pulse, laser_wavelength, electron_density, 
                    plasma_temperature, 
                    L_det, length_to_lens, radius_of_lens, theta, phi):
    
    n_laser = laser_photons(E_pulse, laser_wavelength)
    n_e     = electron_density
    del_l   = abs(laser_wavelength - wavelength)

    l_half  = thomson_scattering_half_width(theta, laser_wavelength,
                                            plasma_temperature)
    
    cross   = thomson_crosssection(theta, phi)
    Omega   = collection_optics_solid_angle(length_to_lens, radius_of_lens)
    expo    = (1/(l_half * np.sqrt(np.pi))) * np.exp(-(del_l/l_half)**2)
        
    value = n_laser * n_e * L_det * cross * Omega * expo
    
    return np.array(wavelength), np.array(value)


def thomson_photons_in_wavelength_range(wavelength, E_pulse, laser_wavelength, electron_density, 
                    plasma_temperature, 
                    L_det, length_to_lens, radius_of_lens, theta, phi,
                    min_l, max_l):

    w, s = thomson_photons(wavelength, E_pulse, laser_wavelength, electron_density, 
                           plasma_temperature, 
                           L_det, length_to_lens, radius_of_lens, theta, phi)
    
    value = 0 
    for i in range(0, len(w)):
        if w[i] >= min_l:
            if w[i] <= max_l:
                value += s[i]
          
       
    return value   


def step_function_array(start, stop, height):
    frac = (stop - start)/20
    x = np.linspace(start - frac, stop + frac, 110)
    y = np.array([0.0] * 110)
    y[5:104] = height
    return x, y


def plot_thomson_channels(height):
    x1, y1 = step_function_array(533.5, 539, height)
    plt.plot(x1, y1, 'k' , label = '533.5 - 539 nm')
    x1, y1 = step_function_array(539.5, 545, height)
    plt.plot(x1, y1, 'k' , label = '539.5 - 545 nm')  
    x1, y1 = step_function_array(545.5, 551, height)
    plt.plot(x1, y1, 'k' , label = '545.5 - 551 nm')    
    x1, y1 = step_function_array(551.5, 557, height)
    plt.plot(x1, y1, 'k' , label = '551.5 - 557 nm') 
    x1, y1 = step_function_array(557.5, 563, height)
    plt.plot(x1, y1, 'k' , label = '557.5 - 563 nm')
    return


