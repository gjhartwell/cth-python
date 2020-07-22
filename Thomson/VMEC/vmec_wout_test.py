# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 20:35:09 2018

@author: James Kring
@email:  jdk0026@auburn.edu
"""





from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
f = Dataset('test.nc')

#print(f.variables['rmnc'])

phi = np.pi * 0
ns  = 4

rmnc = np.array(f.variables['rmnc'][:])
zmns = np.array(f.variables['zmns'][:])
xm = np.array(f.variables['xm'])
xn = np.array(f.variables['xn'])

#print(xn.shape)
#print(xn)

u = np.linspace(0, 2 * np.pi, 100)
r = np.zeros(len(u))
z = np.zeros(len(u))

plt.figure()
plt.gca().set_aspect('equal', adjustable='box')
plt.xlim([.55, .8])
plt.ylim([-.25, .25])

for j in range(0, len(rmnc)):
    for i in range(0, len(u)):
    
        r[i] = sum(rmnc[j] * np.cos(xm * u[i] - xn *phi))
        z[i] = sum(zmns[j] * np.sin(xm * u[i] - xn *phi))
    
    plt.plot(r, z, 'k')

"""
x = np.cos(phi) * r
plt.show()
plt.figure()
plt.plot(x, z)
"""



plt.show()

print(f.variables['phi'][:])

"""
print(f.variables['xn'])
print(f.variables['xm'])

print(f.variables['rmnc'])
print(f.variables['zmns'])
"""
#print(z)