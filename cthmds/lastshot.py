# -*- coding: utf-8 -*-
# --------------------------------------
# lastShot.py
# 
# MDSplus Python project
# for CTH data access
#
# lastShot returns the last shot taken and the time when data was available
#
# Parameters:
#	none
# Return: 
# 	A sentence describing the last shot and the time it was taken
#
# Example:
#       lastShot()
#
# Greg Hartwell
# 2016-12-7
#----------------------------------------------------------------------------

from cthconnect import cthconnect
from cthopen import cthopen

def lastshot():
	c=cthconnect("neil")
	c.openTree("cthtree",12345)
	lastshotnum = c.get("prevnum")
	cthopen(c,lastshotnum)
	time=c.get("timestamp")
	c.closeAllTrees()
	
	t0 = str(int(time[0]))
	t1 = str(int(time[1]))
	t2 = str(int(time[2]))
	time=t0+':'+t1+':'+t2

	print('The last shot was',lastshotnum,'taken at',time)

# END of lastshot definition
#----------------------------------------------------------------------------

