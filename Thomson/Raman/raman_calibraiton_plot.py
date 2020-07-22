# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 22:35:00 2018

@author: James

"""
import numpy as np
import matplotlib.pyplot as plt
from raman_theory import total_photoelectrons_raman_center_function
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

R = 2 * 10**6
R = 25
mu = 2 * 10**5
tau = 20 * 10**-9

run_a = np.loadtxt('170929_g1_volt_edit.txt')
pressure_a = np.loadtxt('170929_pressure_torr_edit.txt')


def raw_volt_to_n( voltage, resistance, tau, gain):
    #takes the raw voltage and returns the number of electrons
    e = 1.60217662 * 10 **-19

    n = (tau * voltage*.001)/(gain * e * resistance)
    n = n/.4
    return n
weights = np.loadtxt('weights_a.txt')
weights = weights[:17]

Pressure = np.linspace(0, 50, 100)
Photons = total_photoelectrons_raman_center_function(1.8, Pressure, 295, 535.12, 562.10)

photons_collected = raw_volt_to_n(run_a, R, tau, mu)

plt.figure()
plt.plot(Pressure, Photons, 'k')


plt.scatter(pressure_a, photons_collected, color='r')



plt.xlabel('Pressure (Torr)', fontsize = 15, weight ='bold')
plt.ylabel('Photons', fontsize = 15, weight ='bold')
title = str("Predicted Raman Scattering \n (535.12 nm - 562.10 nm)")
plt.title(title, fontsize = 15, weight ='bold')
plt.xticks(fontsize = 13, weight = 'bold')
plt.yticks(fontsize = 13, weight = 'bold')

x, y = Pressure, Photons
a = np.polyfit(x, y, 1)
label2 = str('Photons Produced (Theory): ' + 'y = ' + str(np.round(a[0],2)) + 'x')
print(label2)
plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)),
         color='k',label = label2)

x, y = pressure_a, photons_collected
a1 = np.polyfit(x, y, 1, w = weights)
label1 = str('Photons Collected (Data)   : ' + 'y = ' + str(np.round(a1[0],2)) + 'x')
print(label1)
plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)),
         color='r',label = label1)


print(a1[0]/a[0])
plt.legend()


#plt.xlabel('Pressure (torr)', fontsize = 15, weight = 'bold')

#plt.ylabel('Photons', fontsize = 15, weight = 'bold')
#plt.title('Raman Scattering of Nitrogen \n(562 nm - 536 nm)', fontsize = 15, weight ='bold')
plt.xticks(fontsize = 13, weight = 'bold')
plt.yticks(fontsize = 13, weight = 'bold')
plt.savefig('raman_calibration.png', format='png', dpi = 1000)
plt.show()

