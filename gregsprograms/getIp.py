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
from timeSubset import timeSubset

#from sys import argv

#shotnum = argv[1]

def getIp(shotnum,server):
    if not server: 
        print('server = ',server)
        c=cthconnect("mds")
    else:
        c=cthconnect(server)
	
    cthopen(c,shotnum)
    Ip=c.get('\\I_p')
    time=c.get('dim_of(\\I_p)')
    c.closeAllTrees
	
    time2=timeSubset(time,time,1.6,1.7)
    Ip2=timeSubset(time,Ip,1.6,1.7)
	
    print('maximum plasma current: ',max(Ip2))

    tit='Plasma Current - shot '+str(shotnum)

    plt.plot(time2,Ip2/1000)
    plt.title(tit)
    plt.xlabel('time(s)')
    plt.ylabel('Plasma Current (kA)')
    plt.show()

#getIp(20032705,"Neil")
getIp(20082512,"mds")

#-----------------------------------------------------------------------------

	


