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
# 	A sentence describing the last shot and the time
#
# Example:
#       lastShot
#
# Greg Hartwell
# 2016-12-7
#----------------------------------------------------------------------------

from cthconnect import cthconnect
from cthopen import *

c=cthconnect("neil")
c.openTree("cthtree",12345)
lastshot = c.get("prevnum")
c.closeAllTrees()
tree=treeFromShot(lastshot)
cthopen(c,lastshot)
time=c.get("timestamp")

t0 = str(int(time[0]))
t1 = str(int(time[1]))
t2 = str(int(time[2]))
time=t0+':'+t1+':'+t2

print('The last shot was',lastshot,'taken at',time)

# END of lastshot definition
#----------------------------------------------------------------------------

