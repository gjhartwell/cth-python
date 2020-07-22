# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 21:53:41 2018

@author: James Kring
@email:  jdk0026@auburn.edu
"""

from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# Purpose: VMEC class to handle vmec wout files and produce flux surfaces with 
# usable coordinates such as cylindrical and cartesian
# 
# To Do: Need to generate full 3d output in cylindrical and cartesian 
# =============================================================================


class VMEC:
    
    def __init__(self, wout_filepath):
        self.wout       = Dataset(wout_filepath)
        self.rmnc       = np.array(self.wout.variables['rmnc'][:])
        self.zmns       = np.array(self.wout.variables['zmns'][:])
        self.xm         = np.array(self.wout.variables['xm'])
        self.xn         = np.array(self.wout.variables['xn'])       

        self.num_surfaces   = len(self.rmnc)
        self.num_theta      = 499
        self.s              = self.get_flux_coord_s()
        
    def get_flux_surfaces_at_phi_cyl(self, phi):
        # phi in degrees
        phi = phi/180 * np.pi
        theta = np.linspace(0, 2*np.pi, self.num_theta)
        
        R = np.zeros([self.num_surfaces, self.num_theta])
        Z = np.zeros([self.num_surfaces, self.num_theta])        
        
        for j in range(0, len(self.rmnc)):
            for i in range(0, len(theta)):
                R[j,i] = sum(self.rmnc[j] * np.cos(self.xm * theta[i] 
                                                   - self.xn * phi))
                Z[j,i] = sum(self.zmns[j] * np.sin(self.xm * theta[i] 
                                                   - self.xn * phi))        
                
        return R, Z

    
    def get_flux_coord_s(self):
        # s = sqrt(phi/phi_edge)
        phi         = np.array(self.wout.variables['phi'][:])
        phi_edge    = phi[len(phi) - 1]
        
        s           = np.sqrt(phi/phi_edge)

        return s


"""

test = VMEC('test.nc')
R, Z =test.get_flux_surfaces_at_phi_cyl(26) 
plt.figure()
plt.gca().set_aspect('equal', adjustable='box')
plt.xlim([.55, .8])
plt.ylim([-.25, .25])
plt.plot(R[14], Z[14], 'k')    
plt.plot([1, 0], [0, .1], 'r')

"""

