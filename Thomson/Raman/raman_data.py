# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 13:25:13 2017

@author: James
"""

import numpy as np
import matplotlib.pyplot as plt
import thomson as th
plt.ioff()
#R = 2 * 10**6
R = 25
mu = 2 * 10**5
tau = 2 * 10**-9
e = 1.60217662 * 10 **-19

"""
photon_array = []


for i in range(3, 23):
    if i < 10:
        shot = '1709290' + str(i)
    else:
        shot = '170929' + str(i)

    shot = int(shot)
    s1   = th.Thomson(shot)
    photons, photon_error, x, y, y_ini = s1.total_photons(mu, .4, R)
    time, data = s1.get_pmt_current_data_smooth(25)
    
    print(str(shot) + ': ' + str(photons))
    fig = plt.figure()
    plt.title(str(shot))
    
    plt.plot(x, y_ini, 'y', label = 'Initial')
    plt.plot(x, y, 'r', label = 'Fit')
    plt.plot(time, data, 'k', label = 'Data')
    plt.show()
    plt.xlabel('Time')
    plt.ylabel('Photons')
    plt.savefig('170929_plots/' + str(shot) +'_new.png')
    plt.close(fig)
    
    photon_array.append([photons, photon_error])
    
    
    
  
   
np.savetxt('170929_photon_counts_a_new_fit.txt', np.array(photon_array))

print(photon_array)
print('Done')
"""
a1 = np.loadtxt('170929_photon_counts_combined_b_edit.txt')
a2 = np.loadtxt('170929_photon_counts_test.txt')

pressure_a = np.loadtxt('170929_pressure_torr_a.txt')
pressure_b = np.loadtxt('170929_pressure_torr_b_edit.txt')
plt.figure()
plt.plot(pressure_b, a1, 'k')
#plt.plot(pressure_a, a2, 'r')
#plt.plot(pressure_a, (a1 + a2) * .5, 'b')
plt.show()

a = np.loadtxt('170929_photon_counts_combined_a.txt')
b = np.loadtxt('170929_photon_counts_combined_b_edit.txt')


pressure_a = np.loadtxt('170929_pressure_torr_a.txt')
pressure_b = np.loadtxt('170929_pressure_torr_b_edit.txt')



weights_b = np.loadtxt('weights_b.txt')
weights = weights_b[1:20]

plt.figure()
pressure_a1 = np.loadtxt('170929_pressure_torr_a.txt')

x, y = pressure_b, a1
print(len(y))

a = np.polyfit(x, y, 1, w = weights)

plt.scatter(pressure_b, a1, color = 'b')
#plt.scatter(pressure_b, run_b, color = 'b', label = '2nd Position')


plt.xlabel('Pressure (torr)', fontsize = 15, weight = 'bold')
#plt.xlabel('Number Density ($m^{-3}$)')
plt.ylabel('Photons', fontsize = 15, weight = 'bold')


label1 = str('y = ' + str(np.round(a[0],2)) + 'x + ' + str(np.round(a[1],2)))
print(label1)
plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)),
         color='k',label = label1)
plt.legend()
#plt.ylim([-25, 575])
plt.title('Raman Scattering of Nitrogen \n 170929 (565 nm - 543 nm)', 
          fontsize = 15, weight ='bold')
plt.xticks(fontsize = 13, weight = 'bold')
plt.yticks(fontsize = 13, weight = 'bold')
plt.savefig('raman_plot.png', format='png', dpi = 1000)
plt.show()





