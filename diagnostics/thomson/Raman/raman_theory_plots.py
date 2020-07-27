# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 19:05:10 2018

@author: James
"""
import numpy as np
import matplotlib.pyplot as plt
import raman_theory_james as rt

B_N2 = 2.48*10**-4
gamma_sq_N2 = 0.395*10**-82
L_det_1 = .0142             

x = rt.raman_wavelength(4, 532*10**-9, B_N2)
y = rt.raman_crosssection(4, 532*10**-9, B_N2, gamma_sq_N2)
z = rt.raman_J_density(4, B_N2, 50, 295)
a = rt.raman_photons(1.69, 532*10**-9, B_N2, gamma_sq_N2, 50, 295, 
                  L_det_1, 71.8, 7.5)

b = rt.raman_photons_in_wavelength_range(1.69, 532*10**-9, B_N2, gamma_sq_N2, 50, 295, 
                  L_det_1, 71.8, 7.5, 533.0 *10**-9, 535.0*10**-9)
print(sum(a[1]))

print(b)



plt.plot(a[0] * 10**9, a[1])







Pressure = np.linspace(0, 50, 100)
#Photons = total_photoelectrons_raman_center_function(1.8, Pressure, 295, 536, 561)
Photons = rt.raman_photons_in_wavelength_range(1.69, 532*10**-9, B_N2, gamma_sq_N2, Pressure, 295, 
                  L_det_1, 71.8, 7.5, 533.0 *10**-9, 535.0*10**-9)

a = np.loadtxt('170929_photon_counts_a_new_fit.txt')
print(a[0][0])
c = []
for i in range(0, len(a)):
    c.append(a[i][0])

print(c)    
a = c    
b = np.loadtxt('170929_photon_counts_combined_b_edit.txt')


pressure_a = np.loadtxt('170929_pressure_torr_a.txt')
pressure_b = np.loadtxt('170929_pressure_torr_b_edit.txt')

weights_b = np.loadtxt('weights_b.txt')
weights_a = weights_b[1:len(a)]

plt.figure()




plt.plot(Pressure, Photons, c='k')
plt.scatter(pressure_a, a, c = 'r')
fit1 = np.polyfit(Pressure, Photons, 1)
label1 = str('Theory: y = ' + str(np.round(fit1[0],2)) + 'x')

plt.plot(np.unique(Pressure), np.poly1d(np.polyfit(Pressure, Photons, 1))(np.unique(Pressure)),
         color='k', label=label1)

fit2 = np.polyfit(pressure_a, a, 1)
label2 = str('Data: y = ' + str(np.round(fit2[0],2)) + 'x' )

plt.plot(np.unique(pressure_a), np.poly1d(np.polyfit(pressure_a, a, 1))(np.unique(pressure_a)),
         color='r', label = label2)

plt.xlabel('Pressure (Torr)', fontsize = 15, weight ='bold')
plt.ylabel('Photons', fontsize = 15, weight ='bold')
title = str("Predicted Raman Scattering \n (536 nm - 561 nm)")
plt.title(title, fontsize = 15, weight ='bold')
plt.xticks(fontsize = 13, weight = 'bold')
plt.yticks(fontsize = 13, weight = 'bold')
plt.legend()
#plt.savefig('test_1_theory_vs_data.png', format='png', dpi = 1000)
plt.savefig('17092920_raman_scattering_first_position.png', format='png', dpi = 1000,  bbox_inches='tight')

plt.show()