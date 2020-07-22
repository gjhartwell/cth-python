# -*- coding: utf-8 -*-
"""
Created on Tue May 26 14:13:46 2020

@author: hartwgj
"""

# --------------------------------------
# AllShots.py
# 
# MDSplus Python project
# for CTH data access
#
# 	AllShots.py --- gets the shots within a given date range
#
# Parameters:
#	startdate
#   enddate
#	
# Returns:
#    list of shots
#
# Example:
#       shots=allshots(190901,200329)
#
# Also defines:
#	
# Greg Hartwell
# 2020 May 26
#----------------------------------------------------------------------------

import cthmds

def allshots(startdate,enddate):
    #allways connect to mds server
    c=cthmds.cthconnect("mds")
    shots=[]
    for idate in range(startdate,enddate+1):
        # don't search for dates that don't exist    
        if ((idate % 100) <= 31) \
                        and ((idate % 10000 - idate % 100)/100) <= 12: 
            print(idate)
            for ishot in range(1,100):
                shotnum=idate*100+ishot
                try:
                    cthmds.cthopen(c,shotnum)
                except:
                    # do nothing
                    continue
                else:
                    shots.append(shotnum)
                    
    return shots
	
#allshots(200326,200327)

#-----------------------------------------------------------------------------

	


