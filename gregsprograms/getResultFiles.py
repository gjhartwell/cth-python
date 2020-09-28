# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 13:25:04 2020

@author: hartwgj
"""
import glob
from os.path import join
from results_file_contents import results_file_contents
import matplotlib.pyplot as plt
import numpy as np

def getResultFiles(folder):
    path=join(folder,'result.*.nc')
    files=glob.glob(path)
    return files
 
def timeFromResultFile(file):
    parts1=file.split('\\')
    parts=parts1[-1].split('_')
    time=parts[1]
    return time

def shotFromResultFile(file):
    parts1=file.split('\\')
    parts=parts1[-1].split('_')
    parts=parts[0].split('.')
    shot=parts[1]
    return shot

def plotChi2(folder):
    files=getResultFiles(folder)
    chi2=[]
    time=[]
    
    for f in files:
        result=results_file_contents(f)
        chi2.append(float(result.g2))
        time.append(float(timeFromResultFile(f)))
    
    shot=shotFromResultFile(files[0])   
        
    plt.title('shot '+str(shot))
    chi_2,=plt.plot(time,chi2,color='g',label='$\chi^2$',
                        linestyle='',marker='o',markersize=3)
    plt.xlabel('time(s)')
    plt.ylabel('$\chi^2$')
    plt.yscale('log')
    plt.legend(handles=[chi_2])
    plt.show()
    
def plotParameters(folder):
    files=getResultFiles(folder)
    f=files[0]
    nfiles=len(files)
    shot=shotFromResultFile(f)
    result=results_file_contents(f)
    
    n_param=len(result.param_name)
    print("number of reconstructed parameters is",n_param)
    result=results_file_contents(f)
    names=[]
    for p in result.param_name:
        names.append(p)
    print(names)
    

    time=[]
    value=np.zeros((n_param,nfiles))
    sigma=np.zeros((n_param,nfiles))
    for fdx,f in enumerate(files):
        result=results_file_contents(f)
        time.append(float(timeFromResultFile(f)))
        
        for pdx,p in enumerate(result.param_name):
            value[pdx,fdx]=result.param_value[pdx]
            sigma[pdx,fdx]=result.param_sigma[pdx]
        
    for pdx,name in enumerate(names):
        
        if name=='phiedge':
            plt.title('$\Phi_{edge}$--shot '+str(shot))
            plt.errorbar(time,value[pdx,:],sigma[pdx,:],
                         color='g',
                         linestyle='',marker='o',markersize=3,
                         ecolor='gray',elinewidth=.7)
            plt.xlabel('time(s)')
            plt.ylabel('$\Phi_{edge}$')
            plt.ylim(min(value[pdx,:])*.9,max(value[pdx,:])*1.1)
            #plt.legend()
            plt.show()
        elif name=='pp_ne_af':
            unit=r' ($\times$ '+str(result.ne_unit[0])+r'$m^{-3}$)'
            tit=name+'('+str(result.param_index[pdx,0])+')'
            plt.title(tit+'--shot '+str(shot))
            plt.errorbar(time,value[pdx,:],sigma[pdx,:],
                         color='g',
                         linestyle='',marker='o',markersize=3,
                         ecolor='gray',elinewidth=.7)
            plt.xlabel('time(s)')
            plt.ylabel(name+unit)
            plt.ylim(min(value[pdx,:])*.9,max(value[pdx,:])*1.1)
            #plt.legend()
            plt.show()
        
    
    
def recon_synopsis(file):
    print(file)
    print('shot number',shotFromResultFile(file))
    print('reconstruction time',timeFromResultFile(file))
    
    result=results_file_contents(file)
    print('reconstruction steps',result.nsteps)
    print('chi^2',result.g2)
    print("number of reconstructed parameters is",len(result.param_name))
    print('index',result.param_index,'name',result.param_name)
    print('parameter values',result.param_value)
    print('parameter sigma',result.param_sigma)

    
folder=r'C:\Users\hartwgj\Documents\Reconstructions\shot_20090173\20090173b'
# files=getResultFiles(folder)
# file=files[0]
# recon_synopsis(file)
plotChi2(folder)
plotParameters(folder)
