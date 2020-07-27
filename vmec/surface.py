#-----------------------------------------------------
#Modified from a written by CaoXiang ZHU (czhu@pppl.gov)
#March, 11, 2020
#-----------------------------------------------------

import numpy as np
import xarray as ncdata
import matplotlib.pyplot as plt
from mayavi import mlab # to overrid plt.mlab


def plot_vmec_surface(wout, ns=-1, plottype='cross-section',zeta=0.0, zeta1=2*np.pi,
                         color=(1,0,0),style='-', marker=None, width=2.0, lbl='VMEC_surface',npol=128,ntor=128, prange='full'):
    '''
    wout : the vmec netcdf file;
    plot the ns-th flux surface;
    '''
    half = 0.5
    vmec = ncdata.open_dataset(wout)
    mf = vmec['mpol'].values
    nf = vmec['ntor'].values
    xm = vmec['xm'].values
    xn = vmec['xn'].values
    rmnc = vmec['rmnc'].values
    zmns = vmec['zmns'].values
    rbc = rmnc[ns,:]
    zbs = zmns[ns,:]

    if vmec['lasym__logical__'].values: # if no stellarator symmetry
        zmnc = vmec['zmnc'].values
        rmns = vmec['rmns'].values
        rbs = rmns[ns,:]
        zbc = zmnc[ns,:]
    else :
        rbs = np.zeros(np.shape(rbc))
        zbc = np.zeros(np.shape(rbc))

    if plottype=='cross-section' : #plot cross-section
        npoints = 361 #number of points
        theta = np.linspace(0,2*np.pi, npoints)
        r = np.zeros(npoints)
        z = np.zeros(npoints)
        for ipoint in range(npoints):
            tmpr = rbc*np.cos(xm*theta[ipoint]-xn*zeta) + rbs*np.sin(xm*theta[ipoint]-xn*zeta)
            r[ipoint] = np.sum(tmpr) #r value at ipont

            tmpz = zbs*np.sin(xm*theta[ipoint]-xn*zeta) + zbc*np.cos(xm*theta[ipoint]-xn*zeta)
            z[ipoint] = np.sum(tmpz) #z value at ipont
        if plt.get_fignums():
            fig = plt.gcf()
            ax = plt.gca()
        else :
            fig, ax = plt.subplots()

        plt.axis('equal')
        plt.xlabel('R [m]',fontsize=20)
        plt.ylabel('Z [m]',fontsize=20)
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=16)
        plt.tight_layout()

        if prange == 'full':
            ax.plot(r, z, color=color,linewidth=width,linestyle=style,label=lbl, marker=marker)
            plt.show()
            return r, z
        elif prange == 'upper':
            ax.plot(r[0:npoints/2+1], z[0:npoints/2+1], color=color,linewidth=width,linestyle=style,label=lbl)
            return r[0:npoints/2+1], z[0:npoints/2+1]
        elif prange == 'below':
            ax.plot(r[npoints/2:npoints], z[npoints/2:npoints], color=color,linewidth=width,linestyle=style,label=lbl)
            return r[npoints/2:npoints], z[npoints/2:npoints]
        else:
            raise NameError("No such option!")


    #mayavi 3D plot
    elif plottype == 'surface3d' :
        x=np.zeros((npol+1,ntor+1))
        y=np.zeros((npol+1,ntor+1))
        z=np.zeros((npol+1,ntor+1))

        for i in range(ntor+1):
            ator = zeta + (i+half)*(zeta1-zeta)/ntor #zeta
            for j in range(npol+1):
                apol = (j+half)*2*np.pi/npol #theta
                tmpr = rbc*np.cos(xm*apol-xn*ator)
                tmpz = zbs*np.sin(xm*apol-xn*ator)

                x[j,i] = np.sum(tmpr) * np.cos(ator)
                y[j,i] = np.sum(tmpr) * np.sin(ator)
                z[j,i] = np.sum(tmpz)
        fig = mlab.figure(bgcolor=(1,1,1),fgcolor=(0,0,0),size=(600,600))
        mlab.mesh(x,y,z,color=color)
        mlab.show()
        return x, y, z
    else :
        raise NameError("No such option!")
        print("plottype = cross-section/surface3d")
