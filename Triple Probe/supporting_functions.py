# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 11:52:25 2019

@author: Ellie_2
"""
import numpy as np


def exp_size(wavelength,intensities, test_wavelength):
    
    import scipy.integrate as si
    # Gives the size of a peak of experimental data.
    # At the moment it just gives the height. It will eventually give 
    # the area under the curve.

    import numpy as np
    from lmfit.models import GaussianModel
    comparison_exp = np.where((np.array(wavelength) >= test_wavelength-.5) & 
                              (np.array(wavelength) <= test_wavelength + .5))[0]
    
    peaks = np.argmax(np.array(intensities)[comparison_exp])
    
#    print(test_wavelength)
#    
#    fig, ax1 = plt.subplots(1,1,figsize=(8,4))
#    fig.subplots_adjust(bottom=0.15,top=0.92,left=0.105,right=0.965)
#    ax1.set_title(str(test_wavelength))
#    ax1.set_xlabel("Wavelength (nm)")
#    ax1.set_ylabel("Intensity")
#    
#     if np.size(peaks) > 1:
    if np.size(peaks) > 0:
        
#        first_trough = np.max(ss.argrelmin(np.array(intensities)[list(range(comparison_exp[peaks]-15,comparison_exp[peaks]))]))
#        second_trough = np.min(ss.argrelmin(np.array(intensities)[list(range(comparison_exp[peaks],comparison_exp[peaks]+15))]))
        
        y = np.array(intensities)[list(range(comparison_exp[peaks]-8,comparison_exp[peaks]+8))]
        x = np.array(wavelength)[list(range(comparison_exp[peaks]-8,comparison_exp[peaks]+8))]
        mod = GaussianModel()
        pars = mod.guess(y, x=x)
        out = mod.fit(y, pars, x=x)
##        print(out.fit_report(min_correl=0.25))
#        plt.scatter(x,y)
#        plt.scatter(x,out.best_fit)
#        print(pars['sigma']._val)
        # (np.sqrt(2*np.pi*pars['height']._val))
#        # si.simps(y,x)
#        print("Integral of " + str(test_wavelength) + "= " + str(si.simps(out.best_fit,x)))
#        # print(x)
#        print("Peak of " + str(test_wavelength) + "= " + str(pars['height']._val))
        # x,y,peaks,first_trough,second_trough
        return si.simps(out.best_fit,x)
    
def nearby(comparison_array,array_to_change):
    
    # Gives the location of the value in comparison array nearest to array_to_change
    
    end_size = np.size(array_to_change)
    if end_size > 1:
        changed_array = np.zeros(end_size,dtype = int)
        for i in range(0,end_size):
            changed_array[i] = int(np.abs(comparison_array - array_to_change[i]).argmin())
    else:
        changed_array = int(np.abs(comparison_array - array_to_change).argmin())
        
    return changed_array    