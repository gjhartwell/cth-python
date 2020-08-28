# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 12:34:53 2020

@author: hartwgj
"""

import glob
from os.path import join
from vmec import wout_file
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
   
def plotrMajor(folder):
    files=getWoutFiles(folder)
    rmajor=[]
    time=[]
    for f in files:
        wout=wout_file(f)
        rmajor.append(float(wout.Rmajor))
        time.append(float(timeFromWoutFile(f)))
        
        
    plt.plot(time,rmajor,'bo')
    plt.xlabel('time(s)')
    plt.ylabel('Ro (m)')
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
        
        
    plt.plot(time,iota0,'bo')
    plt.plot(time,iotaf,'ro')
    plt.xlabel('time(s)')
    plt.ylabel('$\iota_0$')
    plt.show()
    
def plotPhiEdge(folder):
    files=getWoutFiles(folder)
    phiedge=[]
    time=[]
    for f in files:
        wout=wout_file(f)
        phiedge.append(float(wout.phi[-1]))
        time.append(float(timeFromWoutFile(f)))
        
        
    plt.plot(time,phiedge,'go')
    plt.xlabel('time(s)')
    plt.ylabel('$\Phi_{edge}$')
    plt.show()
        
    
    
folder=r'C:\Users\hartwgj\Desktop\TestReconFiles\20032705'
#folder=r'C:\Users\hartwgj\Documents\Reconstructions\shots_200327\shot_20032705\20032705ls'
plotrMajor(folder)
plotIotas(folder)
plotPhiEdge(folder)