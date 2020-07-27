# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 21:53:41 2018

@author: James Kring
@email:  jdk0026@auburn.edu_
"""

from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# Purpose: wout_File class to handle vmec wout files and produce flux surfaces with
# usable coordinates such as cylindrical and cartesian
#
# To Do: Need to generate full 3d output in cylindrical and cartesian
# =============================================================================

class wout_file:

    def __init__(self, wout_filepath):

        data            = Dataset(wout_filepath, 'r')
        #print(data.variables.keys())
        #print(data.variables['ctor'][:])

        self.rmnc       = np.array(data.variables['rmnc'][:])
        self.zmns       = np.array(data.variables['zmns'][:])
        self.xm         = np.array(data.variables['xm'])
        self.xn         = np.array(data.variables['xn'])

        self.phi = data.variables['phi'][:]

        self.ns         = data.variables['ns'][:]
        self.num_theta      = 499
        self.s              = self.get_flux_coord_s()

        self.curtor = data.variables['ctor'][:]

        self.xm_nyq = data.variables['xm_nyq'][:]
        self.xn_nyq = data.variables['xn_nyq'][:]

        self.bsubumnc = data.variables['bsubumnc'][:]
        self.bsubvmnc = data.variables['bsubvmnc'][:]
        self.bsupumnc = data.variables['bsupumnc'][:]
        self.bsupvmnc = data.variables['bsupvmnc'][:]

        #self.currumnc = data.variables['currumnc'][:]
        #self.currvmnc = data.variables['currvmnc'][:]

        self.gmnc = data.variables['gmnc'][:]

        self.lfreeb = data.variables['lfreeb__logical__'][:]


        self.lasym = data.variables['lasym__logical__'][:]

        self.jcurv = data.variables['jcurv'][:]
        self.jcuru = data.variables['jcuru'][:]

        self.s_total = np.linspace(0,1, self.ns + self.ns - 1)

        self.s_full = self.s_total[::2]
        self.s_half = self.s_total[1::2]

        self.iotaf = data.variables['iotaf'][:]
        self.iotas = data.variables['iotas'][:]
        self.iota_total = self.iotaf[0]

        self.Rmajor = data.variables['Rmajor_p'][:]
        self.Aminor = data.variables['Aminor_p'][:]

        self.presf = data.variables['presf'][:]
        pres = data.variables['pres'][:]
        self.pres_total = self.presf[0]
        self.pcurr_type = self.decode_nc_string([data.variables['pcurr_type'][:]])
#        self.pcurr_type = data.variables['pcurr_type'][:]


        if self.lasym:
            self.mns = data.variables['rmns'][:]
            self.zmnc = data.variables['zmnc'][:]
            self.bsubumns = data.variables['bsubumns'][:]
            self.bsubvmns = data.variables['bsubvmns'][:]
            self.bsupumns = data.variables['bsupumns'][:]
            self.bsupvmns = data.variables['bsupvmns'][:]

            self.gmns = data.variables['gmns'][:]

        for i in range(1, self.ns):
            self.iota_total = np.append(self.iota_total, self.iotas[i])
            self.iota_total = np.append(self.iota_total, self.iotaf[i])

        for i in range(1, self.ns):
            self.pres_total = np.append(self.pres_total, pres[i])
            self.pres_total = np.append(self.pres_total, self.presf[i])

        data.close()


    def get_flux_surfaces_at_phi_cyl(self, phi):
        # phi in degrees
        phi = phi/180 * np.pi
        theta = np.linspace(0, 2*np.pi, self.num_theta)


        R = np.zeros([self.ns, self.num_theta])
        Z = np.zeros([self.ns, self.num_theta])

        for j in range(0, len(self.rmnc)):
            for i in range(0, len(theta)):
                R[j,i] = sum(self.rmnc[j] * np.cos(self.xm * theta[i]- self.xn * phi))
                Z[j,i] = sum(self.zmns[j] * np.sin(self.xm * theta[i]- self.xn * phi))

        return R, Z


    def decode_nc_string(self, nc_array):
        new_array = []

        for item in nc_array:
            item_array = []
            for sub_item in item:
                decoded_sub_item = sub_item.decode("utf-8")
                item_array.append(decoded_sub_item)

            new_item = ''.join(item_array)
            new_array.append(new_item.rstrip())

        return new_array


    def get_flux_coord_s(self):
        # s = sqrt(phi/phi_edge)
        phi         = self.phi
        phi_edge    = phi[len(phi) - 1]
        s           = phi/phi_edge
        #s           = np.sqrt(phi/phi_edge)

        return s



def get_fluxsurfaces(ns, rmnc, zmns, xm, xn, num_theta, phi):
        # phi in degrees

        phi = phi/180 * np.pi
        theta = np.linspace(0, 2*np.pi, num_theta)
        xm = np.array(xm)
        xn = np.array(xn)
        ns = ns
        #print('ns',ns)
        R = np.zeros([ns, num_theta])
        Z = np.zeros([ns, num_theta])
        j = 0
        i = 0
        for j in range(0, len(rmnc)):
            for i in range(0, len(theta)):
                R[j,i] = sum(rmnc[j] * np.cos(xm * theta[i] - xn * phi))
                Z[j,i] = sum(zmns[j] * np.sin(xm * theta[i]
                                                   -xn * phi))

        return R[:ns], Z[:ns]


def get_fluxsurface_RZ_stheta(ns, rmnc, zmns, xm, xn, num_theta, phi):
        # phi in degrees

        phi = phi/180 * np.pi
        theta = np.linspace(0, 2*np.pi, num_theta)
        s = np.linspace(0, 1, ns +1)
        xm = np.array(xm)
        xn = np.array(xn)
        ns = ns
        #print('ns',ns)
        R = np.zeros([ns, num_theta])
        Z = np.zeros([ns, num_theta])


        s_grid = s[:,np.newaxis]*np.ones(num_theta)
        theta_grid = np.ones(ns)[:,np.newaxis]*theta

        j = 0
        i = 0

        for j in range(0, ns):
            for i in range(0, num_theta):
                R[j,i] = sum(rmnc[j] * np.cos(xm * theta[i] - xn * phi))
                Z[j,i] = sum(zmns[j] * np.sin(xm * theta[i]
                                                   -xn * phi))

        return R, Z, s_grid, theta_grid


def plot_array_on_flux_surfaces(wout_filepath, array, phi):
    # plot flux surface quantities such as T_e at a given phi location

    wout = wout_file(wout_filepath)
    R,Z = wout.get_flux_surfaces_at_phi_cyl(phi)
   #print(Z)
    #print(len(R))
    if len(array)==len(R):
        mesh = []
        for value in array:
            mesh.append([value]*len(R[0]))

        plt.figure()
        plt.gca().set_aspect('equal', adjustable='box')
        plt.xlim([.45, 1])
        plt.ylim([-.25, .25])
        plt.pcolormesh(R,Z,mesh)
        plt.colorbar()
        plt.show()

    else:
        print('Array is does not have the same number of flux surfaces as',wout_filepath)
        print(str(len(R)), ' flux surfaces needed.')
    return
