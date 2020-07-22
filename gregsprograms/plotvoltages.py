# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 12:50:34 2020

@author: hartwgj
"""
from gregsprograms import ohshots
from gregsprograms import OHVoltageUsed
#from gregsprograms import plotOHvolts

def plotvoltages(day,server):
    shots=ohshots(day,day,server)
    OHVoltageUsed(shots,server)
    #plotOHvolts(shots,volts)