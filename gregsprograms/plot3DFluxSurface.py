# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 13:32:38 2020

@author: hartwgj
"""
    
    
    # -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 11:14:46 2020

@author: hartwgj
"""

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
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


# parts1=file.split('\\')
# parts=parts1[-1].split('_')
# time=parts[2]

# parts1=file.split('\\')
# parts=parts1[-1].split('_')
# shot=parts[1]


# ls=test.ns-1
# phimin=0.0
# phimax=359.0
# dphi=1.0
# nphi=int((phimax-phimin)/dphi)

# phiarray=np.linspace(phimin,phimax,nphi)

# R=[]
# Z=[]
# B=[]
# for p in phiarray:
#     Rtemp,Ztemp,Btemp=get_bmod(test,100,0)
#     R.append(Rtemp[ls])
#     Z.append(Ztemp[ls])
#     B.append(Btemp[ls])
    
# plt.plot(R[0],Z[0])
# plt.show()
# plt.plot(R[0],B[0])
# plt.show()

# make a vacuum vessel
nphi=2000
ntheta=2000
Ro=0.75
avv=0.3
phiarr=np.arange(nphi)/(nphi-1)*2.0*np.pi
thetaarr=np.arange(ntheta)/(ntheta-1)*2*np.pi
r=np.zeros([nphi,ntheta])
z=np.zeros([nphi,ntheta])
xarr=np.zeros([nphi,ntheta])
yarr=np.zeros([nphi,ntheta])

#create in r,z,phi coordinates
for k,phi in enumerate(phiarr):
    for i,theta in enumerate(thetaarr):
        r[k,i]=Ro+avv*np.cos(theta)
        z[k,i]=avv*np.sin(theta)

# put into cartesian coordinates for plotting
for k,phi in enumerate(phiarr):
    for i,theta in enumerate(thetaarr):
        xarr[k,i]=r[k,i]*np.cos(phi)
        yarr[k,i]=r[k,i]*np.sin(phi)



fig = plt.figure()
ax = fig.gca(projection='3d')

surf=ax.plot_surface(xarr,yarr,z,
                 cmap=cm.coolwarm,linewidth=0) # , #antialiased=False,

plt.show()
# aspect_ratio=1,aspect_z=1, $
# color='gray', $
# axis_style=0, $
# transparency=transparency,shading=1,_extra=extrakeywords


