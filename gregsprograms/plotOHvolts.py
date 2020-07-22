# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 11:33:07 2020

@author: hartwgj
"""
import matplotlib.pyplot as plt
def plotOHvolts(shots,volts):
    nshots=[]
    for idx in range(len(shots)):
        nshots.append(shots[idx] % 100)
    plt.plot(nshots,volts,'go')
    plt.ylim(800,1000)
    titlestring=str(int((shots[0]-shots[0] % 100)/100))
    plt.title(titlestring)
    plt.ylabel("OH LV Bank (V)")
    plt.xlabel("shot number")
    plt.show()