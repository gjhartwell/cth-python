# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 11:14:46 2020

@author: hartwgj
"""

import matplotlib.pyplot as plt
from vmec import wout_file
from vmec import get_fluxsurfaces
from vmec import get_bmod

file='C:\\Users\\hartwgj\\Documents\\Reconstructions\\shots_200327\\shot_20032705\\20032705ls\\wout_20032705_1.64_2.nc'#
#file="C:\\Users\\hartwgj\\Documents\\Reconstructions\\Steve_Recon_Pack_2016\\18102253\\wout_18102253_1.61_3.nc"
file='C:\\Users\\hartwgj\\Desktop\\TestReconFiles\\wout_20032705_1.64_7.nc'
test=wout_file(file)

R,Z=get_fluxsurfaces(test,100,0)

for i in range(len(R)):
    plt.plot(R[i], Z[i]) 

plt.axes().set_aspect('equal')
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