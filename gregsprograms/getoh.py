# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 11:20:15 2020

@author: hartwgj
"""
# --------------------------------------
# GetOH.py
# 
# MDSplus Python project
# for CTH data access
#
# 	getOH --- plots the plasma current for the given shot 
#
# Parameters:
#	shotnum - integer - the shotnumber to open
#	plotit - not implemented 
# Returns:
#
# Example:
#       oh_current=getoh(shotnum,server)
#       not sure this works yet
#
# Also defines:
#	
# Greg Hartwell
# 2016-12-16
#----------------------------------------------------------------------------

import matplotlib.pyplot as plt
import cthmds
from timeSubset import timeSubset

#from sys import argv

#shotnum = argv[1]

def getOH(shotnum,server):
    if not server: 
        print('server = ',server)
        c=cthmds.cthconnect("mds")
    else:
        c=cthmds.cthconnect(server)
	
    cthmds.cthopen(c,shotnum)
    oh=c.get('\\I_OH')
    time=c.get('dim_of(\\I_OH)')
    c.closeAllTrees
	
    time2=timeSubset(time,time,1.6,2.5)
    oh=timeSubset(time,oh,1.6,2.5)
	
    print('maximum OH current: ',max(oh))

    plt.plot(time2,oh)
    plt.show()
