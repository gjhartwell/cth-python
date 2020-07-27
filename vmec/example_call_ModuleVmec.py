'''
Run with Python 3
Plot flux surfaces at different angular positions
'''
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
from ModuleVmec import *
import os

cwd = os.getcwd()
Nfp = 5 #CTH field period
torangleList = np.linspace(0,180/Nfp,5)
for torangle in torangleList:
    name = cwd + "/wout_vmec.nc"
    test = wout_file(name)
    R, Z = test.get_flux_surfaces_at_phi_cyl(torangle) #Phi is in degrees
    RoCTH , aCTH = 0.75, 0.29
    circle = plt.Circle((RoCTH, 0), aCTH, color='k', fill=False)
    fig, ax = plt.subplots()
    #for i in range(10):
    #    plt.plot(R[10*i], Z[10*i], 'k') #Select subset of mag. surfaces
    for i in range(len(R)):
        plt.plot(R[i], Z[i], 'k')
    ax.set_aspect(1)
    ax.add_artist(circle)
    plt.title('CTH-1608535, '+r'$\phi='+str(torangle)+'$')
    plt.xlabel('R [m]',fontsize=18)
    plt.ylabel('Z [m]',fontsize=18)
    plt.xlim( 0.95 * (RoCTH-aCTH) , 1.05 *(RoCTH+aCTH) )
    plt.ylim(-1.05*aCTH,1.05*aCTH)
    name =  cwd + '/CTH-1608535_free_magsurf_'+str(torangle)+'.png'
    plt.savefig(name)
    plt.close()
