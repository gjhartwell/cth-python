# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 10:17:22 2018

@author: Greg
"""
import numpy as np
from cthmds.timeSubset import timeSubset

def findAverageValues(data,shot):
    #returns an array of data for specific times
    #averaged  over dt
    # data.data is the data
    # data.taxis is the time axis
    # shot has shotnumber, a time array, and dt information
    timeArray=shot.time
    #print("timeArray ",timeArray)
    #print(data)
    dt=shot.dt
#    print("dt = ",dt)
#    print("taxis is ",data.taxis)
#    print("data is ",data.data)
    averageValues=[]
    for time in timeArray:
        #average over the data from -dt/2 to dt/2
        dataRange=timeSubset(data.taxis,data.data,time-dt/2,time+dt/2)
        value=np.sum(dataRange)/np.size(dataRange)
        averageValues=averageValues+[value]
    #print("average values: ",averageValues)
    return averageValues
