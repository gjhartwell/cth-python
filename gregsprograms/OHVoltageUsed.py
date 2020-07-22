# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 10:43:41 2020

@author: hartwgj
"""

# --------------------------------------
# OHVoltageUsed.py
# 
# MDSplus Python project
# for CTH data access
#
# 	OHVoltageUsed.py --- gets the shots within a given date range that use OH
#
# Parameters:
#	startdate
#   enddate
#	
# Returns:
#    list of shots
#
# Example:
#       volts=OHVoltageUsed(OHshots)
#
# Also defines:
#	
# Greg Hartwell
# 2020 June 9
#----------------------------------------------------------------------------
import cthmds
import matplotlib.pyplot as plt

def OHVoltageUsed(shots,server):
    #allways connect to mds server
    c=cthmds.cthconnect(server)
    volts=[]
    badshots=[]
    for shotnum in shots:
        cthmds.cthopen(c,shotnum)
        try:
            usedvolts=c.get('parameters:currents:oh:voltage_used')
        except:
            print(shotnum)
            badshots.append(shotnum)
        else:
            volts.append(usedvolts)
        
    #return volts

    for bshot in badshots: 
        shots.remove(bshot)
    print('voltage length ',len(volts))
    print('shots length ',len(shots))
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