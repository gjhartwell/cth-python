# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 12:34:53 2020

@author: hartwgj
"""

import glob
from os.path import join
from vmec import wout_file
from vmec import get_maxR
import matplotlib.pyplot as plt
def getWoutFiles(folder):
    path=join(folder,'wout_*.nc')
    files=glob.glob(path)
    return files
 
def timeFromWoutFile(file):
    parts1=file.split('\\')
    parts=parts1[-1].split('_')
    time=parts[2]
    return time

def shotFromFile(file):
    parts1=file.split('\\')
    parts=parts1[-1].split('_')
    shot=parts[1]
    return shot
   
def plotrMajor(folder):
    files=getWoutFiles(folder)
    rmajor=[]
    time=[]
    for f in files:
        wout=wout_file(f)
        rmajor.append(float(wout.Rmajor))
        time.append(float(timeFromWoutFile(f)))
        
    shot=shotFromFile(files[0])
    
    major_radius,=plt.plot(time,rmajor,color='b',label='$R_{major}$',
                            linestyle='',marker='o',markersize=3)
    
    plt.title('shot '+str(shot))
    plt.xlabel('time(s)')
    plt.ylabel('Ro (m)')
    plt.legend(handles=[major_radius])
    plt.show()    
    
def plotrRmax(folder,phi):
    files=getWoutFiles(folder)
    Rmax=[]
    time=[]
    for f in files:
        wout=wout_file(f)
        Rmax.append(get_maxR(wout,phi))
        time.append(float(timeFromWoutFile(f)))
        
    shot=shotFromFile(files[0])   
    max_radius,=plt.plot(time,Rmax,color='b',label='$R_{maximum}$',
                            linestyle='',marker='o',markersize=3)
    plt.title('shot '+str(shot))
    plt.xlabel('time(s)')
    plt.ylabel('Rmax (m)')
    plt.legend(handles=[max_radius])
    plt.show()   
    print('maximum Rmax',max(Rmax))

def plotRmaxAndRmajor(folder,phi):
    files=getWoutFiles(folder)
    rmajor=[]
    Rmax=[]
    time=[]
    shot=shotFromFile(files[0]) 
    
    for f in files:
        wout=wout_file(f)
        rmajor.append(float(wout.Rmajor))
        Rmax.append(get_maxR(wout,phi))
        time.append(float(timeFromWoutFile(f)))
    
    plt.plot(time,Rmax,color='g',label='$R_{maximum}$',
                            linestyle='',marker='o',markersize=3)
    plt.plot(time,rmajor,color='m',label='$R_{major}$',
                            linestyle='',marker='o',markersize=3)
    plt.title('shot '+str(shot))
    plt.xlabel('time(s)')
    plt.ylabel('R (m)')
    plt.legend()
    plt.show()    
    
    
    
def plotIotas(folder):
    files=getWoutFiles(folder)
    iota0=[]
    iotaf=[]
    time=[]
    for f in files:
        wout=wout_file(f)
        iota0.append(float(wout.iota_total[0]))
        iotaf.append(float(wout.iota_total[-1]))
        time.append(float(timeFromWoutFile(f)))
    
    shot=shotFromFile(files[0])
        
    iota_axis,=plt.plot(time,iota0,color='b',label='iota(0)',
                        linestyle='',marker='o',markersize=3)
    iota_edge,=plt.plot(time,iotaf,color='r',label='iota(a)',
                       linestyle='',marker='o',markersize=3)
    plt.title('rotational transform - shot '+str(shot))
    plt.xlabel('time(s)')
    plt.ylabel('rotational transform')
    plt.legend(handles=[iota_axis,iota_edge])
    plt.show()
    
def plotPhiEdge(folder):
    files=getWoutFiles(folder)
    phiedge=[]
    time=[]
    for f in files:
        wout=wout_file(f)
        phiedge.append(float(wout.phi[-1]))
        time.append(float(timeFromWoutFile(f)))
    
    shot=shotFromFile(files[0])   
        
    plt.title('shot '+str(shot))
    phi_edge,=plt.plot(time,phiedge,color='g',label='$\Phi(a)$',
                        linestyle='',marker='o',markersize=3)
    plt.xlabel('time(s)')
    plt.ylabel('$\Phi_{edge}$')
    plt.legend(handles=[phi_edge])
    plt.show()
        
    
    
folder=r'C:\Users\hartwgj\Documents\Reconstructions\Nic20072944\20072944'
#folder=r'C:\Users\hartwgj\Documents\Reconstructions\shots_200327\shot_20032705\20032705ls'
#plotrMajor(folder)
#plotIotas(folder)
#plotPhiEdge(folder)
#plotrRmax(folder,36)
plotRmaxAndRmajor(folder,36)