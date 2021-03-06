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
import cthmds
from timeSubset import timeSubset

#from sys import argv

#shotnum = argv[1]

def getip(shotnum,server):
    if not server: 
        print('server = ',server)
        c=cthmds.cthconnect("mds")
    else:
        c=cthmds.cthconnect(server)
	
    cthmds.cthopen(c,shotnum)
    Ip=c.get('\\I_p')
    time=c.get('dim_of(\\I_p)')
    c.closeAllTrees
	
    time2=timeSubset(time,time,1.6,1.7)
    Ip2=timeSubset(time,Ip,1.6,1.7)
	

    plt.plot(time2,Ip2)
    plt.show()

#getip(20032705,"Neil")
getip(20032705,"mds")

#-----------------------------------------------------------------------------

	


