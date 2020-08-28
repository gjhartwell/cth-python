# -*- coding: utf-8 -*-
"""
Created on Tue May 26 15:53:33 2020

@author: hartwgj
"""


# --------------------------------------
# OHShots.py
# 
# MDSplus Python project
# for CTH data access
#
# 	OHShots.py --- gets the shots within a given date range that use OH
#
# Parameters:
#	startdate
#   enddate
#	
# Returns:
#    list of shots
#
# Example:
#       shots=ohshots(190901,200329,'mds')
#
# Also defines:
#	
# Greg Hartwell
# 2020 May 26
#----------------------------------------------------------------------------

import cthmds

def ohshots(startdate,enddate,server):
    #allways connect to mds server
    c=cthmds.cthconnect(server)
    shots=[]
    for idate in range(startdate,enddate+1):
        # don't search for dates that don't exist    
        if ((idate % 100) <= 31) \
                        and ((idate % 10000 - idate % 100)/100) <= 12: 
            print(idate)
            for ishot in range(1,100):
                shotnum=idate*100+ishot
                #print(shotnum)
                try:
                    cthmds.cthopen(c,shotnum)
                except:
                    #print('shot not opened')
                    continue
                else:
                    try:
                        usestate=c.get('usestate')
                    except:
                        #print('usestate not found')
                        continue
                    else:
                        if usestate > 0:
                            usestate = \
                                [int(i) for i in bin(usestate)[2:]] 
                            usestate.reverse() 
                            # the OH is set at bit 5
                            if usestate[5]:
                                shots.append(shotnum)
                          
                    
    return shots
#-----------------------------------------------------------------------------

	


