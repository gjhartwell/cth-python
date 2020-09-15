# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 11:14:46 2020

@author: hartwgj
"""

import matplotlib.pyplot as plt
from vmec import wout_file
from vmec import get_fluxsurfaces
from vmec import get_bmod
import numpy as np

#file='C:\\Users\\hartwgj\\Documents\\Reconstructions\\shots_200327\\shot_20032705\\20032705ls\\wout_20032705_1.64_2.nc'#
#file="C:\\Users\\hartwgj\\Documents\\Reconstructions\\Steve_Recon_Pack_2016\\18102253\\wout_18102253_1.61_3.nc"
#file='C:\\Users\\hartwgj\\Desktop\\TestReconFiles\\20032705\\wout_20032705_1.645_0.nc'
#file='C:\\Users\\hartwgj\\Desktop\\wout files\\wout_20032705_1.63_0.nc'
file=r'C:\Users\hartwgj\Documents\Reconstructions\Nic20072944\20072944\wout_20072944_1.67_0.nc'
test=wout_file(file)


parts1=file.split('\\')
parts=parts1[-1].split('_')
time=parts[2]

parts1=file.split('\\')
parts=parts1[-1].split('_')
shot=parts[1]


phi=36


R,Z=get_fluxsurfaces(test,100,phi)

for i in range(len(R)):
    plt.plot(R[i], Z[i]) 

plt.axes().set_aspect('equal')

Rvv=0.29
Rlim=0.265
theta=np.arange(0.0,999)*2.0*np.pi/1000
R=np.cos(theta)
Z=np.sin(theta)

plt.plot(R*Rvv+0.75,Z*Rvv)
plt.title('shot '+shot+'  $\phi= $'+str(phi)+'  '+time+'s')
plt.xlabel('R(m)')
plt.ylabel('Z(m)')
#plt.plot(R*Rlim+0.75,Z*Rlim)
plt.show()

R,Z,B=get_bmod(test,100,0)

print("central bmod",B[0,0])
levels = [0.0, 0.1, 0.2,0.3,0.4,0.5]

# B=np.sqrt(B*B)
# print(B[1:])
cp = plt.contourf(R,Z,B)
plt.axes().set_aspect('equal')
plt.colorbar(cp)
plt.show()