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
        self.bmnc = data.variables['bmnc'][:]

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
        self.volume_p = data.variables['volume_p'][:]
        
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
                R[j,i] = sum(self.rmnc[j] * np.cos(self.xm * theta[i] 
                                                   - self.xn * phi))
                Z[j,i] = sum(self.zmns[j] * np.sin(self.xm * theta[i] 
                                                   - self.xn * phi))        
                
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

def get_fluxsurfaces(wout, num_theta, phi):
        # phi in degrees
        
        phi = phi/180 * np.pi
        theta = np.linspace(0, 2*np.pi, num_theta)
        xm = np.array(wout.xm)
        xn = np.array(wout.xn)
        ns = wout.ns
        #print('ns',ns)
        R = np.zeros([ns, num_theta])
        Z = np.zeros([ns, num_theta])        
        j = 0
        i = 0
        for j in range(0, len(wout.rmnc)):
            for i in range(0, len(theta)):
                R[j,i] = sum(wout.rmnc[j] * np.cos(xm * theta[i] - xn * phi))
                Z[j,i] = sum(wout.zmns[j] * np.sin(xm * theta[i] 
                                                   -xn * phi))        
                
        return R[:ns], Z[:ns]

def get_maxR(wout, phi):
        # phi in degrees
        
        phi = phi/180 * np.pi
        theta = 0.0
        xm = np.array(wout.xm)
        xn = np.array(wout.xn)
        ns = wout.ns
        #print('ns',ns)
        
       
        Rmax = sum(wout.rmnc[ns-1] * np.cos(xm * theta - xn * phi))
              
                
        return Rmax

def get_iotabar(woutdata):
    # gets the rotational transform information from the wout file
    # also returns the 's' of toroidal flux array
    # Greg Hartwell
    # July 17, 2020
    # woutdata - storage for wout file from James code
    
    size=woutdata.ns*2-1
    s=(np.arange(size)+1)/size
    iotabar=woutdata.iota_total
    
    return s,iotabar


def get_bmod(woutdata, num_theta, phi):
    # determines |B| on the flux surfaces
    # also calculates the R and Z positions of the flux surfaces
    # Returns - R, Z, |B|(R,Z) that is suitable for a contour plot
    #
    # Greg Hartwell
    # June 26, 2020
    # woutdata - storage for wout file data per James code
    # phi - toroidal angle in degrees
    # num_theta - number of poloidal angles per flux surface
        
    phi = phi/180 * np.pi
    theta = np.linspace(0, 2*np.pi, num_theta)
    xm = np.array(woutdata.xm)
    xn = np.array(woutdata.xn)
    ns = woutdata.ns
    
    R = np.zeros([ns, num_theta])
    Z = np.zeros([ns, num_theta]) 
    bc= np.zeros([ns, num_theta])
    bmnc=np.array(woutdata.bmnc)
    
    #determine index array for bmnc coefficents that are used
    idx=[]
    for i in range(bmnc.shape[1]):
        for j in range(len(woutdata.xm)):
            if (woutdata.xm_nyq[i] == xm[j]) \
                    and (woutdata.xn_nyq[i] == xn[j]):
                        idx.append(i)
    # Set b2 to bmnc with above coeffcients
    # and set 0 surface to a combonation of surface 1 and 2
    # don't remember why and there may be a better way
    b2=bmnc[:,idx]
    for j in range(0,len(woutdata.rmnc)):
        b2[0,j]=1.5*bmnc[1,j]-0.5*bmnc[2,j]   

    
    for j in range(0, len(woutdata.rmnc)):
        for i in range(0, len(theta)):
            R[j,i] = sum(woutdata.rmnc[j] * np.cos(xm * theta[i] - xn * phi))
            Z[j,i] = sum(woutdata.zmns[j] * np.sin(xm * theta[i] - xn * phi)) 
            bc[j,i]= sum(b2[j] * np.cos(xm*theta[i]-xn*phi))            
            
    return R[:ns], Z[:ns], np.abs(bc[:ns] )


def get_fluxsurface_RZ_stheta(ns, rmnc, zmns, xm, xn, num_theta, phi):
        # phi in degrees
        
        phi = phi/180 * np.pi
        theta = np.linspace(0, 2*np.pi, num_theta)
        s = np.linspace(0, 1, ns)
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

#test = wout_file('fermi_dirac/wout_14092626_1.6495_0.vmec.nc')
#R, Z =test.get_flux_surfaces_at_phi_cyl(36) 

#plt.figure()
#for i in range(len(R)):
#    plt.plot(R[i], Z[i], 'k') 

"""


test = wout_file('fermi_dirac/wout_14092626_1.6495_0.vmec.nc')



R,Z, s_grid, theta_grid = get_fluxsurface_RZ_stheta(test.ns, test.rmnc, test.zmns, test.xm, test.xn,
                                5, 252)


print(theta_grid[0])


#R, Z =test.get_flux_surfaces_at_phi_cyl(72) 

for i in range(len(R)):
    plt.plot(R[i], Z[i], 'k') 
#print(R)




r = np.linspace(0, .2, len(R))
theta = np.linspace(0, 2*np.pi, 100)

R1 = r[:,np.newaxis]*np.cos(theta) + R[0][0]
Z1 = r[:,np.newaxis]*np.sin(theta) + Z[0][0]


print(R1[-1])
print(Z1[-1])



#file1 = 'fermi_dirac/fd_norm.nc'
#file2 = 'fermi_dirac/fd.nc'
#test1 = wout_file(file1)
#test2 = wout_file(file2)

#print(sum(test1.jcuru))

#print(' ')
#print(test2.jcuru)
#print(test2.jcurv)
#print(test2.gmnc)



from result_file import result_file
wout_filepath = 'fermi_dirac/wout_14092626_1.6495_0.vmec.nc'
result_filepath = 'fermi_dirac/result.input.14092626_1.6495_0.v3fit.nc'

#wout_filepath_curt = 'wout_14092626_1.6495_0.vmec.nc'
#result_filepath_curt = 'result.input.14092626_1.6495_0.v3fit.nc'

recout = result_file(result_filepath)

te_grid = recout.te_grid[-1]   #From the last reconstruction step


plot_array_on_flux_surfaces(wout_filepath, te_grid, 72)





values = np.linspace(1, 0, 15)
print(values)




R, Z =test.get_flux_surfaces_at_phi_cyl(72) 
plt.figure()
plt.gca().set_aspect('equal', adjustable='box')
plt.xlim([.45, 1])
plt.ylim([-.25, .25])

for i in range(len(R)):
    plt.plot(R[i], Z[i], 'k')    


array = []
for value in values:
    array.append([value]*len(R[0]))



plt.figure()
plt.pcolormesh(R,Z,array)
plt.gca().set_aspect('equal', adjustable='box')
plt.xlim([.45, 1])
plt.ylim([-.25, .25])
plt.colorbar()

"""
