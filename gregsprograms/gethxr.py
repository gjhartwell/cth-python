# -*- coding: utf-8 -*-
"""
Created on Thu May 21 11:08:31 2020

@author: hartwgj
"""

# --------------------------------------
# GetHXR
# 
# MDSplus Python project
# for CTH data access
#
# 	getHXR --- plots the hard x-ray data for a given shot 
#
# Parameters:
#	shotnum - integer - the shotnumber to open
#	plotit - not implemented 
# Returns:
#
# Example:
#       get_hxr(shotnum)
#      
#
# 
#	
# Greg Hartwell
# 2020, May 21
#----------------------------------------------------------------------------

import matplotlib.pyplot as plt
import cthmds
from timeSubset import timeSubset

#from sys import argv

#shotnum = argv[1]

def gethxr(shotnum,server):
    if not server: 
        print('server = ',server)
        c=cthmds.cthconnect("mds")
    else:
        c=cthmds.cthconnect(server)
	
    cthmds.cthopen(c,shotnum)
    hxr=c.get('acqfast2:input_01')
    time=c.get('dim_of(acqfast2:input_01)')
    c.closeAllTrees
	
    time2=timeSubset(time,time,1.6,1.7)
    hxr2=timeSubset(time,hxr,1.6,1.7)
	

    plt.plot(time2,hxr2)
    plt.show()

#getip(20032705,"Neil")
gethxr(20032705,"mds")

#-----------------------------------------------------------------------------

	


