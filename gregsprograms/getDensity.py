# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 09:58:34 2020

@author: hartwgj
"""
# --------------------------------------
# GetIp.py
# 
# MDSplus Python project
# for CTH data access
#
# 	get_ip --- plots the plasma current for the given shot 
#
# Parameters:
#	shotnum - integer - the shotnumber to open
#	plotit - not implemented 
# Returns:
#
# Example:
#       plasma_current=get_ip(shotnum)
#       not sure this works yet
#
# Also defines:
#	
# Greg Hartwell
# 2016-12-16
#----------------------------------------------------------------------------

import matplotlib.pyplot as plt
from cthconnect import cthconnect 
from cthopen import cthopen
import numpy as np

#from sys import argv

#shotnum = argv[1]

def getDensity(shotnum,server,ttime):
    if not server: 
        print('server = ',server)
        c=cthconnect("mds")
    else:
        c=cthconnect(server)
	
    cthopen(c,shotnum)
    nedl1=c.get('processed:intfrm_1mm:int_nedl_1')
    nedl2=c.get('processed:intfrm_1mm:int_nedl_2')
    nedl3=c.get('processed:intfrm_1mm:int_nedl_3')
    nedl4=c.get('processed:intfrm_1mm:int_nedl_4')
    time=c.get('dim_of(processed:intfrm_1mm:int_nedl_1)')
    c.closeAllTrees
    
    # time=np.array(time)
    # idx=np.where(time==ttime)
	

#    print(idx)

    tit='Density Plot - shot '+str(shotnum)

    plt.plot(time,nedl1/1.0E18,color='black')
    plt.plot(time,nedl2/1.0E18,color='blue')
    plt.plot(time,nedl3/1.0E18,color='red')
    plt.plot(time,nedl4/1.0E18,color='orange')
    
    plt.title(tit)
    plt.xlabel('time(s)')
    plt.ylabel('Neld ($x10^{18}m^{-3}$)')
    plt.show()

#getIp(20032705,"Neil")
getDensity(20090173,"mds",1.7)

#-----------------------------------------------------------------------------

	


