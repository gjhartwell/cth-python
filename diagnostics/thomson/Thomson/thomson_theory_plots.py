# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 19:02:35 2018

@author: James
"""
import matplotlib.pyplot as plt
import numpy as np
import thomson_theory as tt

x = np.linspace(530*10**-9, 580*10**-9, 200)


x, intensity1 = tt.thomson_photons(x, 1.8, 532*10**-9, 1*10**19, 
                                100, 
                                0.0142, 71.8, 7.5, np.pi * .5, np.pi * .5 )

x, intensity2 = tt.thomson_photons(x, 1.8, 532*10**-9, 1*10**19, 
                                200, 
                                0.0142, 71.8, 7.5, np.pi * .5, np.pi * .5 )

x, intensity3 = tt.thomson_photons(x, 1.8, 532*10**-9, 1*10**19, 
                                50, 
                                0.0142, 71.8, 7.5, np.pi * .5, np.pi * .5 )
"""
plt.figure()

#plt.plot(x*10**9, intensity3, 'b', label = '50 eV')
plt.plot(x*10**9, intensity1, 'k', linestyle = '--' , label = '100 eV')
#plt.plot(x*10**9, intensity2, 'r', label = '200 eV')
plt.xticks(fontsize = 13, weight = 'bold')
plt.yticks(fontsize = 13, weight = 'bold')
plt.xlabel('Wavelength (nm)', fontsize = 15, weight ='bold')
plt.ylabel('Photons Collected', fontsize = 15, weight ='bold')

plt.axvline(x = 532, c='k', linewidth=3, label = 'Laser Line')
tt.plot_thomson_channels(1 * 10**12)

title = str("Predicted Thomson Scattering")
plt.title(title, fontsize = 15, weight ='bold')
plt.legend()
plt.savefig('thomson_predicted_signal_half_profile_bins.png', format='png', dpi = 1000,  bbox_inches='tight')

plt.show()
"""

value = tt.thomson_photons_in_wavelength_range(x, 1.8, 532*10**-9, 1*10**19, 
                                50, 
                                0.0142, 71.8, 7.5, np.pi * .5, np.pi * .5,
                                536*10**-9, 561*10**-9)

print(value)
print(value * .002488 * 1.60217662 * 10 **-19 * .4 * 2*10**5 *25)